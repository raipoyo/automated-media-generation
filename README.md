# Automated Protein Media Generation

プロテイン製品の画像・動画・音楽を自動生成するワークフローです。毎日定時実行され、完成した動画を自動的に作成します。

## 🎬 ワークフロー概要

1. **Imagen4 Ultra** - プロテイン製品の高品質な画像を生成
2. **Flux Kontext** - 画像に「Protein is good」テキストを追加
3. **Hailuo-02 Pro** - 画像を動的な動画に変換
4. **Google Lyria** - BGM音楽を生成
5. **FFmpeg** - 動画と音楽を結合して最終動画を作成

## 📁 ファイル構成

```
.
├── .github/workflows/
│   └── protein-media-generation.yml  # GitHub Actions ワークフロー
├── generate_protein_media.py         # メイン実行スクリプト
└── README.md                         # このファイル
```

## 🚀 セットアップ

### 1. 必要なシークレット設定

GitHub リポジトリの Settings > Secrets and variables > Actions で以下を設定：

| シークレット名 | 説明 | 取得方法 |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude API キー | [Anthropic Console](https://console.anthropic.com) |
| `FAL_KEY` | Fal.ai API キー | [Fal.ai Dashboard](https://fal.ai/dashboard) |
| `GOOGLE_API_KEY` | Google AI API キー | [Google AI Studio](https://aistudio.google.com) |

### 2. ワークフローの実行

#### 自動実行
- 毎日午前9時（JST）に自動実行
- cron: `0 0 * * *` (UTC 0:00 = JST 9:00)

#### 手動実行
1. GitHub リポジトリの「Actions」タブ
2. 「Automated Protein Media Generation」ワークフロー選択
3. 「Run workflow」ボタンクリック
4. 任意でカスタムプロンプトやテキストを指定

## 🔧 カスタマイズ

### プロンプトの変更

**画像生成プロンプト** (デフォルト):
```
High quality protein powder and supplements, professional product photography, clean white background, various protein containers including powder jars, protein bars, and shaker bottles, vibrant and appetizing presentation, studio lighting, commercial food photography style
```

**テキストオーバーレイ** (デフォルト):
```
Protein is good
```

### 実行頻度の変更

`.github/workflows/protein-media-generation.yml` の `cron` 設定を変更：

```yaml
schedule:
  # 毎日午前9時（JST）
  - cron: '0 0 * * *'
  
  # 毎週月曜日午前9時（JST）
  - cron: '0 0 * * 1'
  
  # 毎時実行
  - cron: '0 * * * *'
```

## 📊 出力ファイル

各実行で以下のファイルが生成されます：

- `imagen4_ultra_YYYYMMDD_HHMMSS.png` - 元の画像
- `kontext_YYYYMMDD_HHMMSS.jpg` - テキスト付き画像
- `hailuo_02_YYYYMMDD_HHMMSS.mp4` - 動画
- `lyria_output_XXXXXXXX.wav` - BGM音楽
- `final_protein_video_with_music_YYYYMMDD_HHMMSS.mp4` - 最終動画

## 💾 ストレージ管理

- **アーティファクト**: 30日間保持
- **リリース**: 定期実行時に自動作成
- **自動クリーンアップ**: 7日以上古いファイルを削除

## 🛠️ ローカル実行

```bash
# 依存関係のインストール
pip install requests mcp-sdk anthropic

# 環境変数設定
export ANTHROPIC_API_KEY="your-api-key"
export FAL_KEY="your-fal-key"
export GOOGLE_API_KEY="your-google-key"

# スクリプト実行
python generate_protein_media.py
```

## 🔍 トラブルシューティング

### よくある問題

1. **API キーエラー**
   - シークレットが正しく設定されているか確認
   - API キーの有効期限をチェック

2. **ffmpeg エラー**
   - Ubuntu の場合は自動インストール
   - ローカル実行時は手動インストール必要

3. **ファイルサイズ制限**
   - GitHub Actions の制限: 2GB
   - 必要に応じて圧縮設定を調整

### ログの確認

GitHub Actions の実行ログで詳細なエラー情報を確認できます：
1. Actions タブ > 該当ワークフロー > 実行結果
2. 各ステップのログを展開して確認

## 📝 ライセンス

このプロジェクトは MIT ライセンスの元で公開されています。

## 🤝 貢献

プルリクエストやイシューは歓迎です。改善提案がありましたらお気軽にお知らせください。

---

**注意**: 本ワークフローは AI サービスの API を使用するため、利用料金が発生する可能性があります。各サービスの料金体系を確認してご利用ください。