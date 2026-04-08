import time
import queue
import json
import datetime
import subprocess
import sounddevice as sd
import sys
import random
import soundfile as sf
import re
import requests

from ddgs import DDGS
from TTS.api import TTS
from vosk import Model, KaldiRecognizer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from sumy.summarizers.lsa import LsaSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

# ---------------- CONFIG ----------------
WAKE_WORD = "gecko"
KILL_PHRASE = "gecko stop"

MODEL_PATH = "vosk-model-en-us-0.22"
SAMPLE_RATE = 16000
FIRSTWAKE = True
MUSICPAUSED = False
# ---------------- TTS ----------------

print("Loading TTS model...")
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC",progress_bar=False, gpu=False)

def play_audio(filename):

    # Extract data and sampling rate from file
    data, fs = sf.read(f"./prebuiltphrases/{filename}", dtype='float32')

    # Start playback
    sd.play(data, fs)

    # Wait until the file is done playing
    sd.wait()

    # Optional: Stop playback explicitly if needed
    sd.stop()

def speak(text):
    if not text:
        return

    print("Speaking:", text)

    # Coqui TTS can return audio as a NumPy array
    audio = tts.tts(text)  # default is float32 array
    samplerate = tts.synthesizer.output_sample_rate  # usually 22050

    # Play directly
    sd.play(audio, samplerate)
    sd.wait()  # wait until finished
# ---------------- BROWSER SETUP ----------------
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

options = Options()
options.binary_location = brave_path
options.add_experimental_option("detach", True)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

actions = ActionChains(driver)
   
# ---------------- BROWSER/ASSISTANT FUNCTIONS ----------------

def clean_summary(text):
    # Replace '/' with the word 'slash', then remove or replace other special characters
    text = text.replace("/", "slash")
    # Remove all non-alphanumeric characters except spaces and the word 'slash'
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Optional: replace multiple spaces with a single space and strip
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned   
def summarize_text(text, sentences_count=3):
    text=clean_summary(text)
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count)
    return " ".join(str(sentence) for sentence in summary)
def start_browser():
    options = Options()
    options.binary_location = brave_path
    options.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def check_browser_session():
    global driver
    try:
        driver.current_url
        print("Session is active")
    except Exception:
        print("Session ended. Restarting...")
        driver.quit()
        driver = start_browser()
    

def joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        setup = data["setup"]
        punchline = data["punchline"]
        speak(setup)
        time.sleep(4)
        speak(punchline)
    else:
        dadjokes = [
    "I only know 25 letters of the alphabet. I don't know Y.",
    "I'm on a seafood diet. I see food, and I eat it.",
    "What do you call a fish wearing a bowtie? Sofishticated!",
    "What do you call a can opener that doesn't work? A can't opener.",
    "Why don't scientists trust atoms? Because they make up everything.",
    "Did you hear about the restaurant on the moon? Great food, no atmosphere."
        ]
        speak(random.choice(dadjokes))
        
    
    speak(f"")
def watch_video(data):
    data = data.replace("play", "").strip()
    play_audio("playingvideo.wav")
    speak(data)
    driver.get(f"https://www.youtube.com/results?search_query={data}")
    wait = WebDriverWait(driver, 15)
    first_video = wait.until(EC.element_to_be_clickable((By.ID, "video-title")))
    first_video.click()
    time.sleep(5)

def next_video():
    play_audio("nextvideo.wav")
    actions.key_down(Keys.SHIFT).send_keys("n").key_up(Keys.SHIFT).perform()

def stop_music():
    play_audio("stoppingvideo.wav")
    driver.get("about:blank")

def pause_handler_music():
    global MUSICPAUSED
    if MUSICPAUSED:
        play_audio("pause.wav")
        actions.send_keys("k").perform()
        MUSICPAUSED = False  # toggle play/pause
    else:
        play_audio("unpause.wav")
        actions.send_keys("k").perform()
        MUSICPAUSED = True  # toggle play/pause
def shutdown():
    play_audio("shutdown.wav")
    driver.quit()
    sys.exit(0)

def search(data):
    searchdata = data.replace("search", "").strip()
    speak(f"Searching for {searchdata}")

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(searchdata, max_results=1))
            if results:
                result = results[0]
                text = result['body']
                print(text)
                speak(text)
            else:
                play_audio("noresults.wav")
    except Exception as e:
        print(e)
        play_audio("searchfailed.wav")

def open_program(data):
    programdata = data.replace("open", "").strip().lower()
    programs = {
        "brave": "brave",
        "whatsapp": "whatsapp",
        "settings": "ms-settings:",
        "vscode": "code"
    }

    for name, command in programs.items():
        if name in programdata:
            play_audio("open.wav")
            speak(name)
            subprocess.Popen(["start", command], shell=True)
            return
    speak("Program not found")

# ---------------- MAIN ----------------
def main():
    global FIRSTWAKE
    audio_queue = queue.Queue()

    def callback(indata, frames, time_info, status):
        if status:
            print(status)
        audio_queue.put(bytes(indata))

    play_audio("loadingup.wav")
    print("Loading model...")
    model = Model(MODEL_PATH)

    # Wake word recognizer
    wake_rec = KaldiRecognizer(model, SAMPLE_RATE, f'["{WAKE_WORD}"]')

    # Command recognizer
    cmd_rec = KaldiRecognizer(model, SAMPLE_RATE)

   
    def listen_for_wake():
        while True:
            data = audio_queue.get()
            if wake_rec.AcceptWaveform(data):
                text = json.loads(wake_rec.Result()).get("text", "")
                if WAKE_WORD in text:

                    play_audio("yes.wav")
                    time.sleep(0.3)
                    # 🔥 Clear leftover audio
                    while not audio_queue.empty():
                        audio_queue.get()

                    # 🔥 Reset command recognizer
                    cmd_rec.Reset()

                    return

    def listen_for_command(timeout=8):
        print("🗣️ Listening for command...")
        start_time = time.time()

        while True:
            if time.time() - start_time > timeout:
                print("⌛ Timeout - no command heard")
                return ""
            data = audio_queue.get()
            if cmd_rec.AcceptWaveform(data):
                text = json.loads(cmd_rec.Result()).get("text", "")
                if text:
                    print("Command:", text)
                    return text

    def handle_command(cmd):
        cmd = cmd.lower()
        if KILL_PHRASE in cmd:
            shutdown()
        elif "play" in cmd:
            watch_video(cmd)
        elif "next" in cmd:
            next_video()
        elif "stop" in cmd or "pause" in cmd:
            stop_music()
        elif "time" in cmd:
            now = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {now}")
        elif "open" in cmd:
            open_program(cmd)
        elif "search" in cmd:
            search(cmd)
        elif "joke" in cmd:
            joke()
        else:
            play_audio("notunderstand.wav")

    # 🎤 AUDIO STREAM LOOP
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=callback
    ):
        
        print("🚀 Assistant started")
        """while True:
            try:
                if FIRSTWAKE:
                    play_audio("started.wav")
                    FIRSTWAKE = False
                listen_for_wake()
                command = listen_for_command()
                handle_command(command)
            except KeyboardInterrupt:
                shutdown()
"""
# Running here
if __name__ == "__main__":
    main()
