"""
Command Line Interface for Viral Video Clip Generator
"""

import argparse
import os
import sys
from viral_analyzer import ViralMomentAnalyzer
from video_editor import ViralVideoEditor
from tts_generator import TTSGenerator


def main():
    parser = argparse.ArgumentParser(
        description='Generate viral video clips from transcriptions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a video with transcription
  python cli.py analyze video.mp4 --transcription transcription.txt
  
  # Process complete workflow
  python cli.py process video.mp4 --transcription transcription.txt --output viral.mp4
  
  # Generate TTS script
  python cli.py tts --moments moments.json --style dramatic
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze video for viral moments')
    analyze_parser.add_argument('video', help='Path to video file')
    analyze_parser.add_argument('--transcription', '-t', required=True, help='Path to transcription file')
    analyze_parser.add_argument('--visuals', '-v', help='Path to visual descriptions file')
    analyze_parser.add_argument('--output', '-o', default='viral_moments.json', help='Output JSON file')
    
    # Process command (complete workflow)
    process_parser = subparsers.add_parser('process', help='Complete processing workflow')
    process_parser.add_argument('video', help='Path to video file')
    process_parser.add_argument('--transcription', '-t', required=True, help='Path to transcription file')
    process_parser.add_argument('--visuals', '-v', help='Path to visual descriptions file')
    process_parser.add_argument('--output', '-o', default='viral_compilation.mp4', help='Output video file')
    process_parser.add_argument('--style', '-s', default='engaging', 
                               choices=['engaging', 'dramatic', 'casual'], 
                               help='TTS narration style')
    process_parser.add_argument('--no-tts', action='store_true', help='Skip TTS generation')
    process_parser.add_argument('--no-transitions', action='store_true', help='Skip transitions')
    
    # TTS command
    tts_parser = subparsers.add_parser('tts', help='Generate TTS script')
    tts_parser.add_argument('--moments', '-m', required=True, help='Path to viral moments JSON')
    tts_parser.add_argument('--style', '-s', default='engaging', 
                           choices=['engaging', 'dramatic', 'casual'],
                           help='TTS style')
    tts_parser.add_argument('--output', '-o', default='tts_script.txt', help='Output text file')
    
    # Compile command
    compile_parser = subparsers.add_parser('compile', help='Compile viral clips')
    compile_parser.add_argument('video', help='Path to source video')
    compile_parser.add_argument('--moments', '-m', required=True, help='Path to viral moments JSON')
    compile_parser.add_argument('--output', '-o', default='compilation.mp4', help='Output video file')
    compile_parser.add_argument('--no-transitions', action='store_true', help='Skip transitions')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'analyze':
            analyze_command(args)
        elif args.command == 'process':
            process_command(args)
        elif args.command == 'tts':
            tts_command(args)
        elif args.command == 'compile':
            compile_command(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def analyze_command(args):
    """Analyze video for viral moments."""
    import json
    
    print(f"Analyzing video: {args.video}")
    
    # Read transcription
    with open(args.transcription, 'r') as f:
        transcription = f.read()
    
    # Read visuals if provided
    visuals = ''
    if args.visuals:
        with open(args.visuals, 'r') as f:
            visuals = f.read()
    
    # Analyze
    analyzer = ViralMomentAnalyzer()
    viral_moments = analyzer.analyze_transcription(transcription, visuals)
    
    # Save results
    with open(args.output, 'w') as f:
        json.dump(viral_moments, f, indent=2)
    
    print(f"\n✅ Found {len(viral_moments)} viral moments")
    for i, moment in enumerate(viral_moments, 1):
        print(f"\nMoment {i}:")
        print(f"  Time: {moment['start_time']:.1f}s - {moment['end_time']:.1f}s")
        print(f"  Score: {moment['score']}/100")
        print(f"  Reason: {moment['reason']}")
    
    print(f"\n💾 Saved to: {args.output}")


def process_command(args):
    """Process complete workflow."""
    import json
    
    print(f"Processing video: {args.video}")
    
    # Read transcription
    with open(args.transcription, 'r') as f:
        transcription = f.read()
    
    # Read visuals if provided
    visuals = ''
    if args.visuals:
        with open(args.visuals, 'r') as f:
            visuals = f.read()
    
    # Step 1: Analyze
    print("\n🔍 Step 1: Analyzing for viral moments...")
    analyzer = ViralMomentAnalyzer()
    viral_moments = analyzer.analyze_transcription(transcription, visuals)
    print(f"   Found {len(viral_moments)} viral moments")
    
    # Step 2: Generate text overlays
    print("\n📝 Step 2: Generating on-screen text...")
    text_overlays = []
    for moment in viral_moments:
        overlays = analyzer.generate_onscreen_text(moment)
        text_overlays.append(overlays)
    
    # Step 3: Generate TTS
    tts_audio_path = None
    if not args.no_tts:
        print(f"\n🎙️ Step 3: Generating TTS script ({args.style})...")
        tts_script = analyzer.generate_tts_script(viral_moments, args.style)
        print(f"   Script: {tts_script[:100]}...")
        
        tts_generator = TTSGenerator()
        tts_audio_path = tts_generator.generate_tts(tts_script)
        if tts_audio_path:
            print(f"   Audio saved to: {tts_audio_path}")
    
    # Step 4: Compile video
    print("\n🎬 Step 4: Compiling viral clips...")
    editor = ViralVideoEditor()
    output_path = editor.create_viral_compilation(
        args.video,
        viral_moments,
        text_overlays,
        args.output
    )
    
    # Step 5: Add TTS if generated
    if tts_audio_path and os.path.exists(tts_audio_path):
        print("\n🔊 Step 5: Adding TTS narration...")
        final_output = args.output.replace('.mp4', '_final.mp4')
        output_path = editor.add_audio_overlay(
            output_path,
            tts_audio_path,
            final_output
        )
    
    print(f"\n✅ Complete! Video saved to: {output_path}")


def tts_command(args):
    """Generate TTS script."""
    import json
    
    # Load viral moments
    with open(args.moments, 'r') as f:
        viral_moments = json.load(f)
    
    # Generate script
    analyzer = ViralMomentAnalyzer()
    script = analyzer.generate_tts_script(viral_moments, args.style)
    
    # Save script
    with open(args.output, 'w') as f:
        f.write(script)
    
    print(f"TTS Script ({args.style}):")
    print(script)
    print(f"\n💾 Saved to: {args.output}")


def compile_command(args):
    """Compile viral clips."""
    import json
    
    # Load viral moments
    with open(args.moments, 'r') as f:
        viral_moments = json.load(f)
    
    print(f"Compiling {len(viral_moments)} clips from: {args.video}")
    
    # Compile
    editor = ViralVideoEditor()
    output_path = editor.create_viral_compilation(
        args.video,
        viral_moments,
        [],  # No text overlays in simple compile
        args.output
    )
    
    print(f"✅ Compilation saved to: {output_path}")


if __name__ == '__main__':
    main()
