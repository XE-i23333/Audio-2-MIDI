# Audio 2 MIDI

<p align="center">
  <img src="logo.png" alt="Audio 2 MIDI" width="720">
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <strong>日本語</strong>
</p>

Audio 2 MIDI は、Audio Separator と [Basic Pitch](https://github.com/spotify/basic-pitch) を組み合わせた Windows 向けデスクトップアプリです。音源分離、音声から MIDI への変換、ノート CSV の出力、MIDI プレビュー音声の生成に対応し、CPU、NVIDIA CUDA、DirectML の 3 エディションを提供します。

## ✨ 機能

- 🎤 ボーカルまたは伴奏ステムを分離。
- 🎹 元の音声または分離したステムを MIDI に変換。
- 📥 MIDI、ノート CSV、Basic Pitch モデル出力 NPZ、MIDI プレビュー WAV を保存。
- 🎛️ オンセット閾値、フレーム閾値、最短ノート長、周波数範囲、ノート結合時間を調整。
- 🔊 WAV、MP3、OGG、FLAC、M4A を入力可能。
- 🌐 English、簡体中文、日本語の UI を搭載。
- 📊 進捗、処理速度、ログを確認可能。

> 💡 **UVR-MDX-NET-Inst HQ 5** の分離品質が最も高く、おすすめです。

<p align="center">
  <img src="screenshot.png" alt="Audio 2 MIDI スクリーンショット" width="720">
</p>

## 🚀 エディションの選択

| エディション | 推奨ハードウェア | 推論バックエンド |
| --- | --- | --- |
| CPU | 対応 GPU がない環境、互換性を優先する環境 | ONNX Runtime CPU |
| CUDA | NVIDIA GPU | CUDA 12.4 (cu124) |
| DirectML | AMD、Intel、NVIDIA GPU、DX12 必須 | DirectML Execution Provider |

CUDA 版には CUDA 12.4 以上と互換性のある NVIDIA ドライバーが必要です。DirectML 版には Windows 10/11、DirectX 12 対応 GPU、最新のグラフィックスドライバーが必要です。古い Intel 内蔵グラフィック（Intel UHD 620 で動作確認済）でも DirectML 経由で実行可能です。不明な場合は CPU 版を使用してください。

## 📦 ダウンロードと実行

一般ユーザーは、自動生成される Source code ではなく、[GitHub Releases](../../releases/latest) からアプリをダウンロードしてください。

1. 使用するエディションのアーカイブをダウンロードします。
2. アプリのフォルダー全体を展開します。EXE だけをコピーしないでください。
3. `Audio 2 MIDI (CPU).exe`、`Audio 2 MIDI (CUDA).exe`、または `Audio 2 MIDI (DirectML).exe` を実行します。

分離モデルの初回使用時にはインターネット接続が必要になる場合があります。モデルは EXE と同じ場所の `models/audio-separator-models` に保存されます。デフォルトで `UVR-MDX-NET-Inst_HQ_5.onnx` が含まれています。

## 🛠️ ソースから実行

必要な環境：

- 64 ビット版 Windows 10 または Windows 11。
- Python ≤ 3.13.0（ビルド済み EXE は Python 3.10 でパッケージされています）。
- [FFmpeg builds ページ](https://www.gyan.dev/ffmpeg/builds/) から FFmpeg full-shared をダウンロードします（通常 7 個の DLL と 3 個の EXE が含まれます）。`bin` フォルダーを手動で実行またはビルドするエディションディレクトリ（`cpu/`、`cuda/`、または `directml/`）にコピーしてから `ffmpeg` にリネームします。
- CUDA 版には NVIDIA GPU と互換ドライバー、DirectML 版には DirectX 12 対応 GPU。

### ソースから実行

エディションを 1 つ選び、そのディレクトリ内に仮想環境を作成します。

<details>
<summary>Python venv を使用（クリックして展開）</summary>

CPU 版の例：

```bat
cd cpu
py -3.10 -m venv .
Scripts\python.exe -m pip install --upgrade pip
Scripts\python.exe -m pip install -r requirements.txt
```

ソースを起動します：

```bat
Scripts\python.exe main.py
```
</details>

または [uv](https://docs.astral.sh/uv/) を使用：

```bat
cd cpu
uv venv
uv pip install -r requirements.txt
uv run main.py
```

`cuda` と `directml` でも同じ手順を使用しますが、必ず各ディレクトリの `requirements.txt` をインストールしてください。3 エディションで仮想環境を共有しないでください。

### 手動ビルド

仮想環境、依存パッケージ、`ffmpeg` を準備した後、ビルドスクリプトを実行します：

```bat
build.bat
```

出力先：

```text
cpu/dist/Audio 2 MIDI (CPU)/
cuda/dist/Audio 2 MIDI (CUDA)/
directml/dist/Audio 2 MIDI (DirectML)/
```

## 📁 リポジトリ構成

```text
Audio-2-MIDI-GitHub/
|-- cpu/                 # CPU のソース、依存関係、ビルド設定
|-- cuda/                # NVIDIA CUDA のソース、依存関係、ビルド設定
|-- directml/            # DirectML のソース、依存関係、ビルド設定
|-- .gitignore
|-- LICENSE              # Apache-2.0
|-- logo.png
|-- screenshot.png
|-- README.md            # English
|-- README.zh-CN.md      # 简体中文
|-- README.ja.md         # 日本語
```

## ⚖️ サードパーティソフトウェア

本プロジェクトは Audio Separator、[Basic Pitch](https://github.com/spotify/basic-pitch)、ONNX Runtime、PyTorch、PyQt6、FFmpeg を使用します。再配布前に、依存関係、モデル、FFmpeg build、アイコン、Logo のライセンスと表示要件を確認してください。

## 🐞 Issue の報告

エディション、Windows バージョン、CPU/GPU、グラフィックスドライバー、アプリのログ、再現手順を記載してください。許可のない個人情報や著作権保護された音声をアップロードしないでください。
