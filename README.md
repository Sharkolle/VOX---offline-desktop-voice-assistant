# 🎙️ VOX Voice Assistant
VOX is a robust, privacy-focused, cross-platform voice assistant that seamlessly toggles between **Online** and **completely Offline** operation modes. Built in Python, it integrates offline speech-to-text (STT) via **Faster-Whisper**, custom wake-word detection, offline/online text-to-speech (TTS), and a rich set of system control, productivity, and utility skills.
VOX is equipped with both a sleek command-line terminal interface and an elegant graphical interface featuring dynamic dark/light mode toggles, interactive rounded chat bubbles, and the specialized **SilentNote** memo recorder.
> [!NOTE]
> VOX was created and is actively developed by **Ahmad**, a software developer dedicated to building secure, modular, offline-first assistive tools.
---
## 🌟 Key Features
VOX supports a highly rich ecosystem of commands categorized as follows:
### ⚙️ Core Architecture & Modes
*   **Online Mode**: Transcribes audio using Google Speech Recognition API and synthesizes high-quality audio using Google TTS (`gTTS`) played via `pygame`.
*   **Offline Mode**: Operates completely cut off from the internet. Transcribes audio locally using **Faster-Whisper** (`base.en` / `tiny.en` models running on local CPU) and synthesizes voice using the offline `pyttsx3` engine.
*   **Hands-Free Wake Word**: Continuously sleeps in the background and activates upon hearing "Hey VOX" (supports fuzzy matching against variations like *Hey box*, *Hi fox*, *Hey folks*, etc.).
### 🖥️ System & Media Control
*   **Application Launcher**: Open everyday apps (browser, notepad, file explorer, calculator, recycle bin, system settings) across Windows, macOS, and Linux.
*   **Power Operations**: Safely shutdown, restart, logout, lock, or sleep your computer (with explicit spoken confirmation prompts for destructive actions).
*   **Utility Operations**: Capture screenshots, empty the recycle bin, or run a comprehensive **System Diagnosis** report (covering disk space, memory, and OS details).
*   **Hardware Adjustments**: Toggle Wi-Fi, control Bluetooth, and adjust screen brightness levels.
*   **Media Controller**: Adjust volume up/down, mute the system, or play/pause active media.
### 📅 Productivity & Organization
*   **Reminder Manager**: Schedule reminders using natural temporal parsing (e.g., *"Remind me to meet Ahmad at 4:30 PM"*). VOX checks for due tasks in the background and speaks them aloud. Includes options to list all saved reminders or delete specific ones.
*   **TO-DO List**: Add items to your active list, view current to-dos, remove individual tasks, or clear the entire list.
*   **SilentNote Plugin**: A dedicated note-taking suite. Record high-fidelity audio notes, save them to the `notes/` folder as `.wav` files, and automatically transcribe them locally with offline Whisper. Play back voice recordings directly from the GUI.
*   **Daily Briefing**: Say *"Good morning"* or *"Briefing"* to hear a consolidated report of the current date, active reminders, and a motivational quote.
### 🧠 Memory & Personality
*   **Active User Switching**: Support for multiple profiles with personalized settings (voice rate, volume, and preferences saved to individual JSON databases under `data/`).
*   **Conversation Recall**: Asks VOX to repeat its last response (*"Repeat"*), retrieve your last spoken command (*"What did I say?"*), or output the last 5 conversation rounds in the chat window.
*   **Knowledge Queries**: Integrate Wikipedia search queries (online) to fetch 2-sentence summaries on any concept.
*   **Witty Personality**: A collection of tech-oriented jokes, programming humor, motivational quotes, and clever AI-flavored easter eggs.
---
## 📂 Project Structure
The project is structured modularly to decouple the user interface from the underlying skill implementations:
```filepath
VOX_Assiatant/
├── main_terminal.py         # Entry point for the CLI/Terminal voice loop
├── task_router.py           # The system's central command-matching router
├── core/                    # Engine configurations and service runners
│   ├── config.py            # Global configuration (Online vs. Offline modes)
│   ├── memory.py            # Active profile state & JSON key-value user storage
│   ├── voice_recognition.py # STT pipelines (Google Online API & Faster-Whisper)
│   └── wake_word.py         # Threaded wait loop for wake-word triggers ("Hey VOX")
├── commands/                # Individual skill modules
│   ├── speak.py             # TTS logic (gTTS & pygame / pyttsx3)
│   ├── reminders.py         # Reminders database operations & temporal normalizers
│   ├── system_control.py    # Multi-OS system, volume, brightness, power controls
│   ├── todo.py              # TO-DO list database operations
│   ├── open_app.py          # OS-aware desktop application launching
│   ├── daily_briefing.py    # Consolidated date, reminder, and quotes generator
│   ├── fun_skills.py        # Jokes, motivations, and clever text outputs
│   ├── knowledge.py         # Wikipedia parsing integration
│   ├── conversation_memory.py # History recall mechanisms
│   └── help.py              # Dynamic terminal and voice helper guides
├── gui/                     # Graphical User Interface module
│   ├── main_gui.py          # Entry point for launching the VOX window
│   └── vox_gui.py           # Tkinter canvas, chat bubbles, user picker, and settings
├── plugins/                 # Add-ons and extensions
│   ├── note_mode/
│   │   └── gui.py           # SilentNote window (voice recordings and playback)
│   └── creas/               # Core plugins shared tools
│       ├── live_recorder.py # Low-level audio recording streaming (sounddevice/soundfile)
│       ├── recognizer.py    # Local standalone Whisper transcription
│       ├── settings.py      # Note theme/font configurations
│       └── storage.py       # Local notes text/audio file storage
├── models/                  # Storage directory for local Faster-Whisper models
│   ├── base.en/             # Higher precision Whisper model (CPU execution)
│   └── tiny.en/             # Low-latency, CPU-friendly model for wake word
├── data/                    # User profile JSONs and global reminders config (Git ignored)
└── requirements.txt         # Project package dependencies
```
---
## 🛠️ Technology Stack & Dependencies
VOX is developed on Python 3.10+ and relies on the following libraries:
|
 Library 
