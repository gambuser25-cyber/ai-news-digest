from html_template import build_html
import os
import sys
import json
import re
import html
import hashlib
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
import xml.etree.ElementTree as ET

try:
    import feedparser
    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False

JST = timezone(timedelta(hours=9))

RSS_FEEDS = [
    {
        "name": "Google News (AI)",
        "url": "https://news.google.com/rss/search?q=AI+OR+%E7%94%9F%E6%88%90AI+OR+LLM+when:24h&hl=ja&gl=JP&ceid=JP:ja",
        "default_category": "ビジネス・動向"
    },
    {
        "name": "Zenn (AI)",
        "url": "https://zenn.dev/topics/ai/feed",
        "default_category": "モデル・技術"
    },
    {
        "name": "Qiita (AI)",
        "url": "https://qiita.com/tags/ai/feed",
        "default_category": "モデル・技術"
    },
    {
        "name": "はてブ (IT/AI)",
        "url": "https://b.hatena.ne.jp/hotentry/it.rss",
        "default_category": "ツール・活用",
        "filter_keywords": ["ai", "gpt", "llm", "claude", "gemini", "人工知能", "生成", "機械学習", "モデル", "copilot", "cursor"]
    }
]

def clean_html(text: str) -> str:
    if not text:
        return ""
    # 簡易タグ除去 & HTMLエンティティデコード
    res = re.sub(r'<[^>]+>', ' ', text)
    res = html.unescape(res)
    res = re.sub(r'\s+', ' ', res)
    return res.strip()

def generate_id(url: str, title: str) -> str:
    raw = f"{url}_{title}".encode("utf-8")
    return hashlib.md5(raw).hexdigest()[:12]

def fetch_feed_fallback(url: str):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    )
    with urllib.request.urlopen(req, timeout=15) as res:
        xml_content = res.read()
    
    root = ET.fromstring(xml_content)
    entries = []
    
    items = root.findall(".//item")
    if not items:
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        items = root.findall(".//atom:entry", ns)
        if not items:
            items = root.findall(".//entry")
    
    for item in items:
        # Title
        title_el = item.find("title")
        if title_el is None:
            title_el = item.find("{http://www.w3.org/2005/Atom}title")
        title = "".join(title_el.itertext()).strip() if title_el is not None else ""

        # Link
        link_el = item.find("link")
        if link_el is None:
            link_el = item.find("{http://www.w3.org/2005/Atom}link")
        link = ""
        if link_el is not None:
            link = link_el.get("href") or "".join(link_el.itertext()).strip()

        # Description / Summary
        desc_candidates = [
            "description",
            "summary",
            "{http://www.w3.org/2005/Atom}summary",
            "{http://purl.org/rss/1.0/modules/content/}encoded",
            "content",
            "{http://www.w3.org/2005/Atom}content"
        ]
        desc = ""
        for tag in desc_candidates:
            el = item.find(tag)
            if el is not None:
                desc = "".join(el.itertext()).strip()
                if desc:
                    break

        # Date
        date_candidates = [
            "pubDate",
            "{http://purl.org/dc/elements/1.1/}date",
            "published",
            "{http://www.w3.org/2005/Atom}published",
            "updated",
            "{http://www.w3.org/2005/Atom}updated"
        ]
        date_str = ""
        for tag in date_candidates:
            el = item.find(tag)
            if el is not None:
                date_str = "".join(el.itertext()).strip()
                if date_str:
                    break

        entries.append({
            "title": title,
            "link": link,
            "summary": desc,
            "date_str": date_str
        })
    return entries

def parse_datetime(date_str: str) -> datetime:
    now = datetime.now(JST)
    if not date_str:
        return now
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.astimezone(JST)
    except Exception:
        pass
    try:
        clean_iso = date_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean_iso)
        return dt.astimezone(JST)
    except Exception:
        pass
    return now

def fetch_articles():
    articles = []
    seen_urls = set()

    for feed_info in RSS_FEEDS:
        print(f"Fetching: {feed_info['name']}...")
        try:
            if HAS_FEEDPARSER:
                feed = feedparser.parse(feed_info["url"])
                raw_entries = []
                for entry in feed.entries:
                    raw_entries.append({
                        "title": getattr(entry, "title", ""),
                        "link": getattr(entry, "link", ""),
                        "summary": getattr(entry, "summary", "") or getattr(entry, "description", ""),
                        "date_str": getattr(entry, "published", "") or getattr(entry, "updated", "")
                    })
            else:
                raw_entries = fetch_feed_fallback(feed_info["url"])

            print(f"  -> Got {len(raw_entries)} items")

            for item in raw_entries[:20]:
                url = item.get("link", "").strip()
                title = item.get("title", "").strip()
                if not url or not title or url in seen_urls:
                    continue

                filter_keywords = feed_info.get("filter_keywords")
                if filter_keywords:
                    combined = (title + " " + item.get("summary", "")).lower()
                    if not any(kw.lower() in combined for kw in filter_keywords):
                        continue

                seen_urls.add(url)
                clean_desc = clean_html(item.get("summary", ""))
                dt = parse_datetime(item.get("date_str", ""))

                articles.append({
                    "id": generate_id(url, title),
                    "title": title,
                    "url": url,
                    "source": feed_info["name"],
                    "published_at": dt.isoformat(),
                    "category": feed_info["default_category"],
                    "clean_desc": clean_desc[:250],
                    "summary_bullets": []
                })
        except Exception as e:
            print(f"  Error fetching {feed_info['name']}: {e}")

    # ソート（最新順）
    articles.sort(key=lambda x: x["published_at"], reverse=True)
    return articles[:30]

