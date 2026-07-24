# Audio 2 MIDI

<p align="center">
  <img src="cpu/logo.png" alt="Audio 2 MIDI" width="720">
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">简体中文</a> | <strong>日本語</strong>
</p>

Audio 2 MIDI は、Audio Separator と Basic Pitch を組み合わせた Windows 向けデスクトップアプリです。音源分離、音声から MIDI への変換、ノート CSV の出力、MIDI プレビュー音声の生成に対応し、CPU、NVIDIA CUDA、DirectML の 3 エディションを提供します。

## ✨ 機能

- ボーカルまたは伴奏ステムを分離。
- 元の音声または分離したステムを MIDI に変換。
- MIDI、ノート CSV、Basic Pitch モデル出力 NPZ、MIDI プレビュー WAV を保存。
- オンセット閾値、フレーム閾値、最短ノート長、周波数範囲、ノート結合時間を調整。
- WAV、MP3、OGG、FLAC、M4A を入力可能。
- English、簡体中文、日本語の UI を搭載。
- 進捗、処理速度、ログを確認可能。

このリリースの Basic Pitch の初期値は、オンセット閾値が `0`、Merge Notes が `50 ms` です。

> 💡 **UVR-MDX-NET-Inst HQ 5** の分離品質が最も高く、おすすめです。

<p align="center">
  <img src="screenshot.jpg" alt="Audio 2 MIDI スクリーンショット" width="720">
</p>

## 🚀 エディションの選択

| エディション | 推奨ハードウェア | 推論バックエンド | 検証済みサイズ |
| --- | --- | --- | ---: |
| CPU | 対応 GPU がない環境、互換性を優先する環境 | ONNX Runtime CPU | 約 1.38 GB |
| CUDA | NVIDIA GPU | CUDA 12.4 (cu124) | 約 5.82 GB |
| DirectML | AMD、Intel、NVIDIA GPU | DirectML / DML Execution Provider | 約 2.04 GB |

CUDA 版には CUDA 12.4 以上と互換性のある NVIDIA ドライバーが必要です。DirectML 版には Windows 10/11、DirectX 12 対応 GPU、最新のグラフィックスドライバーが必要です。不明な場合は CPU 版を使用してください。

## 📦 ダウンロードと実行

一般ユーザーは、自動生成される Source code ではなく、**GitHub Releases** からアプリをダウンロードしてください。

1. 使用するエディションの完全なアーカイブ、またはすべての分割ファイルをダウンロードします。
2. 分割アーカイブの場合は、全ファイルを同じフォルダーに置き、`.7z.001` から展開します。
3. アプリのフォルダー全体を展開します。EXE だけをコピーしないでください。
4. `Audio 2 MIDI (CPU).exe`、`Audio 2 MIDI (CUDA).exe`、または `Audio 2 MIDI (DirectML).exe` を実行します。

分離モデルの初回使用時にはインターネット接続が必要になる場合があります。モデルは EXE と同じ場所の `models/audio-separator-models` に保存されます。デフォルトで `UVR-MDX-NET-Inst_HQ_5.onnx` が含まれています。

## 🛠️ ソースから実行

必要な環境：

- 64 ビット版 Windows 10 または Windows 11。
- 64 ビット版 Python 3.10。
- FFmpeg はバンドルされています。環境変数の設定は不要です。
- CUDA 版には NVIDIA GPU と互換ドライバー、DirectML 版には DirectX 12 対応 GPU。

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

## 🏗️ Windows パッケージのビルド

仮想環境、依存パッケージ、`ffmpeg` を準備した後、対象ディレクトリで実行します：

```bat
build.bat
```

出力先：

```text
cpu/dist/Audio 2 MIDI (CPU)/
cuda/dist/Audio 2 MIDI (CUDA)/
directml/dist/Audio 2 MIDI (DirectML)/
```

スクリプトは `icon.ico` を EXE と同じディレクトリにもコピーします。`_internal`、FFmpeg、ランタイム、リソースが必要なため、リリース時は出力ディレクトリ全体を圧縮してください。

## 📁 リポジトリ構成

```text
Audio-2-MIDI-GitHub/
|-- cpu/                 # CPU のソース、依存関係、ビルド設定
|-- cuda/                # NVIDIA CUDA のソース、依存関係、ビルド設定
|-- directml/            # DirectML のソース、依存関係、ビルド設定
|-- .gitignore
|-- README.md            # English
|-- README.zh-CN.md      # 简体中文
|-- README.ja.md         # 日本語
`-- RELEASENOTE.md
```

## 🌐 GitHub での公開

ソースコードはリポジトリにコミットし、ビルド済みアプリは GitHub Releases に添付します。仮想環境、`build`、`dist`、FFmpeg バイナリ、ダウンロード済みモデル、ローカル設定、テスト音声はコミットしないでください。

CUDA 版は 1 つの GitHub Release ファイルとして公開できないサイズで、DirectML 版も制限に近いため、1900 MB の 7-Zip 分割アーカイブを推奨します：

```bat
7z a -t7z -mx=9 -v1900m "Audio-2-MIDI-CUDA-v0.1.0.7z" "cuda\dist\Audio 2 MIDI (CUDA)\*"
```

CPU 版は通常、1 つのアーカイブとして公開できます。アプリ配布には Git LFS ではなく GitHub Releases を使用してください。

## ✅ 検証状況

3 エディションすべてで、依存関係、GUI 作成、Basic Pitch の実音声変換、Audio Separator、PyInstaller ビルド、パッケージ起動を確認済みです。確認したプロバイダーは `CPUExecutionProvider`、`CUDAExecutionProvider`、`DmlExecutionProvider` です。

## ⚖️ サードパーティソフトウェア

本プロジェクトは Audio Separator、Basic Pitch、ONNX Runtime、PyTorch、PyQt6、FFmpeg を使用します。再配布前に、依存関係、モデル、FFmpeg build、アイコン、Logo のライセンスと表示要件を確認してください。

## 🐞 Issue の報告

エディション、Windows バージョン、CPU/GPU、グラフィックスドライバー、アプリのログ、再現手順を記載してください。許可のない個人情報や著作権保護された音声をアップロードしないでください。
