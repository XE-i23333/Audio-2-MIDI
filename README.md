# Audio 2 MIDI

<p align="center">
  <img src="logo.png" alt="Audio 2 MIDI" width="720">
</p>

<p align="center">
  <strong>English</strong> | <a href="README.zh-CN.md">简体中文</a> | <a href="README.ja.md">日本語</a>
</p>

Audio 2 MIDI is a Windows desktop application that combines Audio Separator and Basic Pitch for stem separation, audio-to-MIDI transcription, note export to CSV, and MIDI audio previews. CPU, NVIDIA CUDA, and DirectML editions are included.

## ✨ Features

- Separate vocals or instrumental stems.
- Convert original audio or a separated stem to MIDI.
- Export MIDI, note CSV, Basic Pitch model output (NPZ), and MIDI preview audio (WAV).
- Tune onset/frame thresholds, minimum note length, frequency range, and note merging.
- Open WAV, MP3, OGG, FLAC, and M4A files.
- Use the interface in English, Simplified Chinese, or Japanese.
- Monitor progress, processing speed, and logs.

Default Basic Pitch settings in this release include an onset threshold of `0` and a merge-notes interval of `50 ms`.

> 💡 **UVR-MDX-NET-Inst HQ 5** offers the best separation quality — recommended as the default choice.

<p align="center">
  <img src="screenshot.jpg" alt="Audio 2 MIDI Screenshot" width="720">
</p>

## 🚀 Choose an Edition

| Edition | Recommended hardware | Inference backend | Verified build size |
| --- | --- | --- | ---: |
| CPU | Systems without a suitable GPU; maximum compatibility | ONNX Runtime CPU | About 1.38 GB |
| CUDA | NVIDIA GPU | CUDA 12.4 (cu124) | About 5.82 GB |
| DirectML | AMD, Intel, or NVIDIA GPU | DirectML / DML Execution Provider | About 2.04 GB |

The CUDA edition requires an NVIDIA driver compatible with at least CUDA 12.4. The DirectML edition requires Windows 10/11, DirectX 12 support, and a current graphics driver. Choose CPU if you are unsure.

## 📦 Download and Run

Regular users should download an application package from **GitHub Releases**, not the automatically generated Source code archive.

1. Download the complete archive or every volume for your edition.
2. For a split archive, place all volumes in one directory and extract from `.7z.001`.
3. Extract the complete application directory. Do not copy only the EXE.
4. Run `Audio 2 MIDI (CPU).exe`, `Audio 2 MIDI (CUDA).exe`, or `Audio 2 MIDI (DirectML).exe`.

The first use of a separation model may require an internet connection. Downloaded models are stored under `models/audio-separator-models` beside the executable. The `UVR-MDX-NET-Inst_HQ_5.onnx` model is included by default.

## 🛠️ Run from Source

Requirements:

- 64-bit Windows 10 or Windows 11.
- 64-bit Python 3.10.
- FFmpeg is bundled — no environment variable setup required.
- An NVIDIA GPU and compatible driver for CUDA, or a DirectX 12 GPU for DirectML.

Choose one edition and create its environment inside that directory.

<details>
<summary>Using Python venv (click to expand)</summary>

Example for CPU:

```bat
cd cpu
py -3.10 -m venv .
Scripts\python.exe -m pip install --upgrade pip
Scripts\python.exe -m pip install -r requirements.txt
```

Start the application:

```bat
Scripts\python.exe main.py
```
</details>

Or using [uv](https://docs.astral.sh/uv/):

```bat
cd cpu
uv venv
uv pip install -r requirements.txt
uv run main.py
```

Follow the same process for `cuda` and `directml`, using the `requirements.txt` from that edition. Do not share one virtual environment between editions.

## 🏗️ Build the Windows Package

After preparing the environment and `ffmpeg` directory, run the edition-specific build script:

```bat
build.bat
```

Outputs are written to:

```text
cpu/dist/Audio 2 MIDI (CPU)/
cuda/dist/Audio 2 MIDI (CUDA)/
directml/dist/Audio 2 MIDI (DirectML)/
```

The script also copies `icon.ico` beside the executable. Publish the entire output directory because `_internal`, FFmpeg, runtime libraries, and resources are all required.

## 📁 Repository Layout

```text
Audio-2-MIDI-GitHub/
|-- cpu/                 # CPU source, dependencies, and build files
|-- cuda/                # NVIDIA CUDA source, dependencies, and build files
|-- directml/            # DirectML source, dependencies, and build files
|-- .gitignore
|-- README.md            # English
|-- README.zh-CN.md      # Simplified Chinese
|-- README.ja.md         # Japanese
`-- RELEASENOTE.md
```

## 🌐 Publishing on GitHub

Commit source code to the repository and attach packaged applications to GitHub Releases. Do not commit virtual environments, `build`, `dist`, FFmpeg binaries, downloaded models, local settings, or test media.

The CUDA package is too large for a single GitHub Release asset, and the DirectML package is close to the limit. Create 1900 MB 7-Zip volumes:

```bat
7z a -t7z -mx=9 -v1900m "Audio-2-MIDI-CUDA-v0.1.0.7z" "cuda\dist\Audio 2 MIDI (CUDA)\*"
```

The CPU package can normally be uploaded as one archive. Use GitHub Releases rather than Git LFS for downloadable application builds.

## ✅ Verification

All three editions passed dependency checks, GUI creation tests, real Basic Pitch transcription, Audio Separator processing, PyInstaller builds, and packaged application startup checks. Verified providers are `CPUExecutionProvider`, `CUDAExecutionProvider`, and `DmlExecutionProvider`.

## ⚖️ Third-Party Software

This project uses Audio Separator, Basic Pitch, ONNX Runtime, PyTorch, PyQt6, and FFmpeg. Before redistribution, review the licenses and attribution requirements for every dependency, model, FFmpeg build, icon, and logo.

## 🐞 Reporting Issues

Include the edition, Windows version, CPU/GPU model, graphics driver version, application log, and reproduction steps. Do not upload private or copyrighted audio without permission.
