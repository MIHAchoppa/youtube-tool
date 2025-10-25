# Contributing to Viral Video Clip Generator

Thank you for considering contributing to this project! 🎉

## Ways to Contribute

- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🔧 Submit code improvements
- 🎨 Enhance the UI/UX
- 🧪 Add tests

## Getting Started

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR_USERNAME/youtube-tool.git
cd youtube-tool
```

### 2. Set Up Development Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Create directories
mkdir -p uploads outputs
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose

### Example Code Style
```python
def process_video(video_path: str, options: Dict) -> str:
    """
    Process a video file with the given options.
    
    Args:
        video_path: Path to the input video file
        options: Processing options dictionary
        
    Returns:
        Path to the processed video file
        
    Raises:
        ValueError: If video_path is invalid
        ProcessingError: If video processing fails
    """
    # Implementation
    pass
```

### Testing

Before submitting a PR, test your changes:

```bash
# Run basic tests
python test_basic.py

# Test your specific changes manually
python examples.py

# Test the web interface
python app.py
# Then open http://localhost:5000

# Test the CLI
python cli.py --help
```

### Commit Messages

Write clear, descriptive commit messages:

```
✅ Good:
- Add support for WebM video format
- Fix text overlay positioning bug
- Improve error handling in video editor

❌ Avoid:
- Update files
- Fix bug
- Changes
```

## Areas for Contribution

### High Priority

1. **TTS Integration**
   - Implement actual Groq Play AI integration in `tts_generator.py`
   - Add support for other TTS services (ElevenLabs, Google TTS, etc.)

2. **Testing**
   - Add unit tests for core modules
   - Add integration tests for complete workflows
   - Add test fixtures and sample videos

3. **Performance**
   - Optimize video processing for large files
   - Add progress indicators for long operations
   - Implement async processing queue

4. **UI Enhancements**
   - Add drag-and-drop for visual editor
   - Show processing progress with percentage
   - Add preview of viral moments before compilation

### Medium Priority

5. **Features**
   - Support for more video formats
   - Batch processing multiple videos
   - Custom text overlay fonts and styles
   - Music/background audio integration

6. **Documentation**
   - Video tutorials
   - More code examples
   - API client libraries
   - Deployment guides

7. **Error Handling**
   - Better error messages
   - Recovery from failures
   - Validation improvements

### Ideas Welcome

8. **Innovation**
   - Social media platform integration
   - Automatic hashtag generation
   - Thumbnail generation
   - A/B testing different edits

## Pull Request Process

### 1. Before Submitting

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### 2. Submit PR

1. Push your branch to your fork
2. Open a Pull Request on GitHub
3. Fill out the PR template
4. Link any related issues

### 3. PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How did you test these changes?

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### 4. Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged!

## Reporting Bugs

### Before Reporting

1. Check existing issues
2. Try with the latest version
3. Reproduce the bug consistently

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Upload video '...'
2. Set transcription '...'
3. Click '...'
4. See error

**Expected Behavior**
What you expected to happen

**Screenshots**
If applicable

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.10]
- FFmpeg version: [e.g., 4.4.2]

**Additional Context**
Any other relevant information
```

## Feature Requests

We love new ideas! When suggesting features:

1. Explain the use case
2. Describe the expected behavior
3. Consider implementation challenges
4. Link to similar features elsewhere

### Feature Request Template

```markdown
**Problem to Solve**
What problem does this solve?

**Proposed Solution**
How should it work?

**Alternatives Considered**
Other approaches you've thought of

**Additional Context**
Mockups, examples, etc.
```

## Code Organization

```
youtube-tool/
├── Core Modules (add features here)
│   ├── viral_analyzer.py    # AI analysis
│   ├── video_editor.py      # Video processing
│   └── tts_generator.py     # TTS generation
│
├── Application Layer
│   ├── app.py              # Flask server
│   └── cli.py              # CLI tool
│
├── Frontend
│   └── templates/
│       └── index.html      # Web UI
│
└── Tests (add tests here)
    └── test_basic.py
```

## Questions?

- 💬 Open a GitHub Discussion
- 📧 Email maintainers
- 🐛 File an issue for clarification

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🙏

Every contribution, no matter how small, helps make this project better.
