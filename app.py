from flask import Flask, render_template, request
import pandas as pd
import random  

app = Flask(__name__)

df = pd.read_csv('YoutubeVideoDataset.csv')

# Function to construct the complete YouTube URL
def construct_youtube_url(video_id):
    return f'https://www.youtube.com/watch?v={video_id}'

# Add a new column with the complete YouTube URL
df['CompleteURL'] = df['Videourl'].apply(lambda video_id: construct_youtube_url(video_id))

# Function to extract video ID from the URL
def extract_video_id(url):
    try:
        video_id = url.split('=')[-1]
        return video_id
    except:
        return None

# Add a new column with the embed URL
df['EmbedURL'] = df['CompleteURL'].apply(lambda url: f'https://www.youtube.com/embed/{extract_video_id(url)}')

@app.route('/')
def index():
    # Shuffle the DataFrame rows to display videos in a random order
    shuffled_df = df.sample(frac=1, random_state=42)  # Use a fixed random_state for consistency

    # Get the page number from the request or set it to 1
    page = int(request.args.get('page', 1))
    # Set the number of videos to display per page
    videos_per_page = 20
    # Calculate the start and end indices for the videos to display
    start_idx = (page - 1) * videos_per_page
    end_idx = start_idx + videos_per_page
    # Get the videos for the current page from the shuffled DataFrame
    current_videos = shuffled_df.iloc[start_idx:end_idx]

    return render_template('index.html', videos=current_videos.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)

