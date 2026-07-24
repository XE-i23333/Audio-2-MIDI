# Audio 2 MIDI

<p align="center">
  <img src="logo.png" alt="Audio 2 MIDI" width="720">
</p>

<p align="center">
  <a href="README.md">English</a> | <strong>简体中文</strong> | <a href="README.ja.md">日本語</a>
</p>

Audio 2 MIDI 是一个 Windows 桌面音频处理工具，结合 Audio Separator 与 [Basic Pitch](https://github.com/spotify/basic-pitch)，支持音轨分离、音频转 MIDI、音符 CSV 导出和 MIDI 音频预览。仓库提供 CPU、NVIDIA CUDA 和 DirectML 三个版本。

## ✨ 功能

- 🎤 分离人声或伴奏音轨。
- 🎹 将原始音频或分离后的音轨转换为 MIDI。
- 📥 导出 MIDI、音符 CSV、Basic Pitch 模型输出 NPZ 和 MIDI 音频预览 WAV。
- 🎛️ 调整起始阈值、帧阈值、最短音符长度、频率范围及相邻音符合并时间。
- 🔊 支持 WAV、MP3、OGG、FLAC 和 M4A。
- 🌐 提供简体中文、English 和日本語界面。
- 📊 查看实时进度、处理速度和运行日志。

> 💡 **UVR-MDX-NET-Inst HQ 5** 分离效果最好，推荐优先选择。

<p align="center">
  <img src="screenshot.png" alt="Audio 2 MIDI 截图" width="720">
</p>

## 🚀 版本选择

| 版本 | 适用设备 | 推理后端 | 已验证成品体积 |
| --- | --- | --- | ---: |
| CPU | 无可用 GPU，或追求最高兼容性 | ONNX Runtime CPU | 约 1.38 GB |
| CUDA | NVIDIA GPU | CUDA 12.4 (cu124) | 约 5.82 GB |
| DirectML | AMD、Intel 或 NVIDIA GPU | DirectML / DML Execution Provider | 约 2.04 GB |

CUDA 版至少需要 CUDA 12.4 的 NVIDIA 驱动。DirectML 版需要 Windows 10/11、DirectX 12 支持和较新的显卡驱动。不确定设备是否兼容时建议使用 CPU 版。

## 📦 下载和运行

普通用户应从 [GitHub Releases](../../releases/latest) 页面下载程序，不要下载自动生成的 Source code 压缩包。

1. 下载对应版本的压缩包。
2. 完整解压整个程序目录，不要只复制 EXE。
3. 运行 `Audio 2 MIDI (CPU).exe`、`Audio 2 MIDI (CUDA).exe` 或 `Audio 2 MIDI (DirectML).exe`。

首次使用某个分离模型时可能需要联网下载。模型会保存在 EXE 同目录的 `models/audio-separator-models` 中。默认已包含 `UVR-MDX-NET-Inst_HQ_5.onnx`。

## 🛠️ 从源码运行

环境要求：

- 64 位 Windows 10 或 Windows 11。
- Python ≤ 3.13.0（预编译 EXE 基于 Python 3.10 打包）。
- 从 [FFmpeg builds 页面](https://www.gyan.dev/ffmpeg/builds/) 下载 FFmpeg full-shared 版本（通常包含 7 个 DLL 和 3 个 EXE），将 `bin` 文件夹复制到要手动运行或构建的版本目录（`cpu/`、`cuda/` 或 `directml/`），再重命名为 `ffmpeg`。
- CUDA 版需要 NVIDIA GPU 和兼容驱动；DirectML 版需要支持 DirectX 12 的 GPU。

### 源码运行

选择一个版本目录，并在目录内创建虚拟环境。

<details>
<summary>使用 Python venv（点击展开）</summary>

以下以 CPU 版为例：

```bat
cd cpu
py -3.10 -m venv .
Scripts\python.exe -m pip install --upgrade pip
Scripts\python.exe -m pip install -r requirements.txt
```

启动源码：

```bat
Scripts\python.exe main.py
```
</details>

或使用 [uv](https://docs.astral.sh/uv/)：

```bat
cd cpu
uv venv
uv pip install -r requirements.txt
uv run main.py
```

`cuda` 和 `directml` 使用相同步骤，但必须安装对应目录中的 `requirements.txt`，不要让三个版本共用同一个虚拟环境。

### 手动构建

准备好虚拟环境、依赖和 `ffmpeg` 目录后，运行构建脚本：

```bat
build.bat
```

输出目录为：

```text
cpu/dist/Audio 2 MIDI (CPU)/
cuda/dist/Audio 2 MIDI (CUDA)/
directml/dist/Audio 2 MIDI (DirectML)/
```

## 📁 仓库结构

```text
Audio-2-MIDI-GitHub/
|-- cpu/                 # CPU 源码、依赖和打包配置
|-- cuda/                # NVIDIA CUDA 源码、依赖和打包配置
|-- directml/            # DirectML 源码、依赖和打包配置
|-- .gitignore
|-- README.md            # English
|-- README.zh-CN.md      # 简体中文
|-- README.ja.md         # 日本語
```

## ⚖️ 第三方软件

本项目使用 Audio Separator、[Basic Pitch](https://github.com/spotify/basic-pitch)、ONNX Runtime、PyTorch、PyQt6 和 FFmpeg。重新发布前，请核对所有依赖、模型、FFmpeg 构建、图标和 Logo 的许可证及署名要求。

## 🐞 问题反馈

提交 Issue 时请注明程序版本、Windows 版本、CPU/GPU 型号、显卡驱动版本，并附上程序日志和复现步骤。请勿上传未经授权的隐私或版权音频。
