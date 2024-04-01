import googleapiclient.discovery
import yt_dlp as youtube_dl
from pydub import AudioSegment
from pydub.playback import play
from API_KEYS import YOUTUBE_API_KEY

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
        'keepvideo': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=True)
        audio_filename = ydl.prepare_filename(info)
    mp3_filename = audio_filename.rsplit(".", 1)[0] + ".mp3"
    return mp3_filename

# Function to play audio using pydub
def play_audio(audio_file):
    sound = AudioSegment.from_file(audio_file)
    play(sound)
 
def main():
    # Example search query
    query = "khantrast i need ya"

    # Search for videos
    videos = search_videos(query, YOUTUBE_API_KEY)

    if len(videos) > 0:
        top_video = videos[0]
        print("Downloading audio of top search result:", top_video["title"])
        audio_file = download_audio(top_video["video_id"])
        print("Audio downloaded.")
        print("Playing audio...")
        play_audio(audio_file)

    else:
        print("No videos found for the search query.")

if __name__ == "__main__":
    main()