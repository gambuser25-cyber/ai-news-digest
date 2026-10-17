# 🌅 AI Morning Digest (AIモーニング)

> **通勤中や隙間時間にスマホでサクサク読める、毎朝自動更新のAIニュースまとめアプリ**  
> GitHub Actions × GitHub Pages の組み合わせにより、**PC電源オフ・サーバー代0円・完全無料** で永続稼働します。

---

## 📱 アプリの特徴

- ⏱ **タイパ重視の3行要約**: 朝の忙しい電車内でもサッと読める30秒ハイライト＆各記事の要点箇条書き
- 📱 **スマホ最適化 (PWA)**: ホーム画面に追加すればネイティブアプリ感覚で起動。ダークモード対応
- 🚇 **オフライン対応**: 地下鉄など電波が不安定な場所でも、キャッシュによりストレスフリーで閲覧可能
- 🏷 **カテゴリ分類 & 検索**: 「ビジネス・動向」「モデル・技術」「ツール・活用」やキーワード絞り込み
- 🔖 **読了・保存管理**: タップするだけで「既読」（半透明化）＆「ブックマーク（あとで読む）」をローカル保存
- 💰 **完全無料＆メンテフリー**: GitHub Actionsの無料枠（月2,000分）とGitHub Pagesの無料枠で稼働。追加サーバー代は永久に0円

---

## 🛠 システム構成

```mermaid
flowchart TD
    subgraph GitHub Cloud [クラウド上で完全自動実行 (PCオフでOK)]
        A[毎朝6:00 JST<br>GitHub Actions Cron] --> B[scripts/fetch_and_build.py 実行]
        B --> C[RSSフィード収集<br>Google News / Zenn / Qiita / はてブ]
        C --> D[Gemini API による要約 & 分類<br>無料枠利用 / 未設定時は自動フォールバック]
        D --> E[docs/data/latest.json 生成]
        E --> F[GitHub Pages へ自動デプロイ]
    end

    subgraph User Device [スマートフォン (Safari / Chrome)]
        F --> G[PWA Webアプリ<br>https://ユーザー名.github.io/リポジトリ名/]
        G --> H[ホーム画面に追加して通勤中にチェック！]
    end
```

---

## 🚀 導入手順（たったの3ステップ）

### 1. リポジトリをGitHubにプッシュ
このプロジェクト一式をご自身のGitHubアカウントに新規作成したリポジトリ（例: `ai-news-digest`）へプッシュします。

```bash
git init
git add .
git commit -m "feat: initial commit of AI Morning Digest"
git branch -M main
git remote add origin https://github.com/<あなたのユーザー名>/ai-news-digest.git
git push -u origin main
```

### 2. GitHub Pages を有効化する
1. GitHubのリポジトリページを開き、**Settings** タブをクリック。
2. 左メニューの **Pages** を選択。
3. **Build and deployment** の **Source** を **`GitHub Actions`** に設定します。

### 3. （任意）Gemini APIキーを設定する（より高度な要約を利用する場合）
> 💡 **APIキーがなくても動作します**（その場合はRSSの概要から自動で3行要約が生成されます）。  
> 無料で取得できる Google Gemini API キーを設定すると、AIによる高品質な朝刊ハイライト＆要点要約が有効になります。

1. [Google AI Studio](https://aistudio.google.com/) にアクセスし、「Get API key」から無料キーを取得。
2. GitHubリポジトリの **Settings** > **Secrets and variables** > **Actions** を開く。
3. **New repository secret** をクリック：
   - Name: `GEMINI_API_KEY`
   - Secret: 取得したAPIキー
4. **Add secret** をクリックして保存。

### 4. 初回実行（手動テスト）
毎朝6:00（JST）に自動実行されますが、今すぐ確認したい場合は手動実行できます：
1. リポジトリの **Actions** タブを開く。
2. 左側の **Daily AI News Digest Update** をクリック。
3. **Run workflow** ボタンをクリック。
4. 数分でビルドとPagesへのデプロイが完了します！

---

## 📲 スマホのホーム画面に追加する方法

1. スマートフォンのブラウザ（iPhoneならSafari、AndroidならChrome）で、公開されたGitHub PagesのURLを開きます。
   - URL形式: `https://<あなたのユーザー名>.github.io/<リポジトリ名>/`
2. **iPhone (Safari)**:
   - 画面下の「共有ボタン（四角から上矢印）」をタップ ➔「**ホーム画面に追加**」を選択。
3. **Android (Chrome)**:
   - 画面右上のメニュー「︙」をタップ ➔「**アプリをインストール**」または「**ホーム画面に追加**」を選択。
4. ホーム画面にアプリアイコンが追加され、全画面で快適にニュースを読めるようになります。

---

## ⚙️ カスタマイズガイド

- **更新時間を変えたい**:
  - `.github/workflows/daily_update.yml` の `cron: '0 21 * * *'` を変更します（UTC基準。例: 朝7時にしたい場合は `cron: '0 22 * * *'`）。
- **ニュース収集元を追加・変更したい**:
  - `scripts/fetch_and_build.py` の `RSS_FEEDS` 配列にお好みのRSSフィードURLを追加するだけです。
- **デザインを変更したい**:
  - `docs/index.html` はTailwind CSSで構築されているため、HTML内のクラス名を編集するだけで自由に配色やレイアウトを調整できます。

---

## 📄 ライセンス
MIT License
