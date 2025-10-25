"""
Flask Web Application for Viral Video Clip Generator
"""

import os
import json
from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
from viral_analyzer import ViralMomentAnalyzer
from video_editor import ViralVideoEditor
from tts_generator import TTSGenerator
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_videos():
    """Handle video file uploads (up to 5 videos)."""
    if 'videos' not in request.files:
        return jsonify({'error': 'No video files provided'}), 400
    
    files = request.files.getlist('videos')
    
    if len(files) > 5:
        return jsonify({'error': 'Maximum 5 videos allowed'}), 400
    
    uploaded_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            uploaded_files.append({
                'filename': filename,
                'path': filepath
            })
        else:
            return jsonify({'error': f'Invalid file: {file.filename}'}), 400
    
    return jsonify({
        'success': True,
        'message': f'{len(uploaded_files)} videos uploaded successfully',
        'files': uploaded_files
    })


@app.route('/analyze', methods=['POST'])
def analyze_video():
    """Analyze video to find viral moments."""
    data = request.get_json()
    
    if not data or 'video_path' not in data:
        return jsonify({'error': 'Video path required'}), 400
    
    video_path = data['video_path']
    transcription = data.get('transcription', '')
    visuals_description = data.get('visuals_description', '')
    
    if not transcription:
        return jsonify({'error': 'Transcription required'}), 400
    
    try:
        analyzer = ViralMomentAnalyzer()
        viral_moments = analyzer.analyze_transcription(transcription, visuals_description)
        
        return jsonify({
            'success': True,
            'viral_moments': viral_moments
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate-tts', methods=['POST'])
def generate_tts_script():
    """Generate TTS script from viral moments."""
    data = request.get_json()
    
    if not data or 'viral_moments' not in data:
        return jsonify({'error': 'Viral moments required'}), 400
    
    viral_moments = data['viral_moments']
    style = data.get('style', 'engaging')
    
    try:
        analyzer = ViralMomentAnalyzer()
        script = analyzer.generate_tts_script(viral_moments, style)
        
        return jsonify({
            'success': True,
            'script': script
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate-text-overlays', methods=['POST'])
def generate_text_overlays():
    """Generate on-screen text for viral moments."""
    data = request.get_json()
    
    if not data or 'viral_moments' not in data:
        return jsonify({'error': 'Viral moments required'}), 400
    
    viral_moments = data['viral_moments']
    
    try:
        analyzer = ViralMomentAnalyzer()
        all_overlays = []
        
        for moment in viral_moments:
            overlays = analyzer.generate_onscreen_text(moment)
            all_overlays.append(overlays)
        
        return jsonify({
            'success': True,
            'text_overlays': all_overlays
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/compile', methods=['POST'])
def compile_video():
    """Compile viral clips with transitions and text overlays."""
    data = request.get_json()
    
    required_fields = ['video_path', 'viral_moments']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    video_path = data['video_path']
    viral_moments = data['viral_moments']
    text_overlays = data.get('text_overlays', [])
    tts_audio_path = data.get('tts_audio_path')
    output_name = data.get('output_name', 'viral_compilation.mp4')
    
    try:
        editor = ViralVideoEditor(output_dir=app.config['OUTPUT_FOLDER'])
        
        # Create the compilation
        output_path = editor.create_viral_compilation(
            video_path,
            viral_moments,
            text_overlays,
            output_name
        )
        
        # Add TTS audio if provided
        if tts_audio_path and os.path.exists(tts_audio_path):
            final_output = os.path.join(
                app.config['OUTPUT_FOLDER'],
                f"final_{output_name}"
            )
            output_path = editor.add_audio_overlay(
                output_path,
                tts_audio_path,
                final_output
            )
        
        return jsonify({
            'success': True,
            'output_path': output_path,
            'download_url': url_for('download_video', filename=os.path.basename(output_path))
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/process-complete', methods=['POST'])
def process_complete_workflow():
    """Process complete workflow: analyze, generate TTS, compile."""
    data = request.get_json()
    
    required_fields = ['video_path', 'transcription']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    video_path = data['video_path']
    transcription = data['transcription']
    visuals_description = data.get('visuals_description', '')
    tts_style = data.get('tts_style', 'engaging')
    output_name = data.get('output_name', 'viral_compilation.mp4')
    
    try:
        # Step 1: Analyze for viral moments
        analyzer = ViralMomentAnalyzer()
        viral_moments = analyzer.analyze_transcription(transcription, visuals_description)
        
        if not viral_moments:
            return jsonify({'error': 'No viral moments identified'}), 400
        
        # Step 2: Generate text overlays
        text_overlays = []
        for moment in viral_moments:
            overlays = analyzer.generate_onscreen_text(moment)
            text_overlays.append(overlays)
        
        # Step 3: Generate TTS script
        tts_script = analyzer.generate_tts_script(viral_moments, tts_style)
        
        # Step 4: Generate TTS audio
        tts_generator = TTSGenerator()
        tts_audio_path = tts_generator.generate_tts(tts_script)
        
        # Step 5: Compile video
        editor = ViralVideoEditor(output_dir=app.config['OUTPUT_FOLDER'])
        output_path = editor.create_viral_compilation(
            video_path,
            viral_moments,
            text_overlays,
            output_name
        )
        
        # Step 6: Add TTS audio if generated
        if tts_audio_path and os.path.exists(tts_audio_path):
            final_output = os.path.join(
                app.config['OUTPUT_FOLDER'],
                f"final_{output_name}"
            )
            output_path = editor.add_audio_overlay(
                output_path,
                tts_audio_path,
                final_output
            )
        
        return jsonify({
            'success': True,
            'viral_moments': viral_moments,
            'tts_script': tts_script,
            'output_path': output_path,
            'download_url': url_for('download_video', filename=os.path.basename(output_path))
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download_video(filename):
    """Download generated video."""
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(file_path, as_attachment=True)


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