|
 Purpose 
|
 Description 
|
|
:---
|
:---
|
:---
|
|
`faster-whisper`
|
 Offline STT 
|
 Fast implementation of OpenAI's Whisper model using CTranslate2. 
|
|
`SpeechRecognition`
|
 Online STT 
|
 Unified API for Google Speech Recognition web services. 
|
|
`pyttsx3`
|
 Offline TTS 
|
 Multi-platform, offline Text-to-Speech library. 
|
|
`gTTS`
|
 Online TTS 
|
 Google Text-to-Speech translator API. 
|
|
`sounddevice`
|
 Audio Streaming 
|
 Recording microphone buffers and real-time audio streams. 
|
|
`soundfile`
|
 Audio Processing 
|
 Reading and writing WAV audio files (used in SilentNote). 
|
|
`pygame`
|
 Audio Playback 
|
 Stream and play online-generated MP3 speech assets safely. 
|
|
`wikipedia`
|
 Knowledge Search
|
 Querying Wikipedia pages and extracting summaries. 
|
|
`pyfiglet`
|
 Terminal Visuals 
|
 Renders the giant retro ASCII startup banner. 
|
|
`numpy`
|
 Data Engineering 
|
 Handles raw microphone audio buffers. 
|
---
## 🚀 Installation & Set Up
Follow these steps to set up VOX locally:
### 1. Prerequisites
Ensure you have **Python 3.10** or higher installed. A working microphone is required for voice operations.
### 2. Clone the Repository
```bash
git clone https://github.com/your-username/VOX_Assiatant.git
cd VOX_Assiatant
```
### 3. Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate
# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
> [!TIP]
> On Windows, to support brightness controls, you can optionally install:
> `pip install screen-brightness-control`
### 5. Download Whisper Models (Offline Mode)
VOX is pre-configured to search for Whisper models in your local `./models/` directory or download them on demand from HuggingFace. By default:
*   `tiny.en` is loaded for low-overhead wake-word monitoring.
*   `base.en` is loaded for highly accurate user command transcription.
---
## 🏃 Running VOX
VOX offers two different execution modes depending on your preference:
### 🖥️ 1. Terminal / CLI Interface
To run the lightweight, retro terminal interface with live log outputs:
```bash
python main_terminal.py
```
VOX will print system diagnostic information, greet you, and start waiting for the wake word:
```text
 _  ______  __  __
| |/ / __ \|  \/  |
| ' / |  | | \  / |
|  <| |  | | |\/| |
|_|\_\______/______
Offline Voice Assistant • OmniGuard Technologies
--------------------------------------------------
VOX system ready. Say 'Hey VOX' when you need me.
VOX is sleeping... Say 'hey vox' to wake me up.
```
### 🎨 2. Modern Graphical UI
To launch the beautiful desktop graphical client featuring a custom chat feed:
```bash
python gui/main_gui.py
```
*   **Push-to-Talk / Hold-to-Talk**: Click and hold the 🎤 microphone button to speak, then release it to send the voice command.
*   **Text Field**: Type your commands directly into the prompt bar and press `Enter`.
*   **Wake Button**: Toggle hands-free voice activation.
*   **Notes (📝)**: Open **SilentNote** to record voice memos, save them, play them back, and view auto-transcribed contents.
*   **Settings (⚙️)**: Toggle between **Online/Offline** modes, select your active user profile, or adjust TTS speech rate and volume.
---
## 🗣️ Supported Voice Commands
You can say or type the following phrases to interact with VOX:
|
 Category 
