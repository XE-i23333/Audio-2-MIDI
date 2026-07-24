# Audio 2 MIDI

<p align="center">
  <img src="cpu/logo.png" alt="Audio 2 MIDI" width="720">
</p>

<p align="center">
  <a href="README.md">English</a> | <strong>简体中文</strong> | <a href="README.ja.md">日本語</a>
</p>

Audio 2 MIDI 是一个 Windows 桌面音频处理工具，结合 Audio Separator 与 Basic Pitch，支持音轨分离、音频转 MIDI、音符 CSV 导出和 MIDI 音频预览。仓库提供 CPU、NVIDIA CUDA 和 DirectML 三个版本。

## ✨ 功能

- 分离人声或伴奏音轨。
- 将原始音频或分离后的音轨转换为 MIDI。
- 导出 MIDI、音符 CSV、Basic Pitch 模型输出 NPZ 和 MIDI 音频预览 WAV。
- 调整起始阈值、帧阈值、最短音符长度、频率范围及相邻音符合并时间。
- 支持 WAV、MP3、OGG、FLAC 和 M4A。
- 提供简体中文、English 和日本語界面。
- 查看实时进度、处理速度和运行日志。

本版本的 Basic Pitch 默认起始阈值为 `0`，Merge Notes 默认值为 `50 ms`。

> 💡 **UVR-MDX-NET-Inst HQ 5** 分离效果最好，推荐优先选择。

<p align="center">
  <img src="screenshot.jpg" alt="Audio 2 MIDI 截图" width="720">
</p>

## 🚀 版本选择

| 版本 | 适用设备 | 推理后端 | 已验证成品体积 |
| --- | --- | --- | ---: |
| CPU | 无可用 GPU，或追求最高兼容性 | ONNX Runtime CPU | 约 1.38 GB |
| CUDA | NVIDIA GPU | CUDA 12.4 (cu124) | 约 5.82 GB |
| DirectML | AMD、Intel 或 NVIDIA GPU | DirectML / DML Execution Provider | 约 2.04 GB |

CUDA 版至少需要 CUDA 12.4 的 NVIDIA 驱动。DirectML 版需要 Windows 10/11、DirectX 12 支持和较新的显卡驱动。不确定设备是否兼容时建议使用 CPU 版。

## 📦 下载和运行

普通用户应从仓库的 **GitHub Releases** 页面下载程序，不要下载自动生成的 Source code 压缩包。

1. 下载对应版本的完整压缩包或全部分卷。
2. 如果是分卷，将所有分卷放在同一目录，并从 `.7z.001` 开始解压。
3. 完整解压整个程序目录，不要只复制 EXE。
4. 运行 `Audio 2 MIDI (CPU).exe`、`Audio 2 MIDI (CUDA).exe` 或 `Audio 2 MIDI (DirectML).exe`。

首次使用某个分离模型时可能需要联网下载。模型会保存在 EXE 同目录的 `models/audio-separator-models` 中。默认已包含 `UVR-MDX-NET-Inst_HQ_5.onnx`。

## 🛠️ 从源码运行

环境要求：

- 64 位 Windows 10 或 Windows 11。
- 64 位 Python 3.10。
- 已自带 FFmpeg，无需配置环境变量。
- CUDA 版需要 NVIDIA GPU 和兼容驱动；DirectML 版需要支持 DirectX 12 的 GPU。

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

## 🏗️ 构建 Windows 成品

准备好虚拟环境、依赖和 `ffmpeg` 目录后，在对应版本目录运行：

```bat
build.bat
```

输出目录为：

```text
cpu/dist/Audio 2 MIDI (CPU)/
cuda/dist/Audio 2 MIDI (CUDA)/
directml/dist/Audio 2 MIDI (DirectML)/
```

脚本会将 `icon.ico` 复制到 EXE 同目录。发布时必须压缩并上传完整成品目录，因为 `_internal`、FFmpeg、运行库和资源文件都不可缺少。

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
`-- RELEASENOTE.md
```

## 🌐 GitHub 发布

源码提交到仓库，打包成品上传到 GitHub Releases。不要提交虚拟环境、`build`、`dist`、FFmpeg 二进制文件、下载模型、本地设置或测试音频。

CUDA 成品无法作为单个 GitHub Release 文件上传，DirectML 成品也接近限制，建议创建 1900 MB 的 7-Zip 分卷：

```bat
7z a -t7z -mx=9 -v1900m "Audio-2-MIDI-CUDA-v0.1.0.7z" "cuda\dist\Audio 2 MIDI (CUDA)\*"
```

CPU 版通常可以上传单个压缩包。应用程序成品应使用 GitHub Releases 发布，不建议放入 Git LFS。

## ✅ 验证状态

三个版本均已通过依赖检查、GUI 创建、实际 Basic Pitch 转录、Audio Separator 分离、PyInstaller 构建和成品启动检查。确认使用的后端分别为 `CPUExecutionProvider`、`CUDAExecutionProvider` 和 `DmlExecutionProvider`。

## ⚖️ 第三方软件

本项目使用 Audio Separator、Basic Pitch、ONNX Runtime、PyTorch、PyQt6 和 FFmpeg。重新发布前，请核对所有依赖、模型、FFmpeg 构建、图标和 Logo 的许可证及署名要求。

## 🐞 问题反馈

提交 Issue 时请注明程序版本、Windows 版本、CPU/GPU 型号、显卡驱动版本，并附上程序日志和复现步骤。请勿上传未经授权的隐私或版权音频。
