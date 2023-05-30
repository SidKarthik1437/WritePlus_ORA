import regex as re

def extract_video_ids_from_file(file_path):
    # Function to extract video ID from a YouTube link
    def extract_video_id(link):
        regex = r"(?<=v=|v\/|vi=|vi\/|youtu.be\/|embed\/|\/v\/|\/e\/|watch\?v=|\?v=|\/embed\/|\/e\/|youtu.be\/|\/v\/|watch\?v=|embed\/)[^#\\?\\&]*"
        match = re.search(regex, link)
        if match:
            return match.group(0)
        else:
            return None

    # Read the text file containing YouTube links
    with open(file_path, "r") as file:
        youtube_links = file.readlines()

    # Extract video IDs from the links
    video_ids = []
    for link in youtube_links:
        video_id = extract_video_id(link)
        if video_id:
            video_ids.append(video_id)

    return video_ids
