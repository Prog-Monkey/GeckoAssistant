Gecko Voice Assistant 🤖

Gecko is a Python-based voice assistant that responds to a wake word, executes commands like playing YouTube videos, telling jokes, opening programs, performing searches, and more.

By default, it uses Brave Browser for ad-blocking and privacy, but you can edit the code to work with any browser you like.

Features
Wake word detection (gecko)
Commands for:
Playing YouTube videos
Pausing, stopping, or skipping videos
Telling the time
Opening programs (Brave, WhatsApp, VS Code, Settings)
Performing web searches
Telling jokes
Text-to-Speech (Coqui TTS) for audio responses
Browser automation using Selenium
Summarization using sumy
Setup
Use Python 3.10
Coqui TTS is not compatible with Python 3.11+, so make sure your environment uses Python 3.10.
Clone the repository:
git clone <repo_url>
cd EchoAssistant
Install Python dependencies:
pip install -r requirements.txt
Download Vosk model:
Get the English Vosk model (vosk-model-en-us-0.22) from Vosk Models
 and place it in the project folder.
Update browser path if needed:
Brave is default, but you can change the path in main.py to use your favorite browser.
Ensure prebuilt audio files exist:
Audio prompts like "yes.wav" or "playingvideo.wav" must be in ./prebuiltphrases/.
Usage

Run the assistant with:

python main.py
Say "gecko" to wake the assistant.
Speak a command within ~8 seconds after wake.

Example commands:

"play [video name]" → Plays a YouTube video
"next" → Skips to the next video
"stop" → Stops the video
"open brave" → Opens Brave browser
"search [query]" → Performs a web search
"joke" → Tells a joke
"gecko stop" → Shuts down the assistant
Folder Structure
EchoAssistant/
│
├─ prebuiltphrases/         # Prebuilt audio prompts (tracked in Git)
├─ vosk-model-en-us-0.22/   # Vosk speech recognition model (ignored in Git)
├─ chromedriver/            # Chrome/Brave driver (ignored in Git)
├─ main.py                  # Main assistant script
├─ requirements.txt
└─ README.md
Notes & Disclaimer
Works best with a microphone and speaker.
Brave is used by default for privacy/ad-blocking, but any browser can be used.
TTS uses CPU by default; GPU setup is optional.
Internet is required for YouTube and search commands.
⚠️ Use only trusted sources when opening links or running programs.
