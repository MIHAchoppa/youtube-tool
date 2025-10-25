# Workflow Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Viral Video Clip Generator                │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐        ┌──────────────┐
│  Web UI      │         │   CLI Tool   │        │   REST API   │
│  (Browser)   │         │  (Terminal)  │        │   (Client)   │
└──────┬───────┘         └──────┬───────┘        └──────┬───────┘
       │                        │                       │
       └────────────────────────┼───────────────────────┘
                                │
                    ┌───────────▼────────────┐
                    │   Flask Application    │
                    │       (app.py)         │
                    └───────────┬────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
┌───────▼────────┐  ┌──────────▼──────────┐  ┌────────▼──────┐
│ Viral Analyzer │  │   Video Editor      │  │ TTS Generator │
│ (Groq AI)      │  │   (MoviePy)         │  │ (Play AI)     │
└───────┬────────┘  └──────────┬──────────┘  └────────┬──────┘
        │                      │                       │
        └──────────────────────┼───────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Output Directory   │
                    │  (Viral Videos)     │
                    └─────────────────────┘
```

## Processing Pipeline

```
1. INPUT
   ┌─────────────┐
   │ Video Files │  (up to 5 videos, MP4/MOV/AVI/etc)
   └──────┬──────┘
          │
   ┌──────▼──────────┐
   │ Transcription   │  (with timestamps [HH:MM:SS])
   └──────┬──────────┘
          │
   ┌──────▼──────────┐
   │ Visual Desc.    │  (optional, with timestamps)
   └──────┬──────────┘
          │
          ▼

2. ANALYSIS (Groq AI)
   ┌─────────────────────────────┐
   │  ViralMomentAnalyzer        │
   │  - Parse transcription      │
   │  - Analyze with Groq LLM    │
   │  - Score viral potential    │
   │  - Identify moments         │
   └──────────┬──────────────────┘
              │
      ┌───────▼────────┐
      │ Viral Moments  │
      │ - Timestamps   │
      │ - Scores       │
      │ - Reasons      │
      │ - Hooks        │
      └───────┬────────┘
              │
              ▼

3. CONTENT GENERATION (Groq AI)
   ┌─────────────────────────────┐
   │  Generate On-Screen Text    │
   │  - Analyze each moment      │
   │  - Create punchy text       │
   │  - Timing & positioning     │
   └──────────┬──────────────────┘
              │
   ┌──────────▼──────────────────┐
   │  Generate TTS Script        │
   │  - Compile moment summary   │
   │  - Create narration         │
   │  - Match style (engaging/   │
   │    dramatic/casual)         │
   └──────────┬──────────────────┘
              │
              ▼

4. VIDEO PROCESSING (MoviePy)
   ┌─────────────────────────────┐
   │  ViralVideoEditor           │
   │  Step 1: Extract Clips      │
   │  - Cut each viral moment    │
   │  - Save temp clips          │
   └──────────┬──────────────────┘
              │
   ┌──────────▼──────────────────┐
   │  Step 2: Add Text Overlays  │
   │  - Apply on-screen text     │
   │  - Position & timing        │
   │  - Fade effects             │
   └──────────┬──────────────────┘
              │
   ┌──────────▼──────────────────┐
   │  Step 3: Add Transitions    │
   │  - Fade in/out              │
   │  - Smooth cuts              │
   └──────────┬──────────────────┘
              │
   ┌──────────▼──────────────────┐
   │  Step 4: Compile Clips      │
   │  - Concatenate moments      │
   │  - Create base compilation  │
   └──────────┬──────────────────┘
              │
              ▼

5. AUDIO PROCESSING (TTS)
   ┌─────────────────────────────┐
   │  TTSGenerator               │
   │  - Generate TTS audio       │
   │  - Save audio file          │
   └──────────┬──────────────────┘
              │
   ┌──────────▼──────────────────┐
   │  Audio Mixing               │
   │  - Reduce original volume   │
   │  - Add TTS narration        │
   │  - Balance audio levels     │
   └──────────┬──────────────────┘
              │
              ▼

6. OUTPUT
   ┌─────────────────────────────┐
   │  Final Viral Compilation    │
   │  ✅ Viral moments extracted │
   │  ✅ Engaging text overlays  │
   │  ✅ Smooth transitions      │
   │  ✅ TTS narration           │
   │  ✅ Ready to share!         │
   └─────────────────────────────┘
```

## Data Flow

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Upload  │────▶│  Analyze │────▶│ Generate │
│  Videos  │     │  Moments │     │ Content  │
└──────────┘     └──────────┘     └──────────┘
                      │                 │
                      │   ┌─────────────┘
                      │   │
                      ▼   ▼
                 ┌──────────┐     ┌──────────┐
                 │   Edit   │────▶│  Export  │
                 │  Videos  │     │  Result  │
                 └──────────┘     └──────────┘
```

## Module Interactions

```
app.py (Flask)
    │
    ├──▶ viral_analyzer.py
    │       └──▶ Groq API (llama-3.2-90b-text-preview)
    │
    ├──▶ video_editor.py
    │       └──▶ MoviePy (FFmpeg)
    │
    └──▶ tts_generator.py
            └──▶ Groq Play AI / FFmpeg
```

## File Structure

```
youtube-tool/
│
├── Core Modules
│   ├── app.py                  # Flask web server
│   ├── viral_analyzer.py       # AI analysis engine
│   ├── video_editor.py         # Video processing
│   └── tts_generator.py        # TTS generation
│
├── Interface
│   ├── cli.py                  # Command-line tool
│   └── templates/
│       └── index.html          # Web UI
│
├── Configuration
│   ├── requirements.txt        # Dependencies
│   ├── .env.example           # Environment template
│   └── .gitignore             # Git ignore rules
│
├── Documentation
│   ├── README.md              # Main documentation
│   ├── QUICKSTART.md          # Quick start guide
│   ├── API.md                 # API reference
│   └── WORKFLOW.md            # This file
│
├── Setup & Testing
│   ├── setup.sh               # Setup script
│   └── test_basic.py          # Basic tests
│
├── Examples
│   ├── example_transcription.txt
│   └── example_visuals.txt
│
└── Runtime Directories (created automatically)
    ├── uploads/               # Uploaded videos
    └── outputs/               # Generated compilations
```

## Technology Stack

```
┌─────────────────────────────────────┐
│         Frontend (Web UI)           │
│  HTML5, CSS3, Vanilla JavaScript    │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│         Backend (Flask)             │
│  Python 3.8+, Flask 3.0             │
└─────────────┬───────────────────────┘
              │
    ┌─────────┼─────────┐
    │         │         │
┌───▼───┐ ┌──▼──┐ ┌────▼────┐
│ Groq  │ │Video│ │ FFmpeg  │
│  AI   │ │Py   │ │         │
└───────┘ └─────┘ └─────────┘
```

## Key Features by Module

### viral_analyzer.py
- ✨ AI-powered moment identification
- 📊 Virality scoring (0-100)
- 📝 TTS script generation
- 🎯 On-screen text suggestions
- 🎪 Hook generation

### video_editor.py
- ✂️ Precision clip extraction
- 🎬 Video compilation
- 📝 Text overlay rendering
- 🎨 Transition effects
- 🔊 Audio mixing

### tts_generator.py
- 🎙️ TTS audio generation
- 🔊 Audio file creation
- 🎵 Voice customization ready
- 🔌 Groq Play AI integration ready

### app.py
- 🌐 RESTful API
- 📤 Multi-file upload
- 🔄 Complete workflow orchestration
- 📥 File download handling
- ✅ Health monitoring
