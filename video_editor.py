"""
Video Editor Module
Handles video cutting, compilation, transitions, and text overlays.
"""

import os
from typing import List, Dict, Optional
from moviepy.editor import (
    VideoFileClip, concatenate_videoclips, TextClip,
    CompositeVideoClip, AudioFileClip, vfx
)
from moviepy.video.fx.all import fadein, fadeout
import numpy as np


class ViralVideoEditor:
    """Edits videos to create viral compilations."""
    
    def __init__(self, output_dir: str = "outputs"):
        """
        Initialize video editor.
        
        Args:
            output_dir: Directory to save output videos
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def extract_clip(self, video_path: str, start_time: float, end_time: float, 
                     output_path: str = None) -> str:
        """
        Extract a clip from a video.
        
        Args:
            video_path: Path to source video
            start_time: Start time in seconds
            end_time: End time in seconds
            output_path: Optional output path
            
        Returns:
            Path to extracted clip
        """
        try:
            video = VideoFileClip(video_path)
            clip = video.subclip(start_time, end_time)
            
            if output_path is None:
                output_path = os.path.join(
                    self.output_dir, 
                    f"clip_{int(start_time)}_{int(end_time)}.mp4"
                )
            
            clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
            video.close()
            clip.close()
            
            return output_path
        
        except Exception as e:
            print(f"Error extracting clip: {e}")
            raise
    
    def add_text_overlay(self, clip: VideoFileClip, text_overlays: List[Dict]) -> VideoFileClip:
        """
        Add text overlays to a video clip.
        
        Args:
            clip: Video clip
            text_overlays: List of text overlay configs
            
        Returns:
            Clip with text overlays
        """
        video_clips = [clip]
        
        for overlay in text_overlays:
            text = overlay.get('text', '')
            delay = overlay.get('delay', 0)
            duration = overlay.get('duration', 2.0)
            position = overlay.get('position', 'top')
            
            # Position mapping
            pos_map = {
                'top': ('center', 50),
                'center': ('center', 'center'),
                'bottom': ('center', clip.h - 100)
            }
            
            try:
                txt_clip = TextClip(
                    text, 
                    fontsize=60, 
                    color='white',
                    font='Arial-Bold',
                    stroke_color='black',
                    stroke_width=2,
                    method='caption',
                    size=(clip.w - 100, None)
                )
                
                txt_clip = txt_clip.set_position(pos_map.get(position, pos_map['top']))
                txt_clip = txt_clip.set_start(delay).set_duration(duration)
                txt_clip = txt_clip.fadein(0.3).fadeout(0.3)
                
                video_clips.append(txt_clip)
            
            except Exception as e:
                print(f"Error creating text overlay '{text}': {e}")
                # Continue without this overlay
        
        return CompositeVideoClip(video_clips)
    
    def add_transition(self, clip: VideoFileClip, transition_duration: float = 0.5) -> VideoFileClip:
        """
        Add fade in/out transitions to a clip.
        
        Args:
            clip: Video clip
            transition_duration: Duration of transition in seconds
            
        Returns:
            Clip with transitions
        """
        try:
            clip = clip.fx(fadein, transition_duration)
            clip = clip.fx(fadeout, transition_duration)
            return clip
        except Exception as e:
            print(f"Error adding transition: {e}")
            return clip
    
    def compile_clips(self, clips: List[VideoFileClip], output_path: str,
                     add_transitions: bool = True, transition_duration: float = 0.5) -> str:
        """
        Compile multiple clips into one video.
        
        Args:
            clips: List of video clips
            output_path: Path for output video
            add_transitions: Whether to add transitions between clips
            transition_duration: Duration of transitions
            
        Returns:
            Path to compiled video
        """
        try:
            if add_transitions:
                clips = [self.add_transition(clip, transition_duration) for clip in clips]
            
            final_video = concatenate_videoclips(clips, method="compose")
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                fps=24
            )
            
            # Clean up
            for clip in clips:
                clip.close()
            final_video.close()
            
            return output_path
        
        except Exception as e:
            print(f"Error compiling clips: {e}")
            raise
    
    def add_audio_overlay(self, video_path: str, audio_path: str, output_path: str,
                         audio_volume: float = 0.5, video_volume: float = 0.3) -> str:
        """
        Add audio overlay (like TTS) to video.
        
        Args:
            video_path: Path to video
            audio_path: Path to audio file
            output_path: Path for output
            audio_volume: Volume of overlay audio (0-1)
            video_volume: Volume of original video audio (0-1)
            
        Returns:
            Path to output video
        """
        try:
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)
            
            # Adjust volumes
            if video.audio:
                original_audio = video.audio.volumex(video_volume)
            else:
                original_audio = None
            
            overlay_audio = audio.volumex(audio_volume)
            
            # Trim or loop audio to match video duration
            if overlay_audio.duration < video.duration:
                # Audio is shorter, just add it
                pass
            else:
                # Audio is longer, trim it
                overlay_audio = overlay_audio.subclip(0, video.duration)
            
            # Combine audio tracks
            if original_audio:
                from moviepy.audio.AudioClip import CompositeAudioClip
                final_audio = CompositeAudioClip([original_audio, overlay_audio])
            else:
                final_audio = overlay_audio
            
            video = video.set_audio(final_audio)
            video.write_videofile(output_path, codec='libx264', audio_codec='aac')
            
            # Clean up
            video.close()
            audio.close()
            
            return output_path
        
        except Exception as e:
            print(f"Error adding audio overlay: {e}")
            raise
    
    def create_viral_compilation(self, video_path: str, viral_moments: List[Dict],
                                text_overlays_per_moment: List[List[Dict]],
                                output_name: str = "viral_compilation.mp4") -> str:
        """
        Create a complete viral compilation from identified moments.
        
        Args:
            video_path: Path to source video
            viral_moments: List of viral moments with timing
            text_overlays_per_moment: Text overlays for each moment
            output_name: Name of output file
            
        Returns:
            Path to final compilation
        """
        temp_clips = []
        clip_objects = []
        
        try:
            # Extract each viral moment
            for i, moment in enumerate(viral_moments):
                temp_clip_path = os.path.join(
                    self.output_dir,
                    f"temp_clip_{i}.mp4"
                )
                
                # Extract the clip
                self.extract_clip(
                    video_path,
                    moment['start_time'],
                    moment['end_time'],
                    temp_clip_path
                )
                temp_clips.append(temp_clip_path)
                
                # Load clip and add text overlays
                clip = VideoFileClip(temp_clip_path)
                
                if i < len(text_overlays_per_moment):
                    clip = self.add_text_overlay(clip, text_overlays_per_moment[i])
                
                clip_objects.append(clip)
            
            # Compile all clips
            output_path = os.path.join(self.output_dir, output_name)
            self.compile_clips(clip_objects, output_path, add_transitions=True)
            
            # Clean up temporary files
            for temp_clip in temp_clips:
                if os.path.exists(temp_clip):
                    os.remove(temp_clip)
            
            return output_path
        
        except Exception as e:
            print(f"Error creating viral compilation: {e}")
            # Clean up on error
            for temp_clip in temp_clips:
                if os.path.exists(temp_clip):
                    os.remove(temp_clip)
            raise
