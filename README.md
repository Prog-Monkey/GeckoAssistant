# 🚀 **GECKO VOICE ASSISTANT** 🚀

**The Ultimate AI-Powered Voice Companion**

---

Gecko is a **blazingly fast** Python-based voice assistant that responds to a wake word, executes commands like playing YouTube videos, telling jokes, opening programs, performing searches, and **much more**!

By default, it uses **Brave Browser** for ad-blocking and privacy, but you can edit the code to work with any browser you like.

---

## ✨ **AWESOME FEATURES** ✨

### 🎯 **Core Capabilities**
- **🔊 Wake word detection** (just say "gecko"!)
- **▶️ YouTube Integration** - Play, pause, skip videos at your command
- **⏰ Time Announcements** - Always know what time it is
- **🔗 Program Launcher** - Open Brave, WhatsApp, VS Code, Settings with voice
- **🔍 Web Search** - Search the internet hands-free
- **😂 Joke Generator** - Need a laugh? Gecko's got you!
- **🗣️ Text-to-Speech** - **Crystal clear** audio responses using Coqui TTS
- **🤖 Browser Automation** - Powered by Selenium
- **📝 Summarization** - Intelligent content summarization using sumy

---

## 🛠️ **SETUP INSTRUCTIONS**

### **Step 1: Python Version**
⚠️ **IMPORTANT**: Use **Python 3.10**
- Coqui TTS is not compatible with Python 3.11+, so make sure your environment uses Python 3.10.

### **Step 2: Clone the Repository**
```bash
git clone <repo_url>
cd EchoAssistant
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Download Vosk Model**
- Get the **English Vosk model (vosk-model-en-us-0.22)** from [Vosk Models](https://alphacephei.com/vosk/models)
- Place it in the project folder

### **Step 5: Configure Browser Path**
- **Brave is default**, but you can change the path in `main.py` to use your favorite browser

### **Step 6: Audio Files**
- Ensure prebuilt audio files exist in `./prebuiltphrases/`
- Examples: `yes.wav`, `playingvideo.wav`

---

## 🎤 **USAGE GUIDE**

### **Get Started**
```bash
python main.py
```

### **Voice Commands** 🗣️
1. Say **"gecko"** to wake the assistant
2. Speak a command within ~8 seconds
3. Watch the magic happen! ✨

### **Command Examples** 💡
| Command | Action |
|---------|--------|
| **"play [video name]"** | Plays a YouTube video |
| **"next"** | Skips to the next video |
| **"stop"** | Stops the video |
| **"open brave"** | Opens Brave browser |
| **"search [query]"** | Performs a web search |
| **"joke"** | Tells a joke |
| **"gecko stop"** | Shuts down the assistant |

---

## 📁 **PROJECT STRUCTURE**

```
EchoAssistant/
│
├─ prebuiltphrases/         # 🔊 Prebuilt audio prompts
├─ vosk-model-en-us-0.22/   # 🧠 Speech recognition model
├─ chromedriver/            # 🚗 Browser driver
├─ main.py                  # ⭐ Main assistant script
├─ requirements.txt         # 📦 Dependencies
└─ README.md                # 📖 You are here!
```

---

## ⚡ **NOTES & DISCLAIMER**

- **🎧 Microphone & Speaker Required** - Works best with quality audio hardware
- **🌐 Internet Required** - Needed for YouTube, searches, and voice features
- **🔒 Privacy First** - Brave Browser is default for ad-blocking & privacy
- **⚙️ GPU Optional** - TTS uses CPU by default; GPU setup is optional
- **⚠️ Security Notice** - Use only **trusted sources** when opening links or running programs

---

**Made with ❤️ by the Gecko Team**