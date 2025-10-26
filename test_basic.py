"""
Simple test script to verify the modules work correctly.
Note: Requires GROQ_API_KEY to be set for full testing.
"""

import os
import sys

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from viral_analyzer import ViralMomentAnalyzer
        from video_editor import ViralVideoEditor
        from tts_generator import TTSGenerator
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_viral_analyzer():
    """Test viral analyzer (requires API key)."""
    print("\nTesting Viral Analyzer...")
    
    if not os.getenv('GROQ_API_KEY'):
        print("⚠️  Skipping: GROQ_API_KEY not set")
        return True
    
    try:
        from viral_analyzer import ViralMomentAnalyzer
        analyzer = ViralMomentAnalyzer()
        print("✅ Analyzer initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_video_editor():
    """Test video editor initialization."""
    print("\nTesting Video Editor...")
    try:
        from video_editor import ViralVideoEditor
        editor = ViralVideoEditor()
        print("✅ Editor initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_tts_generator():
    """Test TTS generator initialization."""
    print("\nTesting TTS Generator...")
    try:
        from tts_generator import TTSGenerator
        generator = TTSGenerator()
        print("✅ TTS Generator initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_flask_app():
    """Test Flask app can be imported."""
    print("\nTesting Flask App...")
    try:
        import app
        print("✅ Flask app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_cli():
    """Test CLI can be imported."""
    print("\nTesting CLI...")
    try:
        import cli
        print("✅ CLI imported successfully")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("Viral Video Clip Generator - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_viral_analyzer,
        test_video_editor,
        test_tts_generator,
        test_flask_app,
        test_cli
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
