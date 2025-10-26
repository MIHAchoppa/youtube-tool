"""
Viral Video Clip Generator
A tool that processes video files with transcriptions to identify and compile viral moments.
"""

import os
import json
from typing import List, Dict, Tuple
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class ViralMomentAnalyzer:
    """Analyzes video transcriptions to identify viral moments using Groq."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the analyzer with Groq API.
        
        Args:
            api_key: Groq API key. If None, uses GROQ_API_KEY from environment.
        """
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("Groq API key not found. Set GROQ_API_KEY environment variable.")
        self.client = Groq(api_key=self.api_key)
    
    def analyze_transcription(self, transcription: str, visuals_description: str = "") -> List[Dict]:
        """
        Analyze transcription and visuals to identify viral moments.
        
        Args:
            transcription: Transcription with timestamps in format "[00:00:00] text"
            visuals_description: Description of visual elements with timestamps
            
        Returns:
            List of viral moments with start_time, end_time, score, and reason
        """
        prompt = f"""Analyze the following video transcription and visual descriptions to identify the most viral moments.
        
Transcription:
{transcription}

Visual Descriptions:
{visuals_description}

Identify 3-5 of the most viral moments that would perform well on social media. For each moment:
1. Provide start and end timestamps in seconds
2. Give a virality score (0-100)
3. Explain why this moment is viral-worthy

Return ONLY a JSON array with this exact structure:
[
  {{
    "start_time": 10.5,
    "end_time": 25.3,
    "score": 95,
    "reason": "High energy reaction with visual impact",
    "hook": "Watch what happens next!"
  }}
]
"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert video editor specializing in viral social media content. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.2-90b-text-preview",  # Using Groq's reasoning model
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            # Extract JSON from markdown code blocks if present
            if content.startswith("```"):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1]) if len(lines) > 2 else content
                if content.startswith('json'):
                    content = content[4:].strip()
            
            viral_moments = json.loads(content)
            return sorted(viral_moments, key=lambda x: x['score'], reverse=True)
        
        except Exception as e:
            print(f"Error analyzing transcription: {e}")
            return []
    
    def generate_tts_script(self, viral_moments: List[Dict], style: str = "engaging") -> str:
        """
        Generate a TTS script for viral clips.
        
        Args:
            viral_moments: List of identified viral moments
            style: Style of narration (engaging, dramatic, casual)
            
        Returns:
            TTS script text
        """
        moments_summary = "\n".join([
            f"- Moment {i+1} ({m['start_time']}s-{m['end_time']}s): {m['reason']}"
            for i, m in enumerate(viral_moments[:3])
        ])
        
        prompt = f"""Create a short, engaging voice-over script for a viral video compilation.

The video contains these viral moments:
{moments_summary}

Style: {style}

Create a 15-30 second script that:
1. Hooks the viewer immediately
2. Builds anticipation
3. Keeps energy high
4. Works well with background music

Return ONLY the script text, no additional formatting or explanations."""

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a viral video content creator. Write punchy, engaging scripts."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.2-90b-text-preview",
                temperature=0.8,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating TTS script: {e}")
            return "Check out these incredible moments!"
    
    def generate_onscreen_text(self, moment: Dict) -> List[Dict]:
        """
        Generate on-screen text suggestions for a viral moment.
        
        Args:
            moment: Viral moment dict with timing and context
            
        Returns:
            List of text overlays with timing and position
        """
        prompt = f"""Create 1-3 punchy on-screen text overlays for this viral moment:

Moment: {moment['reason']}
Duration: {moment['end_time'] - moment['start_time']:.1f} seconds
Hook: {moment.get('hook', '')}

Generate text that:
- Is short and impactful (3-8 words)
- Appears at key moments
- Uses social media language

Return ONLY a JSON array:
[
  {{
    "text": "WAIT FOR IT...",
    "delay": 0,
    "duration": 2.0,
    "position": "top"
  }}
]"""

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a viral video editor. Create attention-grabbing text overlays. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.2-90b-text-preview",
                temperature=0.8,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            # Extract JSON from markdown code blocks if present
            if content.startswith("```"):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1]) if len(lines) > 2 else content
                if content.startswith('json'):
                    content = content[4:].strip()
            
            return json.loads(content)
        
        except Exception as e:
            print(f"Error generating on-screen text: {e}")
            return [{"text": moment.get('hook', 'Watch this!'), "delay": 0, "duration": 2.0, "position": "top"}]