def call_gemini_api(prompt: str, api_key: str) -> str:
    models = ["gemini-2.5-flash", "gemini-1.5-flash"]
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json"
            }
        }
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as res:
                res_body = res.read().decode("utf-8")
                res_json = json.loads(res_body)
                text = res_json["candidates"][0]["content"]["parts"][0]["text"]
                return text
        except Exception as e:
            print(f"Gemini API ({model}) failed: {e}")
    return ""

def make_simple_bullets(desc: str, title: str) -> list:
    if not desc:
        return [title[:40]]
    sentences = [s.strip() for s in re.split(r'[。！？\n]', desc) if s.strip()]
    bullets = sentences[:3]
    if not bullets:
        bullets = [desc[:50] + ("..." if len(desc) > 50 else "")]
    return [b[:45] for b in bullets]

def fallback_summarize(articles: list):
    headline = "忙しい朝の30秒チェック！主要メディアやエンジニアコミュニティから最新のAI動向・技術アップデートを厳選してお届けします。"
    for art in articles:
        if not art["summary_bullets"]:
            art["summary_bullets"] = make_simple_bullets(art["clean_desc"], art["title"])
    return headline, articles

def summarize_with_gemini(articles: list, api_key: str):
    print("Summarizing articles with Gemini API...")
    if not articles:
        return fallback_summarize(articles)

    target_articles = articles[:15]
    articles_payload = []
    for idx, a in enumerate(target_articles):
        articles_payload.append({
            "idx": idx,
            "title": a["title"],
            "source": a["source"],
            "desc": a["clean_desc"]
        })

    prompt = f"""
あなたは毎朝通勤中に読むスマホ向けAIニュースアプリの編集長です。
以下の{len(target_articles)}件のAI関連ニュースを読み、日本のビジネスパーソンやエンジニア向けに要約してください。

入力記事リスト:
{json.dumps(articles_payload, ensure_ascii=False)}

出力形式（必ず指定のJSONオブジェクトのみを返してください）:
{{
  "headline_summary": "本日のAIトレンドを30秒で把握できるハイライトサマリー（120〜180文字程度で、最も注目すべき動きと全体の流れを簡潔にまとめる）",
  "articles": [
    {{
      "idx": 0,
      "category": "ビジネス・動向" または "モデル・技術" または "ツール・活用",
      "bullets": [
        "要点1（25文字以内、結論ファースト）",
        "要点2（25文字以内、具体的な数値やインパクト）",
        "要点3（25文字以内、何がポイントか）"
      ]
    }}
  ]
}}
"""
    raw_response = call_gemini_api(prompt, api_key)
    if not raw_response:
        print("Falling back to rule-based summary.")
        return fallback_summarize(articles)

    try:
        data = json.loads(raw_response)
        headline = data.get("headline_summary", "本日の注目AIニュースまとめをお届けします。")
        gemini_articles = {item["idx"]: item for item in data.get("articles", [])}

        for idx, art in enumerate(articles):
            if idx in gemini_articles:
                info = gemini_articles[idx]
                art["category"] = info.get("category", art["category"])
                art["summary_bullets"] = info.get("bullets", [])
            else:
                art["summary_bullets"] = make_simple_bullets(art["clean_desc"], art["title"])
        return headline, articles
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        return fallback_summarize(articles)

def main():
    now = datetime.now(JST)
    date_str = now.strftime("%Y年%m月%d日")
    datetime_str = now.strftime("%Y-%m-%d %H:%M JST")

    articles = fetch_articles()
    print(f"Total fetched articles: {len(articles)}")

    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if gemini_key:
        headline, articles = summarize_with_gemini(articles, gemini_key)
    else:
        print("GEMINI_API_KEY not found. Using fallback summary.")
        headline, articles = fallback_summarize(articles)

    output_data = {
        "updated_at": datetime_str,
        "date": date_str,
        "headline_summary": headline,
        "total_count": len(articles),
        "categories": ["すべて", "ビジネス・動向", "モデル・技術", "ツール・活用"],
        "articles": articles
    }

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "docs", "data")
    os.makedirs(data_dir, exist_ok=True)

    latest_json_path = os.path.join(data_dir, "latest.json")
    with open(latest_json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print(f"Saved latest data to: {latest_json_path}")

    archive_json_path = os.path.join(data_dir, f"{now.strftime('%Y-%m-%d')}.json")
    with open(archive_json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print(f"Saved archive to: {archive_json_path}")

    # Generate zero-network SSG index.html
    docs_dir = os.path.join(base_dir, "docs")
    index_html_path = os.path.join(docs_dir, "index.html")
    html_content = build_html(output_data)
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated standalone index.html to: {index_html_path}")

if __name__ == "__main__":
    main()
