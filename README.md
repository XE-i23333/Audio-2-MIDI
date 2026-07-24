# Basic-Pitch-GUI 🎶➡️🎹Audio to MIDI converter powered by Basic Pitch, perfect for VOCALOID and etc.


Run locally, convert audio to MIDI with ease!  
Powered by [Basic Pitch](https://github.com/spotify/basic-pitch), this project offers a friendly GUI + CLI for pitch detection and conversion — no internet required.


---


## ✨ Features
- 🖥️ **GUI + CLI** modes for all users
- 🎵 **Audio → MIDI conversion** (supports vocals & instruments in **.mp3 & .ogg & .wav & .flac & .m4a** format)
- ⚙️ **Adjustable advanced parameters**:
  - Onset threshold  
  - Frame threshold  
  - Minimum note length  
  - Frequency range
- 🌐 **Multilingual UI**: English / 中文 / 日本語
- 💾 **Persistent settings** saved in `settings.ini`
- 📦 **Standalone exe** for Windows
- ⚡ **For now, only CPU is supported**


---


## 🎯 Use Cases
- 🎤 Vocaloid production workflows  
- 🎼 Music composition & arrangement  
- 🎹 Music production and DAW integration  
- 📚 Learning transcription & pitch analysis  


---


## 📸 Screenshots


### v0.4.0
![v0.4.0 Screenshot](/v0.4.0_screenshot.png)




## 🚀 Getting Started


<details open>
<summary>🛠️ Run from Source</summary>


1. Clone the repo:
   ```
   git clone https://github.com/charles23333333/basic-pitch-gui.git
   cd basic-pitch-gui
   ```
👉 uv is recommended for installation and running in venv.


**Create venv (Optional)**


👉 Python ≤ 3.13.0 is required, and the pre‑build exe is packaged with Python 3.10




2. Install dependencies
> Use uv venv
```
uv pip install -r requirements.txt
```
> Or use traditional python
```
pip install -r requirements.txt
```
❗Note:
You must ensure the version of setuptools is below 82.0.0, or you'll receive an error:


`ModuleNotFoundError: No module named 'pkg_resources' `


3.Run!


Run GUI:
> Use uv venv
```
uv run gui.py
```
> Or use traditional python
```
python gui.py
```


Run CLI:
> Use uv venv
```
uv run cli.py input.wav -o output_dir
```
> Or use traditional python
```
python cli.py input.wav -o output_dir
```
</details>


<details>
<summary>📦 Prebuilt Executable</summary>


👉 You can also use the prebuilt exe for one‑click run, available from the Release section.


Just download the latest .exe from Releases.


Double‑click to run — no Python environment required.
</details>