|
 Example Command 
|
 Expected Response / Action 
|
|
:---
|
:---
|
:---
|
|
**
Daily Routine
**
|
*
"Good morning"
*
|
 Speaks current date, active reminders, and today's motivation. 
|
|
**
System Apps
**
|
*
"Open browser"
*
|
 Opens Google.com in your default web browser. 
|
|
|
*
"Open calculator"
*
|
 Launches your operating system's calculator application. 
|
|
**
Device Control
**
|
*
"Take a screenshot"
*
|
 Captures screen and saves it. 
|
|
|
*
"Increase volume"
*
|
 Turns up master speaker volume by 5%. 
|
|
|
*
"Mute"
*
|
 Mutes system sound output. 
|
|
**
Reminders
**
|
*
"Remind me to feed the cat at 6 PM"
*
|
 Sets an active notification for 6:00 PM. 
|
|
|
*
"What are my reminders?"
*
|
 Lists all upcoming scheduled items. 
|
|
|
*
"Delete reminder to train at 8 PM"
*
|
 Safely filters out the matching task. 
|
|
**
TO-DO List
**
|
*
"Add to my list learn Python"
*
|
 Saves "learn Python" to your profile to-do list. 
|
|
|
*
"Show my list"
*
|
 Displays indexed tasks. 
|
|
**
Memory
**
|
*
"Remember my name is Ahmad"
*
|
 Updates active user name parameter in storage. 
|
|
|
*
"What did I say?"
*
|
 Repeats your last transcribed voice command. 
|
|
**
Online Search
**
|
*
"Search solar system"
*
|
 Runs a quick Wikipedia summary lookup. 
|
|
**
Fun Stuff
**
|
*
"Tell me a joke"
*
|
 Tells a funny tech/programming joke. 
|
|
|
*
"Who created you?"
*
|
 Speaks: 
*
"I have been created by Ahmad..."
*
|
|
**
Power State
**
|
*
"Shutdown system"
*
|
 Prompts for a "yes/no" confirmation, then powers down. 
|

