#!/usr/bin/env python3
"""
Automated Media Generation Script using Claude Code SDK
This script automates the process of generating cat images, videos, and music
using various AI services through the Claude Code SDK.
"""

import argparse
import os
import sys
import time
import requests
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from anthropic import Anthropic

# Configuration
OUTPUT_DIR = Path("output")
DEFAULT_IMAGE_PROMPT = "A cute fluffy cat sitting peacefully, soft lighting, adorable expression, high quality, photorealistic"
DEFAULT_TEXT_OVERLAY = "The cat is so cute!"
DEFAULT_MUSIC_PROMPT = "Gentle healing music for a cute cat video, soft piano melody, calming ambient sounds, peaceful and soothing atmosphere"

class MediaGenerator:
    def __init__(self):
        self.client = Anthropic()
        self.setup_output_directory()
        
    def setup_output_directory(self):
        """Create output directory if it doesn't exist"""
        OUTPUT_DIR.mkdir(exist_ok=True)
        print(f"✅ Output directory created: {OUTPUT_DIR.absolute()}")
        
    def generate_with_claude(self, prompt: str, tools: list) -> str:
        """Generate content using Claude with specified tools"""
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                tools=tools,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return response.content[0].text
        except Exception as e:
            print(f"❌ Error with Claude generation: {e}")
            return ""
    
    def generate_cat_image(self, prompt: str, text_overlay: str) -> Optional[str]:
        """Generate cat image with text overlay using Imagen 3"""
        print(f"🎨 Generating cat image with text overlay...")
        
        # Create the full prompt including text overlay
        full_prompt = f"{prompt} with the text '{text_overlay}' displayed prominently in the center of the image, beautiful typography"
        
        claude_prompt = f"""
        Generate a cat image with text overlay using the mcp__t2i-google-imagen3__imagen_t2i tool.
        
        Prompt: {full_prompt}
        
        Please use these parameters:
        - aspect_ratio: "1:1"
        - auto_download: true
        - output_directory: "./output/"
        
        Return only the downloaded file path.
        """
        
        tools = [
            {
                "name": "mcp__t2i-google-imagen3__imagen_t2i",
                "description": "Generate images with Google Imagen 3"
            }
        ]
        
        result = self.generate_with_claude(claude_prompt, tools)
        print(f"✅ Cat image generated: {result}")
        return result
    
    def generate_video_from_image(self, image_path: str) -> Optional[str]:
        """Generate video from image using Hailuo i2v"""
        print(f"🎬 Generating video from image: {image_path}")
        
        claude_prompt = f"""
        Generate a video from the cat image using the mcp__i2v-fal-hailuo-02-pro__hailuo_02_submit tool.
        
        Use these parameters:
        - prompt: "A cute cat sitting peacefully, gentle movements, soft lighting, adorable and calming scene"
        - image_url: "{image_path}"
        - prompt_optimizer: true
        
        Then check the status and download the result.
        Return only the downloaded video file path.
        """
        
        tools = [
            {
                "name": "mcp__i2v-fal-hailuo-02-pro__hailuo_02_submit",
                "description": "Generate video from image"
            },
            {
                "name": "mcp__i2v-fal-hailuo-02-pro__hailuo_02_status",
                "description": "Check video generation status"
            },
            {
                "name": "mcp__i2v-fal-hailuo-02-pro__hailuo_02_result",
                "description": "Download generated video"
            }
        ]
        
        result = self.generate_with_claude(claude_prompt, tools)
        print(f"✅ Video generated: {result}")
        return result
    
    def generate_music(self, prompt: str) -> Optional[str]:
        """Generate healing music using Lyria"""
        print(f"🎵 Generating healing music...")
        
        claude_prompt = f"""
        Generate healing music using the mcp__t2m-google-lyria__lyria_generate tool.
        
        Use these parameters:
        - prompt: "{prompt}"
        - style: "ambient"
        - tempo: "slow"
        - duration: 30
        - auto_download: true
        - output_directory: "./output/"
        
        Return only the downloaded file path.
        """
        
        tools = [
            {
                "name": "mcp__t2m-google-lyria__lyria_generate",
                "description": "Generate music with Google Lyria"
            }
        ]
        
        result = self.generate_with_claude(claude_prompt, tools)
        print(f"✅ Music generated: {result}")
        return result
    
    def combine_video_audio(self, video_path: str, audio_path: str) -> Optional[str]:
        """Combine video and audio using moviepy"""
        print(f"🎬 Combining video and audio...")
        
        try:
            from moviepy import VideoFileClip, AudioFileClip
            
            # Load video and audio
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)
            
            # Trim audio to match video duration
            if audio.duration > video.duration:
                audio = audio.subclipped(0, video.duration)
            
            # Combine video and audio
            final_video = video.with_audio(audio)
            
            # Create output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"final_cat_video_{timestamp}.mp4"
            
            # Write final video
            final_video.write_videofile(str(output_path), codec='libx264', audio_codec='aac')
            
            # Cleanup
            video.close()
            audio.close()
            final_video.close()
            
            print(f"✅ Final video created: {output_path}")
            return str(output_path)
            
        except Exception as e:
            print(f"❌ Error combining video and audio: {e}")
            return None
    
    def generate_media_workflow(self, image_prompt: str, text_overlay: str, music_prompt: str) -> Dict[str, Any]:
        """Run the complete media generation workflow"""
        print("🚀 Starting automated media generation workflow...")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "image_prompt": image_prompt,
            "text_overlay": text_overlay,
            "music_prompt": music_prompt,
            "generated_files": {}
        }
        
        # Step 1: Generate cat image with text
        image_path = self.generate_cat_image(image_prompt, text_overlay)
        if image_path:
            results["generated_files"]["image"] = image_path
        
        # Step 2: Generate video from image
        if image_path:
            video_path = self.generate_video_from_image(image_path)
            if video_path:
                results["generated_files"]["video"] = video_path
        
        # Step 3: Generate healing music
        music_path = self.generate_music(music_prompt)
        if music_path:
            results["generated_files"]["music"] = music_path
        
        # Step 4: Combine video and audio
        if results["generated_files"].get("video") and results["generated_files"].get("music"):
            final_video_path = self.combine_video_audio(
                results["generated_files"]["video"],
                results["generated_files"]["music"]
            )
            if final_video_path:
                results["generated_files"]["final_video"] = final_video_path
        
        # Save results to JSON
        results_path = OUTPUT_DIR / f"generation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Workflow completed! Results saved to: {results_path}")
        return results

