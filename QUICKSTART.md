# Quick Start Guide

Get started with the Viral Video Clip Generator in just a few steps!

## Installation

### 1. Clone and Setup
```bash
git clone https://github.com/MIHAchoppa/youtube-tool.git
cd youtube-tool
./setup.sh
```

Or manually:
```bash
pip install -r requirements.txt
mkdir -p uploads outputs
cp .env.example .env
```

### 2. Configure API Key
Edit `.env` and add your Groq API key:
```bash
GROQ_API_KEY=your_api_key_here
```

Get your API key from: https://console.groq.com

### 3. Install FFmpeg (if not already installed)
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows - download from https://ffmpeg.org
```

## Usage

### Option 1: Web Interface (Easiest)

1. Start the server:
```bash
python app.py
```

2. Open browser to: http://localhost:5000

3. Follow the interface:
   - Upload your video(s)
   - Paste your transcription with timestamps
   - Click "Analyze & Create"
   - Download your viral compilation!

### Option 2: Command Line

#### Basic Analysis
```bash
python cli.py analyze video.mp4 \
  --transcription example_transcription.txt \
  --output moments.json
```

#### Complete Processing
```bash
python cli.py process video.mp4 \
  --transcription example_transcription.txt \
  --visuals example_visuals.txt \
  --style engaging \
  --output viral.mp4
```

## Transcription Format

Your transcription should have timestamps in this format:

```
[00:00:05] First piece of dialogue
[00:00:15] Something exciting happens
[00:00:25] Amazing reaction here
```

The tool will automatically identify which moments are most viral!

## Example Workflow

### 1. Prepare Your Content
- Have your video file (MP4, MOV, AVI, etc.)
- Create a transcription with timestamps
- Optionally describe visual moments

### 2. Process
Using web interface:
1. Upload video → Wait for success message
2. Paste transcription → Fill in the text area
3. Select style → Choose "Engaging", "Dramatic", or "Casual"
4. Click "Analyze & Create" → Wait for processing
5. Download → Get your viral compilation!

Using CLI:
```bash
python cli.py process myvideo.mp4 \
  --transcription transcript.txt \
  --output myviral.mp4
```

### 3. Result
You'll get a compiled video with:
- ✂️ Best viral moments extracted
- 🎬 Smooth transitions between clips
- 📝 Engaging on-screen text
- 🎙️ AI-generated narration (optional)
- 🎨 Professional editing

## Tips for Best Results

### Transcriptions
- Include all important dialogue and reactions
- Add timestamps every 5-10 seconds for precision
- Mark moments with high energy or emotion

### Visual Descriptions
- Describe significant visual changes
- Note camera movements and effects
- Highlight surprising or dramatic moments

### Choosing Style
- **Engaging**: Upbeat, positive, energetic (best for tutorials, reactions)
- **Dramatic**: Intense, suspenseful (best for reveals, transformations)
- **Casual**: Friendly, conversational (best for vlogs, casual content)

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "FFmpeg not found"
Install FFmpeg for your system (see Installation step 3)

### "API key error"
Make sure you've:
1. Created `.env` file
2. Added `GROQ_API_KEY=your_key`
3. Restarted the application

### Video processing is slow
- Large videos take time to process
- Process one video at a time initially
- Consider reducing video resolution before upload

### Text overlay errors
Install system fonts or modify `video_editor.py` to use available fonts

## What Gets Created

After processing, you'll find:

```
outputs/
├── viral_compilation.mp4      # Your final video
├── final_viral_compilation.mp4  # With TTS audio
└── tts_audio.mp3              # Generated narration
```

## Advanced Usage

### Batch Processing
Process multiple videos:
```bash
for video in *.mp4; do
  python cli.py process "$video" \
    --transcription "${video%.mp4}.txt" \
    --output "viral_${video}"
done
```

### Custom API Integration
```python
from viral_analyzer import ViralMomentAnalyzer
from video_editor import ViralVideoEditor

# Analyze
analyzer = ViralMomentAnalyzer()
moments = analyzer.analyze_transcription(transcription, visuals)

# Edit
editor = ViralVideoEditor()
output = editor.create_viral_compilation(video_path, moments, overlays)
```

### REST API
See `API.md` for complete REST API documentation.

## Need Help?

- 📖 Full docs: `README.md`
- 🔌 API docs: `API.md`
- 💬 Issues: https://github.com/MIHAchoppa/youtube-tool/issues
- 📧 Contact: [Your contact]

## Next Steps

1. ✅ Get it working with the example files
2. 🎬 Try with your own videos
3. 🚀 Share your viral compilations!
4. ⭐ Star the repo if you find it useful

Happy editing! 🎥✨
