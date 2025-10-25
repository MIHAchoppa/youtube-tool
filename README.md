# Viral Video Clip Generator 🎬

A powerful tool that analyzes video transcriptions using Groq AI to identify viral moments, then automatically creates engaging compilations with transitions, on-screen text, and TTS narration.

## Features ✨

- **Multi-Video Upload**: Upload up to 5 videos at once for processing
- **AI-Powered Analysis**: Uses Groq's reasoning models to identify the most viral moments
- **Smart Video Editing**: Automatically cuts and compiles clips from identified moments
- **Text Overlays**: Generates and adds engaging on-screen text
- **TTS Integration**: Creates narration scripts and generates TTS audio using Groq Play AI
- **Professional Transitions**: Adds smooth fade transitions between clips
- **Web Interface**: User-friendly Flask web application
- **CLI Tool**: Command-line interface for batch processing

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/MIHAchoppa/youtube-tool.git
cd youtube-tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Groq API key:
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

4. Install FFmpeg (required for video processing):
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

## Usage 📖

### Web Interface

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser to `http://localhost:5000`

3. Follow the workflow:
   - Upload video files (up to 5)
   - Provide transcription with timestamps
   - Add visual descriptions (optional)
   - Select TTS narration style
   - Click "Analyze & Create Viral Compilation"
   - Download your viral video!

### Command Line Interface

#### Analyze a Video
```bash
python cli.py analyze video.mp4 --transcription transcript.txt --output moments.json
```

#### Complete Processing Workflow
```bash
python cli.py process video.mp4 \
  --transcription transcript.txt \
  --visuals visuals.txt \
  --style dramatic \
  --output viral_compilation.mp4
```

#### Generate TTS Script Only
```bash
python cli.py tts --moments moments.json --style engaging --output script.txt
```

#### Compile Clips from Moments
```bash
python cli.py compile video.mp4 --moments moments.json --output compilation.mp4
```

## Transcription Format 📝

Provide transcriptions with timestamps in the following format:

```
[00:00:05] Welcome to this amazing video
[00:00:15] Today we're going to show you something incredible
[00:00:30] Watch what happens next...
[00:01:00] This is the moment you've been waiting for
```

Visual descriptions follow the same format:

```
[00:00:05] Camera zooms in dramatically
[00:00:15] Bright lighting emphasizes the subject
[00:00:30] Unexpected visual effect appears
[00:01:00] Close-up reaction shot
```

## API Endpoints 🔌

### POST /upload
Upload video files (max 5).

**Request**: `multipart/form-data` with `videos` field

**Response**:
```json
{
  "success": true,
  "message": "3 videos uploaded successfully",
  "files": [{"filename": "video1.mp4", "path": "uploads/video1.mp4"}]
}
```

### POST /analyze
Analyze video for viral moments.

**Request**:
```json
{
  "video_path": "uploads/video.mp4",
  "transcription": "[00:00:05] text...",
  "visuals_description": "[00:00:05] visual..."
}
```

**Response**:
```json
{
  "success": true,
  "viral_moments": [
    {
      "start_time": 10.5,
      "end_time": 25.3,
      "score": 95,
      "reason": "High energy reaction with visual impact",
      "hook": "Watch what happens next!"
    }
  ]
}
```

### POST /generate-tts
Generate TTS script from viral moments.

**Request**:
```json
{
  "viral_moments": [...],
  "style": "engaging"
}
```

### POST /process-complete
Process complete workflow (recommended).

**Request**:
```json
{
  "video_path": "uploads/video.mp4",
  "transcription": "[00:00:05] text...",
  "visuals_description": "[00:00:05] visual...",
  "tts_style": "engaging",
  "output_name": "viral_compilation.mp4"
}
```

### GET /download/<filename>
Download generated video file.

## Architecture 🏗️

### Components

