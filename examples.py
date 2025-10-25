#!/usr/bin/env python3
"""
Example usage of the Viral Video Clip Generator

This script demonstrates how to use the tool programmatically.
"""

import os
from viral_analyzer import ViralMomentAnalyzer
from video_editor import ViralVideoEditor
from tts_generator import TTSGenerator


def example_basic_analysis():
    """Example: Analyze transcription for viral moments."""
    print("=" * 60)
    print("Example 1: Basic Viral Moment Analysis")
    print("=" * 60)
    
    # Sample transcription
    transcription = """
[00:00:05] Welcome to this amazing tutorial
[00:00:15] Today I'm going to show you something incredible
[00:00:25] Watch what happens when I apply this technique
[00:00:35] BOOM! Did you see that transformation?
[00:00:45] This is why this method is going viral
[00:00:55] Let me show you the secret behind this
[00:01:05] And that's how you create amazing results
"""
    
    visuals = """
[00:00:05] Camera zooms in on subject
[00:00:15] Dramatic lighting change
[00:00:25] Quick editing montage
[00:00:35] Explosive visual effect
[00:00:45] Before and after comparison
[00:00:55] Close-up demonstration
[00:01:05] Final reveal shot
"""
    
    try:
        # Initialize analyzer
        analyzer = ViralMomentAnalyzer()
        
        # Analyze for viral moments
        print("\n🔍 Analyzing transcription...")
        viral_moments = analyzer.analyze_transcription(transcription, visuals)
        
        # Display results
        print(f"\n✅ Found {len(viral_moments)} viral moments:\n")
        for i, moment in enumerate(viral_moments, 1):
            print(f"Moment {i}:")
            print(f"  Time: {moment['start_time']:.1f}s - {moment['end_time']:.1f}s")
            print(f"  Score: {moment['score']}/100")
            print(f"  Reason: {moment['reason']}")
            if 'hook' in moment:
                print(f"  Hook: \"{moment['hook']}\"")
            print()
        
        return viral_moments
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure GROQ_API_KEY is set in your .env file")
        return []


def example_tts_generation(viral_moments):
    """Example: Generate TTS script from viral moments."""
    print("=" * 60)
    print("Example 2: TTS Script Generation")
    print("=" * 60)
    
    if not viral_moments:
        print("⚠️  No viral moments provided, skipping...")
        return None
    
    try:
        analyzer = ViralMomentAnalyzer()
        
        # Generate scripts with different styles
        styles = ['engaging', 'dramatic', 'casual']
        
        for style in styles:
            print(f"\n📝 Generating {style} script...")
            script = analyzer.generate_tts_script(viral_moments, style)
            print(f"\n{style.upper()} Script:")
            print("-" * 60)
            print(script)
            print("-" * 60)
        
        return script
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def example_text_overlays(viral_moments):
    """Example: Generate on-screen text for moments."""
    print("\n" + "=" * 60)
    print("Example 3: On-Screen Text Generation")
    print("=" * 60)
    
    if not viral_moments:
        print("⚠️  No viral moments provided, skipping...")
        return []
    
    try:
        analyzer = ViralMomentAnalyzer()
        
        all_overlays = []
        for i, moment in enumerate(viral_moments[:3], 1):  # Top 3 moments
            print(f"\n📝 Generating text for moment {i}...")
            overlays = analyzer.generate_onscreen_text(moment)
            
            print(f"\nText overlays for moment {i}:")
            for overlay in overlays:
                print(f"  - \"{overlay['text']}\"")
                print(f"    Position: {overlay['position']}, "
                      f"Delay: {overlay['delay']}s, "
                      f"Duration: {overlay['duration']}s")
            
            all_overlays.append(overlays)
        
        return all_overlays
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return []


def example_video_compilation():
    """Example: Video editing workflow (requires actual video file)."""
    print("\n" + "=" * 60)
    print("Example 4: Video Compilation")
    print("=" * 60)
    
    print("\n⚠️  This example requires an actual video file.")
    print("To run a full video compilation:")
    print("\n1. Place a video file in the current directory")
    print("2. Create a transcription file")
    print("3. Run: python cli.py process video.mp4 --transcription transcript.txt")
    print("\nOr use the web interface:")
    print("1. Run: python app.py")
    print("2. Open: http://localhost:5000")
    print("3. Upload and process your video")


def example_tts_audio_generation(script):
    """Example: Generate TTS audio."""
    print("\n" + "=" * 60)
    print("Example 5: TTS Audio Generation")
    print("=" * 60)
    
    if not script:
        script = "This is an example of text-to-speech generation for viral videos."
    
    try:
        tts_generator = TTSGenerator()
        
        print("\n🎙️ Generating TTS audio...")
        print(f"Script: {script[:100]}...")
        
        audio_path = tts_generator.generate_tts(script, output_path="outputs/example_tts.mp3")
        
        if audio_path:
            print(f"\n✅ TTS audio generated: {audio_path}")
            print("\nNote: Currently using placeholder implementation.")
            print("In production, integrate with Groq Play AI or another TTS service.")
        else:
            print("\n⚠️  TTS generation skipped (requires FFmpeg and API integration)")
        
        return audio_path
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("🎬 Viral Video Clip Generator - Examples")
    print("=" * 60)
    print("\nThese examples demonstrate the core functionality")
    print("of the Viral Video Clip Generator.\n")
    
    # Ensure output directory exists
    os.makedirs('outputs', exist_ok=True)
    
    # Example 1: Analyze viral moments
    viral_moments = example_basic_analysis()
    
    # Example 2: Generate TTS scripts
    script = example_tts_generation(viral_moments)
    
    # Example 3: Generate on-screen text
    text_overlays = example_text_overlays(viral_moments)
    
    # Example 4: Video compilation info
    example_video_compilation()
    
    # Example 5: TTS audio generation
    audio_path = example_tts_audio_generation(script)
    
    print("\n" + "=" * 60)
    print("✅ Examples complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Set your GROQ_API_KEY in .env")
    print("2. Try the web interface: python app.py")
    print("3. Or use the CLI: python cli.py --help")
    print("4. See QUICKSTART.md for detailed usage")
    print()


if __name__ == '__main__':
    main()
