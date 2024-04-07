import subprocess
import threading
import json

import googleapiclient.discovery
import yt_dlp as youtube_dl
import pyaudio
import wave


from API_KEYS import YOUTUBE_API_KEY

from Modules.Setup.Config.config import AiName
from Modules.Setup.VoiceBox.VoiceBoxSetup import getVoiceBox
from Modules.Setup.Config.Commands import ValidCommand,evaluateInput


paused = False
stop_requested = False

# Function to search for videos using the YouTube Data API
def search_videos(query, api_key, max_results=1):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        videos.append({
            "title": item["snippet"]["title"],
            "video_id": item["id"]["videoId"]
        })

    return videos

# Function to download audio of a video using youtube_dl
def download_audio(video_id):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # Adjust quality as needed
        }],
        'keepvideo': False
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=True)
        audio_filename = ydl.prepare_filename(info)
    mp3_filename = audio_filename.rsplit(".", 1)[0] + ".mp3"
    return mp3_filename

def convert_to_wav(mp3_file, wav_file):
    subprocess.run(['ffmpeg', '-i', mp3_file, '-acodec', 'pcm_s16le', '-ar', '44100', wav_file])

def play_audio(audio_file):
    global paused, stop_requested

    CHUNK = 1024

    wav_file = audio_file.replace('.mp3', '.wav')
    convert_to_wav(audio_file, wav_file)

    wf = wave.open(wav_file, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data and not stop_requested:
        if not paused:
            stream.write(data)
            data = wf.readframes(CHUNK)
        else:
            # If paused, sleep for a short duration to reduce CPU usage
            threading.Event().wait(0.1)

    stream.stop_stream()
    stream.close()

    p.terminate()

def toggle_pause():
    global paused
    paused = not paused

def toggle_stop():
    global stop_requested
    stop_requested = True

def YoutubePlayer(recognizer, stream, nlpModel, tfidf_vectorizer):
    try:
        # Example search query
        query = ""
        engine = getVoiceBox()
        engine.say("What do you want to play?")
        engine.runAndWait()

        while True:
            data = stream.read(2000)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                resultMap = json.loads(result.lower())
                print(resultMap['text'])
                break

        # Search for videos
        videos = search_videos(query, YOUTUBE_API_KEY)

        if len(videos) > 0:
            top_video = videos[0]
            title = top_video["title"]
            engine.say(f"Downloading audio of top search result: {title}")
            engine.runAndWait()
            audio_file = download_audio(top_video["video_id"])
            engine.say("Playing audio...")
            engine.runAndWait()

            # Start the audio playback in a separate thread
            audio_thread = threading.Thread(target=play_audio, args=(audio_file,))
            audio_thread.start()

            # Loop to listen for user input
            while True:
                data = stream.read(2000)
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    resultMap = json.loads(result.lower())
                    print(resultMap['text'])
                    if ValidCommand(resultMap["text"]):
                        output = evaluateInput(resultMap["text"], nlpModel, tfidf_vectorizer)
                        if output == 'Pause':
                            toggle_pause()
                        elif output == 'Resume':
                            toggle_pause()
                        elif output == "Exit":
                            toggle_stop()
                            break

            # Wait for the audio thread to finish
            engine.say("Exiting YouTube player")
            engine.runAndWait()
            global paused
            paused = False
            global stop_requested
            stop_requested = False
            audio_thread.join()

        else:
            engine.say("No videos found for the search query.")
            engine.runAndWait()

    except Exception as e:
        engine.say("Failed to retrieve song data. Check your wifi connection")
        print(e)
        engine.runAndWait()
