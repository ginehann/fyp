import os
import subprocess


def record_stream(stream_url, datetime, cwd, duration): # cwd = file directory
    resolution = "640x480"  # Set resolution to 640x480
    
    # create file with current datetime as name
    if not os.path.isdir(f"{cwd}/recordings/{datetime}"):
        os.makedirs(f"{cwd}/recordings/{datetime}")
    
    print("Recording stream...")
    # Run ffmpeg command to record stream...
    subprocess.run(["ffmpeg", "-i", stream_url, "-t", duration, "-s", resolution, "-c", "copy", "-an", f"{cwd}/recordings/{datetime}/{datetime}-s.mp4"])
    # then process it so that it has specified setting and runs in real time.
    subprocess.run(["ffmpeg", "-i", f"{cwd}/recordings/{datetime}/{datetime}-s.mp4", "-ss", "0:00:00", "-t", "00:02:00", "-vf", "fps=15.83,setpts=1.25*PTS", f"{cwd}/recordings/{datetime}/{datetime}.mp4"])
    print("Recording done.")

    
