#!/usr/bin/env python3
"""
Project Verification Script

Checks that all components are properly set up and ready to use.
"""

import os
import sys


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def check_files():
    """Check that all required files exist."""
    print_header("FILE STRUCTURE CHECK")
    
    required_files = {
        'Core Modules': [
            'viral_analyzer.py',
            'video_editor.py',
            'tts_generator.py',
            'app.py',
            'cli.py'
        ],
        'Documentation': [
            'README.md',
            'QUICKSTART.md',
            'API.md',
            'WORKFLOW.md',
            'CONTRIBUTING.md',
            'LICENSE'
        ],
        'Configuration': [
            'requirements.txt',
            '.env.example',
            '.gitignore'
        ],
        'Utilities': [
            'setup.sh',
            'test_basic.py',
            'examples.py'
        ],
        'Examples': [
            'example_transcription.txt',
            'example_visuals.txt'
        ],
        'Templates': [
            'templates/index.html'
        ]
    }
    
    all_present = True
    for category, files in required_files.items():
        print(f"\n{category}:")
        for file in files:
            exists = os.path.exists(file)
            status = "✅" if exists else "❌"
            print(f"  {status} {file}")
            if not exists:
                all_present = False
    
    return all_present


def check_dependencies():
    """Check if dependencies are installed."""
    print_header("DEPENDENCIES CHECK")
    
    dependencies = {
        'flask': 'Flask web framework',
        'groq': 'Groq AI client',
        'moviepy': 'Video editing library',
        'dotenv': 'Environment variables',
        'requests': 'HTTP library'
    }
    
    installed = {}
    for package, description in dependencies.items():
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package:15} - {description}")
            installed[package] = True
        except ImportError:
            print(f"  ❌ {package:15} - {description} (NOT INSTALLED)")
            installed[package] = False
    
    return all(installed.values())


def check_environment():
    """Check environment configuration."""
    print_header("ENVIRONMENT CHECK")
    
    checks = []
    
    # Check for .env file
    env_exists = os.path.exists('.env')
    print(f"  {'✅' if env_exists else '⚠️ '} .env file exists: {env_exists}")
    if not env_exists:
        print(f"     Create from: cp .env.example .env")
    checks.append(env_exists)
    
    # Check for API key
    api_key = os.getenv('GROQ_API_KEY')
    has_key = api_key and api_key != 'your_groq_api_key_here'
    print(f"  {'✅' if has_key else '⚠️ '} GROQ_API_KEY configured: {has_key}")
    if not has_key:
        print(f"     Set in .env file")
    checks.append(has_key)
    
    # Check directories
    for directory in ['uploads', 'outputs']:
        exists = os.path.isdir(directory)
        print(f"  {'✅' if exists else '⚠️ '} {directory}/ directory: {exists}")
        if not exists:
            print(f"     Will be created automatically")
    
    return all(checks)


def check_external_tools():
    """Check for external tools like FFmpeg."""
    print_header("EXTERNAL TOOLS CHECK")
    
    import subprocess
    
    tools = {
        'ffmpeg': 'FFmpeg (video processing)',
        'python3': 'Python 3'
    }
    
    available = {}
    for tool, description in tools.items():
        try:
            result = subprocess.run(
                [tool, '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                print(f"  ✅ {tool:15} - {description}")
                print(f"     {version[:60]}")
                available[tool] = True
            else:
                print(f"  ❌ {tool:15} - {description} (NOT FOUND)")
                available[tool] = False
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print(f"  ❌ {tool:15} - {description} (NOT FOUND)")
            available[tool] = False
    
    return available.get('ffmpeg', False)


def print_summary(files_ok, deps_ok, env_ok, tools_ok):
    """Print final summary."""
    print_header("VERIFICATION SUMMARY")
    
    print(f"\n  Files Structure:    {'✅ PASS' if files_ok else '❌ FAIL'}")
    print(f"  Dependencies:       {'✅ PASS' if deps_ok else '⚠️  INCOMPLETE'}")
    print(f"  Environment:        {'✅ PASS' if env_ok else '⚠️  INCOMPLETE'}")
    print(f"  External Tools:     {'✅ PASS' if tools_ok else '⚠️  INCOMPLETE'}")
    
    print("\n" + "=" * 70)
    
    if files_ok and deps_ok and env_ok and tools_ok:
        print("\n  🎉 ALL CHECKS PASSED! Ready to use.")
        print("\n  Quick Start:")
        print("    1. python app.py              # Start web interface")
        print("    2. python cli.py --help       # Use CLI tool")
        print("    3. python examples.py         # Run examples")
        return 0
    else:
        print("\n  ⚠️  SETUP INCOMPLETE - Follow the steps below:")
        
        if not deps_ok:
            print("\n  Install Dependencies:")
            print("    pip install -r requirements.txt")
        
        if not env_ok:
            print("\n  Configure Environment:")
            print("    1. cp .env.example .env")
            print("    2. Edit .env and add your GROQ_API_KEY")
        
        if not tools_ok:
            print("\n  Install FFmpeg:")
            print("    Ubuntu/Debian: sudo apt-get install ffmpeg")
            print("    macOS:         brew install ffmpeg")
            print("    Windows:       https://ffmpeg.org/download.html")
        
        print("\n  Then run this script again to verify.")
        return 1


def main():
    """Run all verification checks."""
    print("\n" + "=" * 70)
    print("  VIRAL VIDEO CLIP GENERATOR - VERIFICATION")
    print("=" * 70)
    
    files_ok = check_files()
    deps_ok = check_dependencies()
    env_ok = check_environment()
    tools_ok = check_external_tools()
    
    return print_summary(files_ok, deps_ok, env_ok, tools_ok)


if __name__ == '__main__':
    sys.exit(main())
