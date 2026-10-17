# scripts/html_template.py
import json
import html

SVG_ICONS = {
    "sparkles": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>',
    "zap": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="#fbbf24" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
    "search": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
    "moon": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>',
    "sun": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>',
    "check_circle": '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    "circle": '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/></svg>',
    "bookmark": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/></svg>',
    "bookmark_filled": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="#f59e0b" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/></svg>',
    "share": '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" x2="15.42" y1="13.51" y2="17.49"/><line x1="15.41" x2="8.59" y1="6.51" y2="10.49"/></svg>',
    "external": '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" x2="21" y1="14" y2="3"/></svg>'
}

def build_html(data: dict) -> str:
    embedded_json = json.dumps(data, ensure_ascii=False)
    
    html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>AI Morning Digest | 毎朝のAIニュースまとめ</title>
  <meta name="description" content="毎朝自動更新。通勤中や隙間時間にスマホでサクサク読めるAIニュース要約アプリ。">
  <link rel="manifest" href="./manifest.json">
  <meta name="theme-color" content="#1e1b4b">
  <link rel="icon" type="image/svg+xml" href="./icon.svg">
  <link rel="apple-touch-icon" href="./icon.svg">
  <style>
    :root {{
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --card-sub: #f1f5f9;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --primary: #4f46e5;
      --primary-light: #eef2ff;
      --primary-text: #4338ca;
    }}
    html.dark {{
      --bg: #090d16;
      --card-bg: #0f172a;
      --card-sub: #1e293b;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --border: #1e293b;
      --primary: #6366f1;
      --primary-light: #1e1b4b;
      --primary-text: #a5b4fc;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}
    body {{
      background-color: var(--bg);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Hiragino Sans", "Noto Sans JP", sans-serif;
      min-height: 100vh;
      padding-bottom: 60px;
      transition: background-color 0.2s, color 0.2s;
    }}
    .container {{
      max-width: 680px;
      margin: 0 auto;
      padding: 0 16px;
    }}
    header {{
      position: sticky;
      top: 0;
      z-index: 50;
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border);
      transition: background-color 0.2s, border-color 0.2s;
    }}
    html.dark header {{
      background: rgba(15, 23, 42, 0.85);
    }}
    .header-content {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 16px;
    }}
    .logo-area {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .logo-badge {{
      width: 36px;
      height: 36px;
      border-radius: 10px;
      background: linear-gradient(135deg, #4f46e5, #0ea5e9);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25);
    }}
    .title-area h1 {{
      font-size: 15px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 6px;
      line-height: 1.2;
    }}
    .badge-tag {{
      font-size: 10px;
      background: var(--primary-light);
      color: var(--primary-text);
      font-weight: 600;
      padding: 2px 6px;
      border-radius: 12px;
    }}
    .title-area p {{
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 2px;
    }}
    .theme-btn {{
      background: none;
      border: none;
      color: var(--text-muted);
      padding: 8px;
      border-radius: 10px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .tabs-container {{
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding: 0 16px 10px;
      scrollbar-width: none;
    }}
    .tabs-container::-webkit-scrollbar {{
      display: none;
    }}
    .tab-btn {{
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      white-space: nowrap;
      cursor: pointer;
      border: 1px solid var(--border);
      background: var(--card-bg);
      color: var(--text-muted);
      transition: all 0.15s;
    }}
    .tab-btn.active {{
      background: var(--primary);
      color: white;
      border-color: var(--primary);
      box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25);
    }}
    main {{
      margin-top: 16px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .progress-bar-area {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      color: var(--text-muted);
      padding: 0 4px;
    }}
    .progress-count {{
      display: flex;
      align-items: center;
      gap: 6px;
      color: #10b981;
      font-weight: 600;
    }}
    .mark-all-btn {{
      background: none;
      border: none;
      color: var(--primary);
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
    }}
    .highlight-card {{
      background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #0f172a 100%);
      color: #ffffff;
      padding: 18px 20px;
      border-radius: 18px;
      box-shadow: 0 8px 20px rgba(30, 27, 75, 0.2);
      border: 1px solid rgba(99, 102, 241, 0.25);
      position: relative;
      overflow: hidden;
    }}
    .highlight-title {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 700;
      color: #a5b4fc;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 8px;
    }}
    .highlight-text {{
      font-size: 13.5px;
      line-height: 1.6;
      color: #e0e7ff;
      font-weight: 500;
    }}
    .search-box {{
      position: relative;
    }}
    .search-icon {{
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      pointer-events: none;
    }}
    .search-input {{
      width: 100%;
      padding: 10px 14px 10px 38px;
      border-radius: 12px;
      border: 1px solid var(--border);
      background: var(--card-bg);
      color: var(--text-main);
      font-size: 13.5px;
      outline: none;
      box-shadow: 0 1px 3px rgba(0,0,0,0.02);
      transition: border-color 0.15s, box-shadow 0.15s;
    }}
    .search-input:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
    }}
    .article-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 16px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.02);
      transition: all 0.15s;
      margin-bottom: 12px;
    }}
    .article-card.read {{
      opacity: 0.55;
      background: var(--card-sub);
    }}
    .article-card:hover {{
      border-color: #cbd5e1;
    }}
    html.dark .article-card:hover {{
      border-color: #334155;
    }}
    .card-meta {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      margin-bottom: 8px;
    }}
    .category-chip {{
      background: var(--primary-light);
      color: var(--primary-text);
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 6px;
    }}
    .source-meta {{
      color: var(--text-muted);
    }}
    .article-title {{
      font-size: 14.5px;
      font-weight: 700;
      line-height: 1.45;
      margin-bottom: 10px;
    }}
    .article-title a {{
      color: var(--text-main);
      text-decoration: none;
    }}
    .article-title a:hover {{
      color: var(--primary);
    }}
    .bullets-box {{
      background: var(--card-sub);
      border-radius: 10px;
      padding: 10px 12px;
      margin-bottom: 12px;
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .bullet-item {{
      font-size: 12px;
      color: var(--text-main);
      display: flex;
      align-items: flex-start;
      gap: 6px;
      line-height: 1.4;
    }}
    .bullet-dot {{
      color: var(--primary);
      font-weight: bold;
      line-height: 1;
      margin-top: 2px;
    }}
    .card-actions {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 10px;
      border-top: 1px solid var(--border);
    }}
    .action-btn {{
      background: none;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 12px;
      color: var(--text-muted);
      padding: 4px 6px;
      border-radius: 8px;
    }}
    .action-btn.active {{
      color: #10b981;
      font-weight: 600;
    }}
    .right-actions {{
      display: flex;
      align-items: center;
      gap: 4px;
    }}
    .icon-action-btn {{
      background: none;
      border: none;
      cursor: pointer;
      padding: 6px;
      border-radius: 8px;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .icon-action-btn:hover {{
      color: var(--text-main);
    }}
    .link-action {{
      display: flex;
      align-items: center;
      gap: 2px;
      color: var(--primary);
      text-decoration: none;
      font-size: 12px;
      font-weight: 600;
      padding-left: 6px;
    }}
    .link-action:hover {{
      text-decoration: underline;
    }}
    .empty-message {{
      text-align: center;
      padding: 40px 0;
      color: var(--text-muted);
      font-size: 13px;
    }}
  </style>
</head>
<body>

  <!-- Header -->
  <header>
    <div class="container header-content">
      <div class="logo-area">
        <div class="logo-badge">
          {SVG_ICONS["sparkles"]}
        </div>
        <div class="title-area">
          <h1>AI Morning Digest <span class="badge-tag">毎朝更新</span></h1>
          <p id="header-date">{html.escape(data.get("date", ""))} 更新 ({html.escape(data.get("updated_at", ""))})</p>
        </div>
      </div>
      <button id="theme-toggle" class="theme-btn" aria-label="テーマ切り替え">
        <span id="theme-icon">{SVG_ICONS["moon"]}</span>
      </button>
    </div>
    
    <!-- Category Tabs -->
    <div class="container">
      <div class="tabs-container" id="category-tabs"></div>
    </div>
  </header>

  <!-- Main -->
  <main class="container">

    <!-- Progress -->
    <div class="progress-bar-area">
      <div class="progress-count">
        {SVG_ICONS["check_circle"]}
        <span id="read-progress">読了状況: 0 / {len(data.get("articles", []))} 記事</span>
      </div>
      <button id="mark-all-read" class="mark-all-btn">すべて既読にする</button>
    </div>

    <!-- 30-Sec Highlight -->
    <section class="highlight-card">
      <div class="highlight-title">
        {SVG_ICONS["zap"]}
        今日の30秒ハイライト
      </div>
      <p class="highlight-text">{html.escape(data.get("headline_summary", "最新のAI動向をお届けします。"))}</p>
    </section>

    <!-- Search Input -->
    <div class="search-box">
      <span class="search-icon">{SVG_ICONS["search"]}</span>
      <input type="search" id="search-input" class="search-input" placeholder="キーワードで検索 (例: Claude, OpenAI, Cursor...)">
    </div>

    <!-- Articles List -->
    <section id="articles-list"></section>

  </main>

  <!-- Embedded Data & Scripts -->
  <script>
    const INITIAL_DATA = {embedded_json};
    let currentCategory = 'すべて';
    let searchQuery = '';
    let readArticles = new Set(JSON.parse(localStorage.getItem('ai_news_read') || '[]'));
    let bookmarkedArticles = new Set(JSON.parse(localStorage.getItem('ai_news_bookmarks') || '[]'));

    const ICONS = {{
      sun: `{SVG_ICONS["sun"]}`,
      moon: `{SVG_ICONS["moon"]}`,
      check: `{SVG_ICONS["check_circle"]}`,
      circle: `{SVG_ICONS["circle"]}`,
      bookmark: `{SVG_ICONS["bookmark"]}`,
      bookmark_filled: `{SVG_ICONS["bookmark_filled"]}`,
      share: `{SVG_ICONS["share"]}`,
      external: `{SVG_ICONS["external"]}`
    }};

    // Theme Management
    const themeBtn = document.getElementById('theme-toggle');
    const themeIconSpan = document.getElementById('theme-icon');

    function initTheme() {{
      const saved = localStorage.getItem('ai_news_theme');
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      if (saved === 'dark' || (!saved && prefersDark)) {{
        document.documentElement.classList.add('dark');
        themeIconSpan.innerHTML = ICONS.sun;
      }} else {{
        document.documentElement.classList.remove('dark');
        themeIconSpan.innerHTML = ICONS.moon;
      }}
    }}

    themeBtn.addEventListener('click', () => {{
      const isDark = document.documentElement.classList.toggle('dark');
      localStorage.setItem('ai_news_theme', isDark ? 'dark' : 'light');
      themeIconSpan.innerHTML = isDark ? ICONS.sun : ICONS.moon;
    }});

    initTheme();

    // Render Tabs
    function renderTabs() {{
      const container = document.getElementById('category-tabs');
      container.innerHTML = '';
      const categories = [...(INITIAL_DATA.categories || ['すべて']), '★ 保存済み'];
      categories.forEach(cat => {{
        const btn = document.createElement('button');
        btn.className = 'tab-btn' + (currentCategory === cat ? ' active' : '');
        btn.textContent = cat;
        btn.addEventListener('click', () => {{
          currentCategory = cat;
          renderTabs();
          renderArticles();
        }});
        container.appendChild(btn);
      }});
    }}

    // Filter Articles
    function getFilteredArticles() {{
      const articles = INITIAL_DATA.articles || [];
      let list = articles;

      if (currentCategory === '★ 保存済み') {{
        list = list.filter(a => bookmarkedArticles.has(a.id));
      }} else if (currentCategory !== 'すべて') {{
        list = list.filter(a => a.category === currentCategory);
      }}

      if (searchQuery.trim()) {{
        const q = searchQuery.toLowerCase();
        list = list.filter(a => 
          (a.title && a.title.toLowerCase().includes(q)) ||
          (a.clean_desc && a.clean_desc.toLowerCase().includes(q)) ||
          (a.summary_bullets && a.summary_bullets.some(b => b.toLowerCase().includes(q)))
        );
      }}
      return list;
    }}

    // Render Articles List
    function renderArticles() {{
      const container = document.getElementById('articles-list');
      const filtered = getFilteredArticles();
      const allArticles = INITIAL_DATA.articles || [];

      // Update progress
      const readCount = allArticles.filter(a => readArticles.has(a.id)).length;
      document.getElementById('read-progress').textContent = '読了状況: ' + readCount + ' / ' + allArticles.length + ' 記事';

      if (filtered.length === 0) {{
        container.innerHTML = '<div class="empty-message">該当する記事が見つかりませんでした</div>';
        return;
      }}

      container.innerHTML = filtered.map(art => {{
        const isRead = readArticles.has(art.id);
        const isBookmarked = bookmarkedArticles.has(art.id);
        const bullets = art.summary_bullets && art.summary_bullets.length > 0
          ? art.summary_bullets.map(b => '<li class="bullet-item"><span class="bullet-dot">•</span><span>' + escapeHtml(b) + '</span></li>').join('')
          : '<li class="bullet-item"><span class="bullet-dot">•</span><span>' + escapeHtml(art.clean_desc || art.title) + '</span></li>';

        return '<article class="article-card' + (isRead ? ' read' : '') + '">' +
          '<div class="card-meta">' +
            '<span class="category-chip">' + escapeHtml(art.category) + '</span>' +
            '<span class="source-meta">' + escapeHtml(art.source) + ' • ' + formatTime(art.published_at) + '</span>' +
          '</div>' +
          '<h2 class="article-title">' +
            '<a href="' + escapeHtml(art.url) + '" target="_blank" rel="noopener noreferrer">' + escapeHtml(art.title) + '</a>' +
          '</h2>' +
          '<ul class="bullets-box">' + bullets + '</ul>' +
          '<div class="card-actions">' +
            '<button onclick="toggleRead(\\'' + art.id + '\\')" class="action-btn' + (isRead ? ' active' : '') + '">' +
              (isRead ? ICONS.check : ICONS.circle) +
              '<span>' + (isRead ? '既読' : '既読にする') + '</span>' +
            '</button>' +
            '<div class="right-actions">' +
              '<button onclick="toggleBookmark(\\'' + art.id + '\\')" class="icon-action-btn" title="保存">' +
                (isBookmarked ? ICONS.bookmark_filled : ICONS.bookmark) +
              '</button>' +
              '<button onclick="shareArticle(\\'' + escapeJs(art.title) + '\\', \\'' + escapeJs(art.url) + '\\')" class="icon-action-btn" title="共有">' +
                ICONS.share +
              '</button>' +
              '<a href="' + escapeHtml(art.url) + '" target="_blank" rel="noopener noreferrer" class="link-action">' +
                '<span>記事へ</span>' + ICONS.external +
              '</a>' +
            '</div>' +
          '</div>' +
        '</article>';
      }}).join('');
    }}

    window.toggleRead = function(id) {{
      if (readArticles.has(id)) {{
        readArticles.delete(id);
      }} else {{
        readArticles.add(id);
      }}
      localStorage.setItem('ai_news_read', JSON.stringify(Array.from(readArticles)));
      renderArticles();
    }};

    window.toggleBookmark = function(id) {{
      if (bookmarkedArticles.has(id)) {{
        bookmarkedArticles.delete(id);
      }} else {{
        bookmarkedArticles.add(id);
      }}
      localStorage.setItem('ai_news_bookmarks', JSON.stringify(Array.from(bookmarkedArticles)));
      renderArticles();
    }};

    document.getElementById('mark-all-read').addEventListener('click', () => {{
      const allArticles = INITIAL_DATA.articles || [];
      allArticles.forEach(a => readArticles.add(a.id));
      localStorage.setItem('ai_news_read', JSON.stringify(Array.from(readArticles)));
      renderArticles();
    }});

    window.shareArticle = function(title, url) {{
      if (navigator.share) {{
        navigator.share({{ title: title, text: '【AI Morning】' + title, url: url }}).catch(() => {{}});
      }} else {{
        navigator.clipboard.writeText(title + ' ' + url).then(() => {{
          alert('URLをクリップボードにコピーしました！');
        }});
      }}
    }};

    document.getElementById('search-input').addEventListener('input', (e) => {{
      searchQuery = e.target.value;
      renderArticles();
    }});

    function escapeHtml(str) {{
      if (!str) return '';
      return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }}

    function escapeJs(str) {{
      if (!str) return '';
      return String(str).replace(/\\\\/g, '\\\\\\\\').replace(/'/g, "\\\\'").replace(/"/g, '\\\\"');
    }}

    function formatTime(isoStr) {{
      if (!isoStr) return '';
      try {{
        const dt = new Date(isoStr);
        const m = (dt.getMonth() + 1).toString().padStart(2, '0');
        const d = dt.getDate().toString().padStart(2, '0');
        const h = dt.getHours().toString().padStart(2, '0');
        const min = dt.getMinutes().toString().padStart(2, '0');
        return m + '/' + d + ' ' + h + ':' + min;
      }} catch {{
        return '';
      }}
    }}

    // Service Worker
    if ('serviceWorker' in navigator) {{
      window.addEventListener('load', () => {{
        navigator.serviceWorker.register('./sw.js').catch(() => {{}});
      }});
    }}

    // Initial render
    renderTabs();
    renderArticles();
  </script>
</body>
</html>"""
    return html_template
