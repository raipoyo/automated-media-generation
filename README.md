# 🎬 Automated Media Generation with Claude Code SDK

このプロジェクトは、Claude Code SDKを使用してAIで猫の画像、動画、音楽を自動生成し、それらを組み合わせた最終的な動画を作成するGitHub Actionsワークフローです。

## 🌟 機能

- 🎨 **画像生成**: Google Imagen 3を使用して可愛い猫の画像を生成
- 📝 **テキストオーバーレイ**: 画像にカスタムテキストを追加
- 🎬 **動画生成**: Hailuo i2vを使用して画像から動画を生成
- 🎵 **音楽生成**: Google Lyriaを使用して癒し系の音楽を生成
- 🎞️ **動画結合**: 動画と音楽を組み合わせた最終的なメディアファイルを作成

## 🚀 セットアップ

### 1. 必要なAPIキー

以下のAPIキーをGitHubのSecretsに設定してください：

- `ANTHROPIC_API_KEY`: Claude APIキー
- `FAL_KEY`: Fal.ai APIキー（動画生成用）
- `GOOGLE_APPLICATION_CREDENTIALS_JSON`: Google Cloud サービスアカウントのJSONキー

### 2. GitHub Secretsの設定

1. GitHubリポジトリの **Settings** → **Secrets and variables** → **Actions** に移動
2. **New repository secret** をクリック
3. 以下のシークレットを追加：

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
FAL_KEY=your_fal_api_key_here
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type":"service_account",...}
```

### 3. ローカル開発環境のセットアップ

```bash
# リポジトリをクローン
git clone https://github.com/your-username/automated-media-generation.git
cd automated-media-generation

# 仮想環境を作成
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate  # Windows

# 依存関係をインストール
pip install -r requirements.txt

# 環境変数を設定
export ANTHROPIC_API_KEY="your_api_key"
export FAL_KEY="your_fal_key"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials.json"
```

## 🎯 使用方法

### GitHub Actionsによる自動実行

#### 手動実行
1. GitHubリポジトリの **Actions** タブに移動
2. **Generate Media with Claude Code SDK** ワークフローを選択
3. **Run workflow** をクリック
4. オプションでカスタムプロンプトを入力
5. **Run workflow** をクリックして実行

#### 自動実行（スケジュール）
- 毎日午前9時（UTC）に自動実行されます
- 生成されたメディアは自動的にリリースとして公開されます

### ローカル実行

```bash
# 基本実行
python generate_media.py

# カスタムプロンプトで実行
python generate_media.py \
  --image-prompt "A playful kitten in a garden" \
  --text-overlay "Hello World!" \
  --music-prompt "Upbeat and cheerful music"

# 出力ディレクトリを指定
python generate_media.py --output-dir custom_output
```

## 📁 プロジェクト構造

```
.
├── .github/
│   └── workflows/
│       └── generate-media.yml    # GitHub Actionsワークフロー
├── output/                       # 生成されたファイルの出力先
├── generate_media.py            # メイン実行スクリプト
├── requirements.txt             # Python依存関係
├── README.md                    # このファイル
└── combine_media.py             # 動画・音楽結合スクリプト
```

## 🔧 設定オプション

### コマンドライン引数

| 引数 | デフォルト値 | 説明 |
|------|-------------|------|
| `--image-prompt` | "A cute fluffy cat..." | 猫画像生成のプロンプト |
| `--text-overlay` | "The cat is so cute!" | 画像に追加するテキスト |
| `--music-prompt` | "Gentle healing music..." | 音楽生成のプロンプト |
| `--output-dir` | "output" | 出力ディレクトリ |

### GitHub Actions入力

ワークフローの手動実行時に以下のパラメータをカスタマイズできます：

- **prompt**: 猫画像生成のプロンプト
- **text_overlay**: 画像に追加するテキスト
- **music_prompt**: 音楽生成のプロンプト

## 📊 出力ファイル

生成される主なファイル：

1. **画像ファイル** (`.png`): テキストオーバーレイ付きの猫画像
2. **動画ファイル** (`.mp4`): 画像から生成された動画
3. **音楽ファイル** (`.wav`): 癒し系の背景音楽
4. **最終動画** (`final_cat_video_*.mp4`): 動画と音楽を組み合わせた完成品
5. **結果JSON** (`generation_results_*.json`): 生成プロセスの詳細

## 🛠️ トラブルシューティング

### よくある問題

1. **APIキーエラー**
   - GitHub Secretsが正しく設定されているか確認
   - APIキーの有効性を確認

2. **依存関係エラー**
   - `pip install -r requirements.txt` を再実行
   - Python バージョンが3.8以上であることを確認

3. **ファイル生成エラー**
   - 出力ディレクトリの書き込み権限を確認
   - 十分なディスク容量があることを確認

### ログの確認

GitHub Actionsの実行ログで詳細なエラー情報を確認できます：
1. **Actions** タブ → 該当のワークフロー実行をクリック
2. 失敗したステップのログを展開して確認

## 🔄 ワークフローの詳細

1. **画像生成**: Google Imagen 3 API使用
2. **動画生成**: Fal.ai Hailuo i2v API使用
3. **音楽生成**: Google Lyria API使用
4. **メディア結合**: MoviePyライブラリ使用
5. **自動リリース**: GitHub Releases機能使用

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🤝 コントリビューション

プルリクエストやイシューの報告を歓迎します！

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 🙏 謝辞

- [Claude Code SDK](https://docs.anthropic.com/claude/docs/claude-code) by Anthropic
- [Google Imagen 3](https://cloud.google.com/vertex-ai/docs/generative-ai/image/overview)
- [Fal.ai](https://fal.ai/) for video generation
- [Google Lyria](https://lyria.google/) for music generation
- [MoviePy](https://zulko.github.io/moviepy/) for video processing

---

🤖 **Generated with Claude Code SDK** ✨