#!/usr/bin/env python3
import os
from moviepy import VideoFileClip, AudioFileClip

# File paths
video_path = "hailuo_02_20250706_164018.mp4"
audio_path = "lyria_output_6ddEkayHR.wav"
output_path = "final_cat_video_with_music.mp4"

print("Loading video file...")
# Load video clip
video = VideoFileClip(video_path)

print("Loading audio file...")
# Load audio clip
audio = AudioFileClip(audio_path)

# Get video duration
video_duration = video.duration
print(f"Video duration: {video_duration:.2f} seconds")
print(f"Audio duration: {audio.duration:.2f} seconds")

# Trim audio to match video duration if needed
if audio.duration > video_duration:
    audio = audio.subclipped(0, video_duration)
    print(f"Audio trimmed to {video_duration:.2f} seconds")

# Set audio to video
print("Combining video and audio...")
final_video = video.with_audio(audio)

# Write the final video
print("Writing final video...")
final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')

print(f"Final video saved as: {output_path}")

# Clean up
video.close()
audio.close()
final_video.close()