def main():
    """Main function to run the media generation workflow"""
    parser = argparse.ArgumentParser(description='Automated Media Generation with Claude Code SDK')
    parser.add_argument('--image-prompt', default=DEFAULT_IMAGE_PROMPT,
                      help='Prompt for cat image generation')
    parser.add_argument('--text-overlay', default=DEFAULT_TEXT_OVERLAY,
                      help='Text to overlay on the image')
    parser.add_argument('--music-prompt', default=DEFAULT_MUSIC_PROMPT,
                      help='Prompt for music generation')
    parser.add_argument('--output-dir', default='output',
                      help='Output directory for generated files')
    
    args = parser.parse_args()
    
    # Update output directory if specified
    global OUTPUT_DIR
    OUTPUT_DIR = Path(args.output_dir)
    
    # Check required environment variables
    required_env_vars = ['ANTHROPIC_API_KEY', 'FAL_KEY', 'GOOGLE_APPLICATION_CREDENTIALS']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    # Initialize generator and run workflow
    generator = MediaGenerator()
    results = generator.generate_media_workflow(
        args.image_prompt,
        args.text_overlay,
        args.music_prompt
    )
    
    print("\n🎉 Media generation completed successfully!")
    print(f"📁 Generated files: {len(results['generated_files'])}")
    for file_type, path in results['generated_files'].items():
        print(f"  - {file_type}: {path}")

if __name__ == "__main__":
    main()