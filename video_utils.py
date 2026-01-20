import subprocess
import os

def extract_audio_from_video(video_path, output_audio="extracted_audio.wav"):
    if os.path.exists(output_audio):
        os.remove(output_audio)

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        output_audio
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_audio
