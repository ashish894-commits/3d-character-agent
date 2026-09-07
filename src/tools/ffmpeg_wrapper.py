"""FFmpeg wrapper for video processing"""

import subprocess
import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


class FFmpegWrapper:
    """Wrapper for FFmpeg commands"""
    
    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        """Initialize FFmpeg wrapper
        
        Args:
            ffmpeg_path: Path to FFmpeg executable
        """
        self.ffmpeg_path = ffmpeg_path
    
    def compose_frames_to_video(self, input_pattern: str, output_file: str,
                               fps: int = 24, codec: str = "libx264",
                               quality: str = "high") -> bool:
        """Compose image frames into video
        
        Args:
            input_pattern: Input file pattern (e.g., "frame_%04d.png")
            output_file: Output video file path
            fps: Frames per second
            codec: Video codec
            quality: Quality preset (low, medium, high, ultra)
            
        Returns:
            Success status
        """
        quality_presets = {
            "low": "-crf 28 -preset fast",
            "medium": "-crf 23 -preset medium",
            "high": "-crf 18 -preset slow",
            "ultra": "-crf 12 -preset veryslow",
        }
        
        quality_args = quality_presets.get(quality, quality_presets["high"])
        
        cmd = [
            self.ffmpeg_path,
            "-framerate", str(fps),
            "-i", input_pattern,
            "-c:v", codec,
            "-pix_fmt", "yuv420p",
        ]
        
        cmd.extend(quality_args.split())
        cmd.append(output_file)
        
        return self._run_command(cmd, "Compose frames to video")
    
    def add_audio(self, video_file: str, audio_file: str,
                 output_file: str) -> bool:
        """Add audio to video
        
        Args:
            video_file: Path to video file
            audio_file: Path to audio file
            output_file: Output video with audio
            
        Returns:
            Success status
        """
        cmd = [
            self.ffmpeg_path,
            "-i", video_file,
            "-i", audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_file,
        ]
        
        return self._run_command(cmd, "Add audio to video")
    
    def scale_video(self, input_file: str, output_file: str,
                   width: int, height: int) -> bool:
        """Scale video to target resolution
        
        Args:
            input_file: Input video file
            output_file: Output video file
            width: Target width
            height: Target height
            
        Returns:
            Success status
        """
        cmd = [
            self.ffmpeg_path,
            "-i", input_file,
            "-vf", f"scale={width}:{height}",
            output_file,
        ]
        
        return self._run_command(cmd, f"Scale video to {width}x{height}")
    
    def extract_frames(self, video_file: str, output_pattern: str,
                      fps: Optional[int] = None) -> bool:
        """Extract frames from video
        
        Args:
            video_file: Input video file
            output_pattern: Output frame pattern (e.g., "frame_%04d.png")
            fps: Output frames per second (None = all frames)
            
        Returns:
            Success status
        """
        cmd = [self.ffmpeg_path, "-i", video_file]
        
        if fps:
            cmd.extend(["-vf", f"fps={fps}"])
        
        cmd.append(output_pattern)
        
        return self._run_command(cmd, "Extract frames from video")
    
    def concatenate_videos(self, video_list: List[str],
                          output_file: str,
                          concat_file: str = "concat.txt") -> bool:
        """Concatenate multiple videos
        
        Args:
            video_list: List of video file paths
            output_file: Output concatenated video
            concat_file: Temporary concat demux file
            
        Returns:
            Success status
        """
        try:
            # Create concat demux file
            with open(concat_file, 'w') as f:
                for video in video_list:
                    f.write(f"file '{video}'\n")
            
            cmd = [
                self.ffmpeg_path,
                "-f", "concat",
                "-safe", "0",
                "-i", concat_file,
                "-c", "copy",
                output_file,
            ]
            
            return self._run_command(cmd, "Concatenate videos")
        finally:
            Path(concat_file).unlink(missing_ok=True)
    
    def apply_filter(self, input_file: str, output_file: str,
                    filter_string: str) -> bool:
        """Apply FFmpeg filter to video
        
        Args:
            input_file: Input video file
            output_file: Output video file
            filter_string: FFmpeg filter string
            
        Returns:
            Success status
        """
        cmd = [
            self.ffmpeg_path,
            "-i", input_file,
            "-vf", filter_string,
            output_file,
        ]
        
        return self._run_command(cmd, f"Apply filter: {filter_string}")
    
    def _run_command(self, cmd: List[str], description: str) -> bool:
        """Run FFmpeg command
        
        Args:
            cmd: Command list
            description: Command description for logging
            
        Returns:
            Success status
        """
        try:
            logger.info(f"{description}: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
            
            logger.info(f"{description} completed successfully")
            return True
        except Exception as e:
            logger.error(f"Error running FFmpeg: {e}")
            return False
