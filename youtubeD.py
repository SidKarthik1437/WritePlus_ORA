from pytube import YouTube
YouTube('https://www.youtube.com/watch?v=cQ1YOzDjZwc').streams.filter(only_audio=True).first().download()
# yt = YouTube('https://www.youtube.com/watch?v=cQ1YOzDjZwc')
# yt.streams.filter(only_audio=True).download()