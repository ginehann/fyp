import os
import subprocess

def record_stream(stream_url, datetime, cwd, duration):
    resolution = "640x480"  # Set resolution to 640x480
    
    if not os.path.isdir(f"{cwd}/recordings/{datetime}"):
        os.makedirs(f"{cwd}/recordings/{datetime}")
    
    print("Recording stream...")
    # Run ffmpeg command to record stream with specified settings
    subprocess.run(["ffmpeg", "-i", stream_url, "-t", duration, "-s", resolution, "-c", "copy", "-an", f"{cwd}/recordings/{datetime}/{datetime}-s.mp4"])
    subprocess.run(["ffmpeg", "-i", f"{cwd}/recordings/{datetime}/{datetime}-s.mp4", "-vf", "fps=15.83", f"{cwd}/recordings/{datetime}/{datetime}.mp4"])
    print("Recording done.")
