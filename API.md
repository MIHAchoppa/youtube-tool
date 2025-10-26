# API Documentation

## Overview

The Viral Video Clip Generator provides a RESTful API for processing videos and creating viral compilations.

Base URL: `http://localhost:5000`

## Authentication

Currently, no authentication is required for the API. In production, implement API key or OAuth authentication.

## Endpoints

### Health Check

**GET** `/health`

Check if the service is running.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Upload Videos

**POST** `/upload`

Upload video files for processing (maximum 5 videos).

**Request:**
- Content-Type: `multipart/form-data`
- Field name: `videos` (can be multiple files)

**Supported formats:** MP4, AVI, MOV, MKV, WEBM

**Response:**
```json
{
  "success": true,
  "message": "3 videos uploaded successfully",
  "files": [
    {
      "filename": "video1.mp4",
      "path": "uploads/video1.mp4"
    },
    {
      "filename": "video2.mp4",
      "path": "uploads/video2.mp4"
    }
  ]
}
```

**Error Response:**
```json
{
  "error": "Maximum 5 videos allowed"
}
```

---

### Analyze Video

**POST** `/analyze`

Analyze video transcription to identify viral moments using Groq AI.

**Request:**
```json
{
  "video_path": "uploads/video.mp4",
  "transcription": "[00:00:05] Welcome to the video\n[00:00:15] This is amazing\n[00:00:30] Watch this moment",
  "visuals_description": "[00:00:05] Camera zooms in\n[00:00:15] Bright lighting\n[00:00:30] Dramatic effect"
}
```

**Response:**
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
    },
    {
      "start_time": 45.0,
      "end_time": 58.2,
      "score": 88,
      "reason": "Surprising reveal with emotional response",
      "hook": "You won't believe this!"
    }
  ]
}
```

---

### Generate TTS Script

**POST** `/generate-tts`

Generate a text-to-speech script for viral moments.

**Request:**
```json
{
  "viral_moments": [
    {
      "start_time": 10.5,
      "end_time": 25.3,
      "score": 95,
      "reason": "High energy reaction"
    }
  ],
  "style": "engaging"
}
```

**Styles:** `engaging`, `dramatic`, `casual`

**Response:**
```json
{
  "success": true,
  "script": "Get ready for the most incredible moments you've ever seen! Watch as these jaw-dropping scenes unfold before your eyes. This is content you don't want to miss!"
}
```

---

### Generate Text Overlays

**POST** `/generate-text-overlays`

Generate on-screen text suggestions for viral moments.

**Request:**
```json
{
  "viral_moments": [
    {
      "start_time": 10.5,
      "end_time": 25.3,
      "score": 95,
      "reason": "High energy reaction",
      "hook": "Watch this!"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "text_overlays": [
    [
      {
        "text": "WAIT FOR IT...",
        "delay": 0,
        "duration": 2.0,
        "position": "top"
      },
      {
        "text": "🔥 INCREDIBLE!",
        "delay": 3.0,
        "duration": 2.5,
        "position": "center"
      }
    ]
  ]
}
```

**Positions:** `top`, `center`, `bottom`

---

### Compile Video

**POST** `/compile`

Compile viral clips with transitions and text overlays.

**Request:**
```json
{
  "video_path": "uploads/video.mp4",
  "viral_moments": [
    {
      "start_time": 10.5,
      "end_time": 25.3,
      "score": 95,
      "reason": "High energy reaction"
    }
  ],
  "text_overlays": [
    [
      {
        "text": "AMAZING!",
        "delay": 0,
        "duration": 2.0,
        "position": "top"
      }
    ]
  ],
  "tts_audio_path": "outputs/tts_audio.mp3",
  "output_name": "viral_compilation.mp4"
}
```

**Response:**
```json
{
  "success": true,
  "output_path": "outputs/final_viral_compilation.mp4",
  "download_url": "/download/final_viral_compilation.mp4"
}
```

---

### Process Complete Workflow

**POST** `/process-complete`

Execute the complete workflow: analyze, generate TTS, add text overlays, and compile.

**Request:**
```json
{
  "video_path": "uploads/video.mp4",
  "transcription": "[00:00:05] Welcome...\n[00:00:15] Amazing content...",
  "visuals_description": "[00:00:05] Zoom in...\n[00:00:15] Dramatic lighting...",
  "tts_style": "engaging",
  "output_name": "viral_compilation.mp4"
}
```

**Response:**
```json
{
  "success": true,
  "viral_moments": [
    {
      "start_time": 10.5,
      "end_time": 25.3,
      "score": 95,
      "reason": "High energy reaction",
      "hook": "Watch what happens next!"
    }
  ],
  "tts_script": "Get ready for the most incredible moments...",
  "output_path": "outputs/final_viral_compilation.mp4",
  "download_url": "/download/final_viral_compilation.mp4"
}
```

---

### Download Video

**GET** `/download/<filename>`

Download a generated video file.

**Example:** `/download/viral_compilation.mp4`

**Response:** Video file download

---

## Error Handling

All endpoints return errors in the following format:

```json
{
  "error": "Description of the error"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (file doesn't exist)
- `500` - Internal Server Error

---

## Rate Limiting

Currently no rate limiting is implemented. In production, consider:
- Request rate limits per IP
- Upload size limits (currently 500MB max)
- Processing queue for large videos

---

## Example cURL Requests

### Upload a video
```bash
curl -X POST http://localhost:5000/upload \
  -F "videos=@video.mp4"
```

### Analyze video
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "video_path": "uploads/video.mp4",
    "transcription": "[00:00:05] Hello world"
  }'
```

### Process complete workflow
```bash
curl -X POST http://localhost:5000/process-complete \
  -H "Content-Type: application/json" \
  -d '{
    "video_path": "uploads/video.mp4",
    "transcription": "[00:00:05] Welcome to the video\n[00:00:15] Amazing content",
    "tts_style": "engaging"
  }'
```

### Download video
```bash
curl -O http://localhost:5000/download/viral_compilation.mp4
```

---

## Python Client Example

```python
import requests

# Upload video
files = {'videos': open('video.mp4', 'rb')}
response = requests.post('http://localhost:5000/upload', files=files)
uploaded = response.json()

# Process complete workflow
data = {
    'video_path': uploaded['files'][0]['path'],
    'transcription': '[00:00:05] Welcome...',
    'tts_style': 'engaging'
}
response = requests.post('http://localhost:5000/process-complete', json=data)
result = response.json()

# Download result
if result['success']:
    video_url = f"http://localhost:5000{result['download_url']}"
    video_response = requests.get(video_url)
    with open('output.mp4', 'wb') as f:
        f.write(video_response.content)
```

---

## JavaScript/Fetch Example

```javascript
// Upload video
const formData = new FormData();
formData.append('videos', fileInput.files[0]);

fetch('/upload', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  // Process complete workflow
  return fetch('/process-complete', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      video_path: data.files[0].path,
      transcription: '[00:00:05] Welcome...',
      tts_style: 'engaging'
    })
  });
})
.then(response => response.json())
.then(result => {
  // Download video
  window.location.href = result.download_url;
});
```
