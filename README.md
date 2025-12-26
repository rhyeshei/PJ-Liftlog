# Liftlog（開発途中）

筋トレの記録と音楽操作を1つの画面で完結させ、
トレーニング中の没入感を最大化することを目的としたアプリです。

## 設計ドキュメント

- 要件定義書（Google Docs）  
  https://docs.google.com/document/d/1IXJkok0C_B1p_BbXeqyv0kcPVPG1RtPufon8oMWEHWA/edit?usp=sharing

- 基本設計書（Google Docs）  
  https://docs.google.com/document/d/1fqO6WoMOt6bc08GyvpJem_3MfDcPuUQrlNyOMoGwqxI/edit?usp=sharing

※ 本プロジェクトは、要件定義 → 基本設計 → 実装の流れで開発しています。


## 主な特徴
- ワークアウト記録と音楽操作を同一画面に統合
- セット記録時に休憩時間を自動取得
- オフライン環境でも記録可能（IndexedDB）
- 将来的に Apple Music / Spotify と連携予定

## 実装状況（概要）

- 認証：DRF Token認証、カスタムユーザーモデル
- ワークアウト記録：Workout / SetRecord / 種目マスタ
- テンプレート：過去ワークアウトから自動生成
- 分析API：部位別ボリューム・重量推移
- 音楽連携：認証・トークン管理まで実装（再生制御は未実装）
- API仕様：Swagger UI（/api/docs/）

<details>
<summary>実装詳細</summary>

### ユーザー認証
- email をユニークキーとしたカスタムユーザーモデル
- DRF TokenAuthentication によるAPI認証

### ワークアウト記録
- Workout / SetRecord / ExerciseMaster モデル
- 開始・終了・セット追加API
- セット追加時に種目ごとの休憩時間（秒）を返却

### テンプレート
- テンプレートの保存・取得
- 過去ワークアウトから自動生成

### 音楽連携
- Apple Music / Spotify 用トークン管理モデル
- 認証・プレイリスト取得（モック実装）

### 分析API
- 部位別トレーニングボリューム集計
- 種目別Max重量の推移データ

</details>

## 技術スタック

### Backend
- Python
- Django 4.2 / Django REST Framework
- SQLite（開発環境）
- 認証：DRF TokenAuthentication
- APIドキュメント：drf-spectacular（Swagger UI）
- セキュリティ：bcrypt
- CORS：django-cors-headers

### Frontend
- Vue.js（開発中）
- 状態管理：Vue Reactive API
- オフライン対応：IndexedDB / LocalStorage
- Native Bridge：Capacitor（iOS / Android予定）

### Music Integration
- Apple Music：MusicKit JS / Native SDK（予定）
- Spotify：Spotify App Remote（予定）


## 今後の予定
- 音楽の再生・曲送り等の実装
- フロントエンドUIの本格実装
- トレーニング分析機能の拡張

※ 本プロジェクトは現在開発途中です。