- **viral_analyzer.py**: Groq AI integration for identifying viral moments and generating content
- **video_editor.py**: Video processing using MoviePy for cutting, compiling, and effects
- **tts_generator.py**: Text-to-speech generation (Groq Play AI integration ready)
- **app.py**: Flask web application with REST API
- **cli.py**: Command-line interface
- **templates/index.html**: Web UI

### Workflow

1. **Upload**: Videos uploaded to `uploads/` directory
2. **Analysis**: Groq AI analyzes transcription to identify viral moments
3. **Text Generation**: AI generates on-screen text overlays
4. **TTS Script**: AI creates engaging narration script
5. **TTS Audio**: Text-to-speech audio generated (placeholder for Groq Play AI)
6. **Video Editing**: Clips extracted, text overlays added, transitions applied
7. **Compilation**: Clips combined into final video
8. **Audio Mixing**: TTS narration mixed with original audio
9. **Output**: Final video saved to `outputs/` directory

## Configuration ⚙️

Environment variables (`.env`):

```bash
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_flask_secret_key  # Optional, for production
```

Application settings in `app.py`:
- `MAX_CONTENT_LENGTH`: 500MB (max file size)
- `ALLOWED_EXTENSIONS`: mp4, avi, mov, mkv, webm
- Max videos per upload: 5

## Requirements 📦

- Python 3.8+
- Flask 3.0.0
- MoviePy 1.0.3
- Groq 0.4.1
- FFmpeg (system requirement)
- See `requirements.txt` for full list

## Examples 💡

### Example Transcription

```text
[00:00:00] Hey everyone, welcome back to the channel
[00:00:05] Today I'm going to show you something absolutely insane
[00:00:12] You won't believe what happens next
[00:00:18] Watch closely as I demonstrate this technique
[00:00:25] BOOM! Did you see that?
[00:00:30] That's how you do it, incredible right?
[00:00:38] Let me show you one more time in slow motion
[00:00:45] This is why it works so well
[00:00:52] And that's it! Make sure to like and subscribe
```

### Example Output

The tool will:
1. Identify top 3-5 viral moments (e.g., "BOOM! Did you see that?" at 00:00:25)
2. Extract those specific segments
3. Add text like "WAIT FOR IT..." and "🔥 INCREDIBLE!"
4. Generate TTS narration: "You won't believe what you're about to see..."
5. Add smooth fade transitions
6. Combine into a 30-60 second viral-ready clip

## Development 🛠️

### Project Structure
```
youtube-tool/
├── app.py                 # Flask web application
├── cli.py                 # Command-line interface
├── viral_analyzer.py      # AI analysis module
├── video_editor.py        # Video editing module
├── tts_generator.py       # TTS generation module
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── templates/
│   └── index.html        # Web UI
├── uploads/              # Uploaded videos (created automatically)
└── outputs/              # Generated videos (created automatically)
```

### Running Tests
```bash
# TODO: Add test suite
python -m pytest tests/
```

## Limitations & Notes ⚠️

1. **TTS Audio**: Currently uses a placeholder implementation. Update `tts_generator.py` with actual Groq Play AI integration when available.

2. **Text Rendering**: Requires fonts to be installed on the system. Default uses Arial.

3. **Processing Time**: Large videos may take several minutes to process depending on:
   - Video size and duration
   - Number of viral moments
   - System hardware

4. **Memory Usage**: Processing multiple large videos simultaneously may require significant RAM.

## Troubleshooting 🔧

### FFmpeg not found
Install FFmpeg on your system (see Installation section).

### Text overlay errors
Install required fonts or modify `video_editor.py` to use system-available fonts.

### Memory errors
Process videos one at a time or reduce video quality before upload.

### API errors
Ensure `GROQ_API_KEY` is properly set in `.env` file.

## Contributing 🤝

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License 📄

MIT License - see LICENSE file for details

## Acknowledgments 🙏

- Groq AI for powerful reasoning models
- MoviePy for video processing
- Flask for web framework

## Support 💬

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [Your contact information]

---

Made with ❤️ for creating viral content