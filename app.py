import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from datetime import datetime, timedelta
import numpy as np
from collections import Counter
import isodate
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import altair as alt
from streamlit_lottie import st_lottie
import json
import requests
from io import BytesIO
import base64
from PIL import Image
from textblob import TextBlob
from dotenv import load_dotenv
import time
import numpy as np
# Set page configuration
st.set_page_config(
    page_title="YouTube Analytics Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load animation
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Custom CSS with modern design
st.markdown("""
    <style>
    /* Main Theme Colors */
    :root {
        --primary: #FF0000;
        --secondary: #282828;
        --accent: #065FD4;
        --light-bg: #f8f9fa;
        --dark-bg: #212529;
        --success: #28a745;
        --warning: #ffc107;
        --info: #17a2b8;
    }
    
    /* Main Header Styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FF0000, #FF5607);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1.5rem;
        padding-top: 1rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sub Headers */
    .sub-header {
        font-size: 1.8rem;
        color: #444;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #eee;
    }
    
    /* Cards for Metrics */
    .metric-card {
        background-color: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.12);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Chart Container */
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 16px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 0, 0, 0.1);
        border-radius: 5px 5px 0 0;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #333;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: var(--primary);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #D10000;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 0, 0, 0.2);
    }
    
    /* Progress styling */
    .stProgress > div > div > div > div {
        background-color: var(--primary);
    }
    
    /* Image styling */
    .thumbnail-image {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }
    
    .thumbnail-image:hover {
        transform: scale(1.03);
    }
    
    /* Table styling */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .dataframe thead tr {
        background-color: #f8f9fa;
    }
    
    .dataframe th {
        padding: 12px 15px;
        text-align: left;
        font-weight: 600;
        color: #333;
        border-bottom: 2px solid #eee;
    }
    
    .dataframe tbody tr {
        border-bottom: 1px solid #eee;
    }
    
    .dataframe td {
        padding: 10px 15px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding-top: 2rem;
        padding-bottom: 1rem;
        font-size: 0.9rem;
        color: #666;
    }
    
    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25em 0.6em;
        font-size: 0.8rem;
        font-weight: 600;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 10px;
        margin-right: 5px;
    }
    
    .badge-primary {
        background-color: var(--primary);
        color: white;
    }
    
    .badge-secondary {
        background-color: var(--secondary);
        color: white;
    }
    
    .badge-success {
        background-color: var(--success);
        color: white;
    }
    
    .badge-warning {
        background-color: var(--warning);
        color: black;
    }
    
    .badge-info {
        background-color: var(--info);
        color: white;
    }
    
    /* KPI Cards styling */
    .kpi-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .kpi-card {
        flex: 1;
        background-color: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #303030;
        margin-bottom: 0;
    }
    
    .kpi-label {
        font-size: 1rem;
        font-weight: 500;
        color: #666;
        margin-top: 0.5rem;
    }
    
    .kpi-trend {
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .trend-up {
        color: var(--success);
    }
    
    .trend-down {
        color: var(--primary);
    }
    
    /* Divider */
    .divider {
        width: 100%;
        height: 1px;
        background-color: #eee;
        margin: 2rem 0;
    }
    
    /* Custom select */
    .stSelectbox > div > div > div {
        background-color: white;
        border-radius: 50px !important;
        border: 1px solid #ddd !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Add SVG logo
def get_youtube_logo():
    youtube_logo = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 20" width="90" height="20">
      <path d="M27.9727 3.12324C27.6435 1.89323 26.6768 0.926623 25.4468 0.597366C23.2197 2.24288e-07 14.285 0 14.285 0C14.285 0 5.35042 2.24288e-07 3.12323 0.597366C1.89323 0.926623 0.926623 1.89323 0.597366 3.12324C2.24288e-07 5.35042 0 10 0 10C0 10 2.24288e-07 14.6496 0.597366 16.8768C0.926623 18.1068 1.89323 19.0734 3.12323 19.4026C5.35042 20 14.285 20 14.285 20C14.285 20 23.2197 20 25.4468 19.4026C26.6768 19.0734 27.6435 18.1068 27.9727 16.8768C28.5701 14.6496 28.5701 10 28.5701 10C28.5701 10 28.5677 5.35042 27.9727 3.12324Z" fill="#FF0000"/>
      <path d="M11.4253 14.2854L18.8477 10.0004L11.4253 5.71533V14.2854Z" fill="white"/>
      <path d="M34.6024 13.0036L31.3945 1.41846H34.1932L35.3174 6.6701C35.6043 7.96361 35.8136 9.06662 35.95 9.97913H36.0323C36.1264 9.32532 36.3381 8.22937 36.665 6.68892L37.8291 1.41846H40.6278L37.3799 13.0036V18.561H34.6001V13.0036H34.6024Z" fill="black"/>
      <path d="M41.4697 18.1937C40.9053 17.8127 40.5031 17.22 40.2632 16.4157C40.0257 15.6114 39.9058 14.5437 39.9058 13.2078V11.3898C39.9058 10.0422 40.0422 8.95805 40.315 8.14196C40.5878 7.32588 41.0135 6.72851 41.592 6.35457C42.1706 5.98063 42.9302 5.79248 43.871 5.79248C44.7976 5.79248 45.5384 5.98298 46.0981 6.36398C46.6555 6.74497 47.0647 7.34234 47.3234 8.15137C47.5821 8.96275 47.7115 10.0422 47.7115 11.3898V13.2078C47.7115 14.5437 47.5845 15.6161 47.3329 16.4251C47.0812 17.2365 46.672 17.8292 46.1075 18.2031C45.5431 18.5771 44.7764 18.7652 43.8098 18.7652C42.8126 18.7675 42.0342 18.5747 41.4697 18.1937ZM44.6353 16.2323C44.7905 15.8231 44.8705 15.1575 44.8705 14.2309V10.3292C44.8705 9.43077 44.7929 8.77225 44.6353 8.35833C44.4777 7.94206 44.2026 7.7351 43.8074 7.7351C43.4265 7.7351 43.156 7.94206 43.0008 8.35833C42.8432 8.77461 42.7656 9.43077 42.7656 10.3292V14.2309C42.7656 15.1575 42.8408 15.8254 42.9914 16.2323C43.1419 16.6415 43.4123 16.8461 43.8074 16.8461C44.2026 16.8461 44.4777 16.6415 44.6353 16.2323Z" fill="black"/>
      <path d="M56.8154 18.5634H54.6094L54.3648 17.03H54.3037C53.7039 18.1871 52.8055 18.7656 51.6061 18.7656C50.7759 18.7656 50.1621 18.4928 49.767 17.9496C49.3719 17.4039 49.1743 16.5526 49.1743 15.3955V6.03751H51.9942V15.2308C51.9942 15.7906 52.0553 16.188 52.1776 16.4256C52.2999 16.6631 52.5045 16.783 52.7914 16.783C53.036 16.783 53.2712 16.7078 53.497 16.5573C53.7228 16.4067 53.8874 16.2162 53.9979 15.9858V6.03516H56.8154V18.5634Z" fill="black"/>
      <path d="M64.4755 3.68758H61.6768V18.5629H58.9181V3.68758H56.1194V1.42041H64.4755V3.68758Z" fill="black"/>
      <path d="M71.2768 18.5634H69.0708L68.8262 17.03H68.7651C68.1654 18.1871 67.267 18.7656 66.0675 18.7656C65.2373 18.7656 64.6235 18.4928 64.2284 17.9496C63.8333 17.4039 63.6357 16.5526 63.6357 15.3955V6.03751H66.4556V15.2308C66.4556 15.7906 66.5167 16.188 66.639 16.4256C66.7613 16.6631 66.9659 16.783 67.2529 16.783C67.4974 16.783 67.7326 16.7078 67.9584 16.5573C68.1842 16.4067 68.3488 16.2162 68.4593 15.9858V6.03516H71.2768V18.5634Z" fill="black"/>
      <path d="M80.609 8.0387C80.4373 7.24849 80.1621 6.67699 79.7812 6.32186C79.4002 5.96674 78.8757 5.79035 78.2078 5.79035C77.6904 5.79035 77.2059 5.93616 76.7567 6.23014C76.3075 6.52412 75.9594 6.90747 75.7148 7.38489H75.6937V0.785645H72.9773V18.5608H75.3056L75.5925 17.3755H75.6537C75.8724 17.7988 76.1993 18.1304 76.6344 18.3774C77.0695 18.622 77.554 18.7443 78.0855 18.7443C79.038 18.7443 79.7412 18.3045 80.1904 17.4272C80.6396 16.5476 80.8653 15.1765 80.8653 13.3092V11.3266C80.8653 9.92722 80.7783 8.82892 80.609 8.0387ZM78.0243 13.1492C78.0243 14.0617 77.9867 14.7767 77.9114 15.2941C77.8362 15.8115 77.7115 16.1808 77.5328 16.3971C77.3564 16.6158 77.1165 16.724 76.8178 16.724C76.585 16.724 76.371 16.6699 76.1734 16.5594C75.9759 16.4512 75.816 16.2866 75.6937 16.0702V8.96062C75.7877 8.6196 75.9524 8.34209 76.1852 8.12337C76.4157 7.90465 76.6697 7.79646 76.9401 7.79646C77.2271 7.79646 77.4481 7.90935 77.6034 8.13278C77.7609 8.35855 77.8691 8.73485 77.9303 9.26636C77.9914 9.79787 78.022 10.5528 78.022 11.5335V13.1492H78.0243Z" fill="black"/>
      <path d="M84.8657 13.8712C84.8657 14.6755 84.8892 15.2776 84.9363 15.6798C84.9833 16.0819 85.0821 16.3736 85.2326 16.5594C85.3831 16.7428 85.6136 16.8345 85.9264 16.8345C86.3474 16.8345 86.639 16.6699 86.8022 16.343C86.9677 16.016 87.0497 15.4705 87.0497 14.7085V13.8712H89.4886V14.7085C89.4886 16.2153 89.1481 17.3397 88.4694 18.0812C87.7906 18.8252 86.8142 19.1952 85.5402 19.1952C84.1674 19.1952 83.1744 18.7405 82.5667 17.8335C81.9568 16.9265 81.6518 15.4705 81.6518 13.4675V11.1605C81.6518 9.28387 81.9756 7.86812 82.6233 6.9034C83.2711 5.94107 84.3015 5.4584 85.7159 5.4584C87.0119 5.4584 87.9894 5.86553 88.6484 6.67919C89.3073 7.49285 89.6368 8.84481 89.6368 10.7309V12.5932H84.8657V13.8712ZM85.2232 7.96811C85.0797 8.14449 84.9857 8.43377 84.9363 8.83593C84.8892 9.2381 84.8657 9.84722 84.8657 10.6657V10.7779H86.7759V10.6657C86.7759 9.86133 86.7406 9.25221 86.6723 8.83593C86.604 8.41966 86.4943 8.12803 86.3427 7.95635C86.1911 7.78702 85.9779 7.7 85.7066 7.7C85.4667 7.70235 85.3144 7.79175 85.2232 7.96811Z" fill="black"/>
    </svg>
    """
    return youtube_logo

# Helper functions for data processing and visualization
def fetch_youtube_data(api_key, channel_id):
    """Fetch data from YouTube API with enhanced error handling"""
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Get channel information
        channel_response = youtube.channels().list(
            part="snippet,contentDetails,statistics,brandingSettings",
            id=channel_id
        ).execute()
        
        if not channel_response['items']:
            st.error(f"Channel with ID {channel_id} not found.")
            return None, None, None
        
        channel_data = channel_response['items'][0]
        
        # Get channel banner URL if available
        banner_url = channel_data.get('brandingSettings', {}).get('image', {}).get('bannerExternalUrl', '')
        
        # Extract relevant channel data
        channel_stats = {
            'Channel Name': channel_data['snippet']['title'],
            'Channel ID': channel_id,
            'Subscribers': int(channel_data['statistics'].get('subscriberCount', 0)),
            'Views': int(channel_data['statistics'].get('viewCount', 0)),
            'Total Videos': int(channel_data['statistics'].get('videoCount', 0)),
            'Channel Created': channel_data['snippet']['publishedAt'],
            'Playlist ID': channel_data['contentDetails']['relatedPlaylists']['uploads'],
            'Description': channel_data['snippet'].get('description', ''),
            'Country': channel_data['snippet'].get('country', 'Not specified'),
            'Banner URL': banner_url,
            'Thumbnail URL': channel_data['snippet']['thumbnails'].get('high', {}).get('url', '')
        }
        
        # Get video IDs from uploads playlist
        video_ids = []
        next_page_token = None
        
        # Limit to 200 videos to avoid quota issues but allow deeper analysis
        max_videos = 200
        
        while True:
            playlist_response = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=channel_stats['Playlist ID'],
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            
            # Get video IDs
            for item in playlist_response['items']:
                video_ids.append(item['contentDetails']['videoId'])
                if len(video_ids) >= max_videos:
                    break
                    
            # Check if we've reached our limit or there are more pages
            if len(video_ids) >= max_videos:
                break
                
            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break
                
        # Get video details in batches
        all_video_data = []
        
        # Process in batches of 50 (API limit)
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i+50]
            
            video_response = youtube.videos().list(
                part="snippet,contentDetails,statistics,topicDetails",
                id=','.join(batch_ids)
            ).execute()
            
            for video in video_response['items']:
                # Extract relevant data with enhanced fields
                video_data = {
                    'Video ID': video['id'],
                    'Title': video['snippet']['title'],
                    'Published Date': video['snippet']['publishedAt'],
                    'Description': video['snippet']['description'],
                    'Tags': video['snippet'].get('tags', []),
                    'Category ID': video['snippet'].get('categoryId', ''),
                    'Duration': video['contentDetails']['duration'],
                    'Views': int(video['statistics'].get('viewCount', 0)),
                    'Likes': int(video['statistics'].get('likeCount', 0)),
                    'Comments': int(video['statistics'].get('commentCount', 0)),
                    'Thumbnail URL': video['snippet']['thumbnails'].get('high', {}).get('url', ''),
                    'Topics': video.get('topicDetails', {}).get('topicCategories', []),
                    'HD': video['contentDetails'].get('definition', '') == 'hd',
                    'Caption': video['contentDetails'].get('caption', '') == 'true'
                }
                
                all_video_data.append(video_data)
                
        # Get up to 20 comments from top videos to analyze sentiment
        top_video_ids = sorted(all_video_data, key=lambda x: x['Views'], reverse=True)[:5]
        comment_data = []
        
        for video in top_video_ids:
            try:
                comment_response = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video['Video ID'],
                    maxResults=20,
                    order="relevance"
                ).execute()
                
                for item in comment_response.get('items', []):
                    comment = {
                        'Video ID': video['Video ID'],
                        'Video Title': video['Title'],
                        'Comment': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                        'Author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        'Likes': item['snippet']['topLevelComment']['snippet']['likeCount'],
                        'Published At': item['snippet']['topLevelComment']['snippet']['publishedAt']
                    }
                    comment_data.append(comment)
            except:
                # Some videos might have comments disabled
                pass
                
        return channel_stats, all_video_data, comment_data
        
    except HttpError as e:
        error_details = json.loads(e.content)
        error_reason = error_details.get('error', {}).get('errors', [{}])[0].get('reason', '')
        
        if error_reason == 'quotaExceeded':
            st.error("YouTube API quota exceeded. Please try again tomorrow or use a different API key.")
        elif error_reason == 'keyInvalid':
            st.error("Invalid API key. Please check your API key and try again.")
        else:
            st.error(f"An HTTP error occurred: {e}")
        return None, None, None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None, None

def enhance_video_data(video_data):
    """Process and enhance video data with advanced metrics"""
    # Convert to DataFrame
    df = pd.DataFrame(video_data)
    
    # Convert date strings to datetime objects
    df['Published Date'] = pd.to_datetime(df['Published Date'])
    
    # Process duration (convert ISO 8601 duration to seconds)
    df['Duration (sec)'] = df['Duration'].apply(lambda x: isodate.parse_duration(x).total_seconds())
    
    # Add duration categories
    df['Duration Category'] = pd.cut(
        df['Duration (sec)'], 
        bins=[0, 60, 300, 600, 1200, 1800, 3600, float('inf')],
        labels=['< 1 min', '1-5 min', '5-10 min', '10-20 min', '20-30 min', '30-60 min', '> 60 min']
    )
    
    # Calculate days since publishing - With timezone handling
    df['Days Since Published'] = (datetime.now() - df['Published Date'].dt.tz_localize(None)).dt.days
    
    # Calculate daily views and growth metrics
    df['Daily Views'] = df['Views'] / df['Days Since Published'].replace(0, 1)  # Avoid division by zero
    df['Daily Views'] = df['Daily Views'].fillna(0).round(2)
    
    # Calculate engagement metrics
    df['Engagement Rate'] = ((df['Likes'] + df['Comments']) / df['Views'] * 100).round(2)
    df['Likes per View'] = (df['Likes'] / df['Views'] * 100).round(2)
    df['Comments per View'] = (df['Comments'] / df['Views'] * 100).round(2)
    df['Like-Comment Ratio'] = (df['Likes'] / df['Comments'].replace(0, 1)).round(2)
    
    # Time-based metrics
    df['Hour Published'] = df['Published Date'].dt.hour
    df['Time Category'] = pd.cut(
        df['Hour Published'],
        bins=[0, 6, 12, 18, 24],
        labels=['Night (0-6)', 'Morning (6-12)', 'Afternoon (12-18)', 'Evening (18-24)']
    )
    df['Publish Day of Week'] = df['Published Date'].dt.day_name()
    df['Publish Year'] = df['Published Date'].dt.year
    df['Publish Month'] = df['Published Date'].dt.month
    df['Publish Day'] = df['Published Date'].dt.day
    df['Year-Month'] = df['Published Date'].dt.strftime('%Y-%m')
    df['Month Name'] = df['Published Date'].dt.month_name()
    # Extract title features
    df['Title Length'] = df['Title'].apply(len)
    df['Title Word Count'] = df['Title'].apply(lambda x: len(str(x).split()))
    
    # Add question mark detection
    df['Has Question'] = df['Title'].apply(lambda x: '?' in str(x))
    
    # Add number detection (e.g., "Top 10", "5 Ways")
    df['Has Number'] = df['Title'].apply(lambda x: bool(re.search(r'\d+', str(x))))
    
    # Add uppercase detection (e.g., "NEW", "BEST")
    df['Has Uppercase Word'] = df['Title'].apply(lambda x: bool(re.search(r'\b[A-Z]{2,}\b', str(x))))
    
    # Extract common words from titles (excluding stopwords)
    stopwords = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'of', 'is', 'are', 'how', 'what', 'why', 'when', 'where', 'who', 'this', 'that', 'these', 'those', 'my', 'your', 'our', 'their'}
    df['Title Words'] = df['Title'].apply(lambda x: [word.lower() for word in re.findall(r'\w+', str(x)) if word.lower() not in stopwords])
    
    # Add description metrics
    df['Description Length'] = df['Description'].apply(len)
    df['Has Description'] = df['Description Length'] > 10
    
    # Add tag metrics
    df['Tag Count'] = df['Tags'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    df['Has Tags'] = df['Tag Count'] > 0
    
    # Calculate days between uploads
    df_sorted = df.sort_values('Published Date')
    df_sorted['Days Since Last Upload'] = (df_sorted['Published Date'] - df_sorted['Published Date'].shift(1)).dt.days
    # Merge back to original dataframe
    df = df.merge(df_sorted[['Video ID', 'Days Since Last Upload']], on='Video ID', how='left')
    
    # Detect thumbnail patterns (have numbers, faces, etc)
    df['Thumbnail Has Number'] = df['Thumbnail URL'].notna()  # Placeholder - would need image analysis
    
    # Seasonality - quarter
    df['Quarter'] = df['Published Date'].dt.quarter
    
    # Video age categories
    df['Age Category'] = pd.cut(
        df['Days Since Published'],
        bins=[0, 7, 30, 90, 365, float('inf')],
        labels=['< 1 week', '1-4 weeks', '1-3 months', '3-12 months', '> 1 year']
    )
    
    # Performance categorization
    df['Views Performance'] = pd.qcut(df['Views'], q=4, labels=['Low', 'Medium', 'High', 'Viral'], duplicates='drop')
    df['Engagement Performance'] = pd.qcut(df['Engagement Rate'].clip(lower=0.01), q=4, labels=['Low', 'Medium', 'High', 'Exceptional'], duplicates='drop')
    
    # Velocity metrics
    df['View Velocity'] = df['Views'] / (df['Days Since Published'].replace(0, 1))
    df['Comment Velocity'] = df['Comments'] / (df['Days Since Published'].replace(0, 1))
    
    # Weekly performance
    df['Week Number'] = df['Published Date'].dt.isocalendar().week
    
    # Popular topics (from titles)
    topic_words = ['how', 'tutorial', 'review', 'top', 'best', 'vs', 'guide', 'tips', 'challenge', 'unboxing']
    for topic in topic_words:
        df[f'Topic_{topic}'] = df['Title'].str.lower().str.contains(topic, na=False)
    
    return df

def enhance_channel_data(channel_stats, video_df):
    """Add additional metrics to channel stats"""
    enhanced_stats = channel_stats.copy()
    
    # Calculate channel age in days
    created_date = pd.to_datetime(channel_stats['Channel Created'])
    enhanced_stats['Age Days'] = (datetime.now() - created_date.replace(tzinfo=None)).days
    
    # Calculate views per subscriber
    enhanced_stats['Views per Subscriber'] = round(channel_stats['Views'] / max(channel_stats['Subscribers'], 1), 2)
    
    # Calculate average views per video
    enhanced_stats['Avg Views per Video'] = round(channel_stats['Views'] / max(channel_stats['Total Videos'], 1), 2)
    
    # Calculate growth metrics from video data if available
    if video_df is not None and not video_df.empty:
        # Average engagement rate
        enhanced_stats['Avg Engagement Rate'] = video_df['Engagement Rate'].mean()
        
        # Upload frequency (days between uploads)
        enhanced_stats['Avg Upload Interval'] = video_df['Days Since Last Upload'].mean()
        
        # Videos per month
        enhanced_stats['Videos per Month'] = (video_df.shape[0] / (enhanced_stats['Age Days'] / 30))
        
        # Most popular video
        top_video = video_df.loc[video_df['Views'].idxmax()]
        enhanced_stats['Top Video Title'] = top_video['Title']
        enhanced_stats['Top Video Views'] = int(top_video['Views'])
        
        # Typical video duration
        enhanced_stats['Median Video Duration'] = video_df['Duration (sec)'].median()
        
        # Publishing patterns
        enhanced_stats['Most Common Publish Day'] = video_df['Publish Day of Week'].mode()[0]
        enhanced_stats['Most Common Publish Hour'] = video_df['Hour Published'].mode()[0]
        
    return enhanced_stats

def analyze_comments(comment_data):
    """Analyze comment sentiment using TextBlob"""
    if not comment_data:
        return pd.DataFrame()
        
    df = pd.DataFrame(comment_data)
    
    # Convert date strings to datetime objects
    df['Published At'] = pd.to_datetime(df['Published At'])
    
    # Add sentiment analysis
    df['Sentiment'] = df['Comment'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['Sentiment Category'] = pd.cut(
        df['Sentiment'],
        bins=[-1.1, -0.3, 0.3, 1.1],
        labels=['Negative', 'Neutral', 'Positive']
    )
    
    # Add comment length metrics
    df['Comment Length'] = df['Comment'].apply(len)
    
    return df

def create_wordcloud(df, column='Title Words', background='white'):
    """Create word cloud from specified column"""
    all_words = []
    for word_list in df[column]:
        if isinstance(word_list, list):
            all_words.extend(word_list)
        elif isinstance(word_list, str):
            try:
                # Try to parse the string as a list
                word_list = eval(word_list)
                if isinstance(word_list, list):
                    all_words.extend(word_list)
            except:
                pass
    
    word_counts = Counter(all_words)
    
    # Create word cloud
    if word_counts:
        wc = WordCloud(width=800, height=400, background_color=background, 
                       max_words=100, colormap='viridis', 
                       contour_width=1, contour_color='steelblue')
        wc.generate_from_frequencies(word_counts)
        
        return wc
    return None

def get_category_name(category_id):
    """Map YouTube category IDs to names"""
    category_map = {
        '1': 'Film & Animation',
        '2': 'Autos & Vehicles',
        '10': 'Music',
        '15': 'Pets & Animals',
        '17': 'Sports',
        '18': 'Short Movies',
        '19': 'Travel & Events',
        '20': 'Gaming',
        '21': 'Videoblogging',
        '22': 'People & Blogs',
        '23': 'Comedy',
        '24': 'Entertainment',
        '25': 'News & Politics',
        '26': 'Howto & Style',
        '27': 'Education',
        '28': 'Science & Technology',
        '29': 'Nonprofits & Activism',
        '30': 'Movies',
        '31': 'Anime/Animation',
        '32': 'Action/Adventure',
        '33': 'Classics',
        '34': 'Comedy',
        '35': 'Documentary',
        '36': 'Drama',
        '37': 'Family',
        '38': 'Foreign',
        '39': 'Horror',
        '40': 'Sci-Fi/Fantasy',
        '41': 'Thriller',
        '42': 'Shorts',
        '43': 'Shows',
        '44': 'Trailers'
    }
    return category_map.get(str(category_id), 'Unknown')

def format_duration(seconds):
    """Format seconds to HH:MM:SS"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    elif minutes > 0:
        return f"{int(minutes)}m {int(seconds)}s"
    else:
        return f"{int(seconds)}s"

def load_data_from_files():
    """Load data from CSV files if they exist"""
    try:
        if os.path.exists('channel_stats.csv') and os.path.exists('video_data.csv'):
            channel_df = pd.read_csv('channel_stats.csv')
            video_df = pd.read_csv('video_data.csv')
            
            # Convert to expected format
            channel_stats = channel_df.iloc[0].to_dict() if not channel_df.empty else None
            video_data = video_df.to_dict('records') if not video_df.empty else None
            
            # Load comments if available
            comment_data = None
            if os.path.exists('comment_data.csv'):
                comment_df = pd.read_csv('comment_data.csv')
                comment_data = comment_df.to_dict('records') if not comment_df.empty else None
            
            return channel_stats, video_data, comment_data
        return None, None, None
    except Exception as e:
        st.error(f"Error loading data from files: {e}")
        return None, None, None

def save_data_to_files(channel_stats, video_data, comment_data=None):
    """Save data to CSV files"""
    try:
        if channel_stats:
            channel_df = pd.DataFrame([channel_stats])
            channel_df.to_csv('channel_stats.csv', index=False)
            
        if video_data:
            video_df = pd.DataFrame(video_data)
            video_df.to_csv('video_data.csv', index=False)
            
        if comment_data:
            comment_df = pd.DataFrame(comment_data)
            comment_df.to_csv('comment_data.csv', index=False)
            
    except Exception as e:
        st.error(f"Error saving data to files: {e}")

def generate_recommendations(enhanced_df, channel_stats):
    """Generate actionable insights based on data analysis"""
    recommendations = []
    
    # Check publishing frequency
    if channel_stats.get('Videos per Month', 0) < 4:
        recommendations.append({
            'category': 'Frequency',
            'recommendation': 'Consider increasing upload frequency to at least once per week',
            'impact': 'High',
            'icon': '📅'
        })
    
    # Check video length
    duration_performance = enhanced_df.groupby('Duration Category')['Views'].mean().sort_values(ascending=False)
    if not duration_performance.empty:
        top_duration = duration_performance.index[0]
        recommendations.append({
            'category': 'Duration',
            'recommendation': f'Your videos in the {top_duration} range perform best. Consider creating more content of this length.',
            'impact': 'Medium',
            'icon': '⏱'
        })
    
    # Check best publishing day
    day_performance = enhanced_df.groupby('Publish Day of Week')['Views'].mean().sort_values(ascending=False)
    if not day_performance.empty:
        top_day = day_performance.index[0]
        recommendations.append({
            'category': 'Scheduling',
            'recommendation': f'Videos published on {top_day} perform best. Consider scheduling more uploads on this day.',
            'impact': 'Medium',
            'icon': '📊'
        })
    
    # Check title patterns
    if enhanced_df[enhanced_df['Has Number']]['Views'].mean() > enhanced_df[~enhanced_df['Has Number']]['Views'].mean():
        recommendations.append({
            'category': 'Titles',
            'recommendation': 'Titles containing numbers (e.g., "Top 10", "5 Ways") perform better. Consider using more numbered lists.',
            'impact': 'High',
            'icon': '🔢'
        })
    
    # Check engagement
    if enhanced_df['Engagement Rate'].mean() < 5:
        recommendations.append({
            'category': 'Engagement',
            'recommendation': 'Your engagement rate is below average. Consider adding clear calls to action and asking questions to viewers.',
            'impact': 'High',
            'icon': '👍'
        })
    
    # Check tag usage
    if enhanced_df['Tag Count'].mean() < 10:
        recommendations.append({
            'category': 'SEO',
            'recommendation': 'You\'re using fewer tags than recommended. Add more relevant tags to improve discoverability.',
            'impact': 'Medium',
            'icon': '🏷'
        })
    
    # Check description length
    if enhanced_df['Description Length'].mean() < 500:
        recommendations.append({
            'category': 'SEO',
            'recommendation': 'Your descriptions are shorter than recommended. Add detailed descriptions with keywords and links.',
            'impact': 'Medium',
            'icon': '📝'
        })
    
    # Check categorization
    top_categories = enhanced_df.groupby('Category ID').agg({'Views': 'mean'}).sort_values('Views', ascending=False)
    if len(top_categories) > 1:
        top_cat = get_category_name(top_categories.index[0])
        recommendations.append({
            'category': 'Content',
            'recommendation': f'Videos in the "{top_cat}" category perform best. Consider creating more content in this category.',
            'impact': 'Medium',
            'icon': '🎯'
        })
    
    return recommendations

def create_thumbnail_grid(df, num_thumbnails=6):
    """Create a grid of video thumbnails with details"""
    # Sort by views and get top videos
    top_videos = df.sort_values('Views', ascending=False).head(num_thumbnails)
    
    # Create columns for the grid
    cols = st.columns(3)
    
    for i, (_, video) in enumerate(top_videos.iterrows()):
        col_idx = i % 3
        with cols[col_idx]:
            st.markdown(f"""
            <div style="border-radius:15px; padding:10px; margin-bottom:20px; box-shadow:0 4px 10px rgba(0,0,0,0.1); background:white;">
                <img src="{video['Thumbnail URL']}" width="100%" class="thumbnail-image">
                <h4 style="margin-top:10px; margin-bottom:5px; font-size:14px; height:40px; overflow:hidden;">{video['Title']}</h4>
                <p style="margin:0; color:#606060; font-size:12px;">Views: {video['Views']:,}</p>
                <p style="margin:0; color:#606060; font-size:12px;">Published: {video['Published Date'].strftime('%b %d, %Y')}</p>
                <div style="display:flex; justify-content:space-between; margin-top:5px;">
                    <span style="color:#606060; font-size:12px;">👍 {video['Likes']:,}</span>
                    <span style="color:#606060; font-size:12px;">💬 {video['Comments']:,}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

def get_trending_insights(df):
    """Identify trending topics and patterns"""
    insights = []
    
    # Look at recent videos performance compared to average
    recent_videos = df[df['Days Since Published'] <= 30]
    if not recent_videos.empty:
        recent_avg_views = recent_videos['Views'].mean()
        all_avg_views = df['Views'].mean()
        
        if recent_avg_views > all_avg_views * 1.2:
            insights.append({
                'type': 'positive',
                'insight': 'Recent videos are outperforming your channel average by 20%+',
                'icon': '📈'
            })
        elif recent_avg_views < all_avg_views * 0.8:
            insights.append({
                'type': 'negative',
                'insight': 'Recent videos are underperforming compared to your channel average',
                'icon': '📉'
            })
    
    # Look for topics that might be trending
    topic_performance = {}
    for topic in ['Topic_how', 'Topic_tutorial', 'Topic_review', 'Topic_top', 'Topic_best']:
        if topic in df.columns:
            avg_topic_views = df[df[topic]]['Views'].mean()
            avg_non_topic_views = df[~df[topic]]['Views'].mean()
            if avg_topic_views > avg_non_topic_views * 1.3:
                topic_name = topic.replace('Topic_', '')
                insights.append({
                    'type': 'positive',
                    'insight': f'Videos about "{topic_name}" perform 30%+ better than other topics',
                    'icon': '🔥'
                })
    
    # Look at length trends
    duration_performance = df.groupby('Duration Category')['Views'].mean().sort_values(ascending=False)
    if not duration_performance.empty:
        top_duration = duration_performance.index[0]
        insights.append({
            'type': 'info',
            'insight': f'Videos in the {top_duration} range get the most views',
            'icon': '⏱'
        })
    
    # Day of week trends
    day_performance = df.groupby('Publish Day of Week')['Views'].mean().sort_values(ascending=False)
    if not day_performance.empty:
        top_day = day_performance.index[0]
        insights.append({
            'type': 'info',
            'insight': f'Videos published on {top_day} perform best',
            'icon': '📆'
        })
    
    # Engagement trends
    if 'Engagement Rate' in df.columns:
        recent_engagement = df[df['Days Since Published'] <= 30]['Engagement Rate'].mean()
        all_engagement = df['Engagement Rate'].mean()
        
        if recent_engagement > all_engagement * 1.15:
            insights.append({
                'type': 'positive',
                'insight': 'Engagement on recent videos has improved',
                'icon': '👍'
            })
    
    return insights

def parse_duration_data(df):
    """Create bins for duration analysis"""
    # For line charts and distribution analysis
    duration_bins = [0, 60, 120, 180, 240, 300, 600, 900, 1200, 1800, 3600, float('inf')]
    labels = ['0-1m', '1-2m', '2-3m', '3-4m', '4-5m', '5-10m', '10-15m', '15-20m', '20-30m', '30-60m', '60m+']
    
    df['Duration Bin'] = pd.cut(df['Duration (sec)'], bins=duration_bins, labels=labels)
    
    duration_performance = df.groupby('Duration Bin').agg({
        'Views': 'mean',
        'Engagement Rate': 'mean',
        'Video ID': 'count'
    }).reset_index()
    
    return duration_performance
# Main app
# def main():
#     # Import required libraries at the top
#     import pandas as pd
#     import streamlit as st
    
#     # Initialize session state for API key
#     if 'api_key' not in st.session_state:
#         st.session_state.api_key = ""
    
#     # Add YouTube logo and header
#     col1, col2 = st.columns([1, 5])
#     with col1:
#         st.markdown(get_youtube_logo(), unsafe_allow_html=True)
#     with col2:
#         st.markdown("<h1 class='main-header'>YouTube Analytics Hub</h1>", unsafe_allow_html=True)
    
#     # Add animated loading indicator
#     lottie_url = "https://assets2.lottiefiles.com/packages/lf20_rbtawnwz.json"
#     lottie_animation = load_lottieurl(lottie_url)
    
#     # Sidebar
#     with st.sidebar:
#         st.markdown("<h2 class='sidebar-header'>📈 Analytics Dashboard</h2>", unsafe_allow_html=True)
        
#         # Input options
#         option = st.radio("Choose Input Method", 
#                          ["Enter Channel Details", "Use Sample Data", "Load Demo Data"])
        
#         if option == "Enter Channel Details":
#             st.markdown("<h3 style='margin-top:20px;'>Channel Information</h3>", unsafe_allow_html=True)
            
#             # API key input with save functionality
#             saved_key = st.session_state.api_key
#             api_key = st.text_input("YouTube API Key", value=saved_key, type="password", 
#                               help="Get your API key from Google Cloud Console")
            
#             if api_key != saved_key:
#                 st.session_state.api_key = api_key
            
#             # Channel ID with examples
#             channel_id = st.text_input("Channel ID", value="",
#                                 help="E.g., UC_x5XG1OV2P6uZZ5FSM9Ttw (Google Developers)")
            
#             # Example channel IDs
#             st.markdown("<p style='font-size:0.8rem; color:#666;'>Try these channels:</p>", unsafe_allow_html=True)
#             st.markdown("""
#             <div style='font-size:0.8rem; color:#666;'>
#             • UC_x5XG1OV2P6uZZ5FSM9Ttw (Google Developers)<br>
#             • UCsBjURrPoezykLs9EqgamOA (Fireship)<br>
#             • UCsBjURrPoezykLs9EqgamOA (MKBHD)
#             </div>
#             """, unsafe_allow_html=True)
            
#             fetch_button = st.button("🔍 Fetch Channel Data", key="fetch", use_container_width=True)
            
#             # Add information about API keys
#             with st.expander("ℹ How to get a YouTube API Key"):
#                 st.markdown("""
#                 1. Go to [Google Cloud Console](https://console.cloud.google.com/)
#                 2. Create a new project
#                 3. Enable the YouTube Data API v3
#                 4. Create credentials (API Key)
#                 5. Copy your API key and use it here
                
#                 Note: YouTube API has daily quota limits. Each request uses some quota points.
#                 """)
        
#         elif option == "Load Demo Data":
#             # Demo data selection
#             st.markdown("<h3 style='margin-top:20px;'>Select Demo Channel</h3>", unsafe_allow_html=True)
#             demo_option = st.selectbox("Choose a demo channel", 
#                                       ["Tech Channel", "Gaming Channel", "Educational Channel", "Music Channel"])
            
#             load_demo = st.button("📂 Load Demo Data", key="load_demo", use_container_width=True)
            
#         else:  # Use Sample Data
#             st.markdown("<h3 style='margin-top:20px;'>Sample Data</h3>", unsafe_allow_html=True)
#             load_sample = st.button("📂 Load Sample Data", key="load_sample", use_container_width=True)
    
#     # Main content area
#     channel_stats = None
#     video_data = None
#     comment_data = None
    
#     # Handle data loading based on option
#     if option == "Enter Channel Details" and fetch_button:
#         if api_key and channel_id:
#             with st.spinner("Fetching data from YouTube API..."):
#                 if lottie_animation:
#                     st_lottie(lottie_animation, height=200, key="loading")
#                 channel_stats, video_data, comment_data = fetch_youtube_data(api_key, channel_id)
#                 if channel_stats and video_data:
#                     save_data_to_files(channel_stats, video_data, comment_data)
#                     st.success("Data fetched successfully!")
#                 else:
#                     st.warning("⚠ Could not fetch data. Please check your API key and channel ID.")
#         else:
#             st.warning("⚠ Please enter both API Key and Channel ID")
    
#     elif option == "Use Sample Data" and load_sample:
#         with st.spinner("Loading sample data..."):
#             channel_stats, video_data, comment_data = load_data_from_files()
#             if not (channel_stats and video_data):
#                 st.warning("No sample data found. Please fetch data using API first.")
    
#     # elif option == "Load Demo Data" and load_demo:
#     #     # This would load pre-saved demo data in a real app
#     #     demo_data_loaded = True
#     #     with st.spinner(f"Loading demo data for {demo_option}..."):
#     #         channel_stats, video_data, comment_data = load_demo_data(demo_option)
#     #         if not (channel_stats and video_data):
#     #             st.warning("No demo data found. Please check back later.")
#     #         else:
#     #             st.success(f"Demo data for {demo_option} loaded successfully!")
    
#     # Process data if available
#     if channel_stats and video_data:
#         # Get enhanced dataframes
#         enhanced_df = enhance_video_data(video_data)
#         enhanced_channel = enhance_channel_data(channel_stats, enhanced_df)
        
#         # Apply category names
#         enhanced_df['Category Name'] = enhanced_df['Category ID'].apply(get_category_name)
        
#         # Process comment data if available
#         comment_df = pd.DataFrame()
#         if comment_data:
#             comment_df = analyze_comments(comment_data)
        
#         # Generate insights and recommendations
#         recommendations = generate_recommendations(enhanced_df, enhanced_channel)
#         insights = get_trending_insights(enhanced_df)
#         duration_data = parse_duration_data(enhanced_df)
        
#         # Create dashboard layout with tabs
#         tab1, tab2, tab3, tab4, tab5 = st.tabs([
#             "📊 Channel Overview", 
#             "🎬 Content Analysis", 
#             "👥 Audience Insights", 
#             "📈 Growth Strategy",
#             "🔍 Deep Dive"
#         ])
        
#         with tab1:
#             # Channel Overview Tab
#             col1, col2 = st.columns([2, 1])
            
#             with col1:
#                 # Channel header with thumbnail
#                 st.markdown(f"""
#                 <div style="display:flex; align-items:center; margin-bottom:20px;">
#                     <img src="{enhanced_channel.get('Thumbnail URL', '')}" style="width:80px; height:80px; border-radius:50%; margin-right:15px;">
#                     <div>
#                         <h2 style="margin:0;">{enhanced_channel['Channel Name']}</h2>
#                         <p style="margin:0; color:#606060;">{enhanced_channel.get('Subscribers', 0):,} subscribers • {enhanced_channel.get('Total Videos', 0)} videos</p>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
                
#                 # Channel description
#                 if enhanced_channel.get('Description'):
#                     with st.expander("📝 Channel Description"):
#                         st.markdown(enhanced_channel['Description'])
            
#             with col2:
#                 # Channel age and country
#                 created_date = pd.to_datetime(enhanced_channel['Channel Created'])
#                 st.markdown(f"""
#                 <div style="background:#f8f9fa; padding:15px; border-radius:10px; margin-bottom:20px;">
#                     <p style="margin:0;"><b>Created:</b> {created_date.strftime('%b %d, %Y')}</p>
#                     <p style="margin:0;"><b>Channel Age:</b> {enhanced_channel['Age Days'] // 365} years, {enhanced_channel['Age Days'] % 365} days</p>
#                     <p style="margin:0;"><b>Country:</b> {enhanced_channel.get('Country', 'Not specified')}</p>
#                 </div>
#                 """, unsafe_allow_html=True)
            
#             # Key metrics
#             st.markdown("<h3 class='sub-header'>Channel Performance</h3>", unsafe_allow_html=True)
            
#             col1, col2, col3, col4 = st.columns(4)
#             with col1:
#                 st.markdown(f"""
#                 <div class="metric-card">
#                     <p class="metric-value">{enhanced_channel['Subscribers']:,}</p>
#                     <p class="metric-label">Subscribers</p>
#                 </div>
#                 """, unsafe_allow_html=True)
                
#             with col2:
#                 st.markdown(f"""
#                 <div class="metric-card">
#                     <p class="metric-value">{enhanced_channel['Views']:,}</p>
#                     <p class="metric-label">Total Views</p>
#                 </div>
#                 """, unsafe_allow_html=True)
                
#             with col3:
#                 st.markdown(f"""
#                 <div class="metric-card">
#                     <p class="metric-value">{enhanced_channel['Total Videos']:,}</p>
#                     <p class="metric-label">Videos</p>
#                 </div>
#                 """, unsafe_allow_html=True)
                
#             with col4:
#                 avg_views = enhanced_df['Views'].mean()
#                 st.markdown(f"""
#                 <div class="metric-card">
#                     <p class="metric-value">{int(avg_views):,}</p>
#                     <p class="metric-label">Avg Views/Video</p>
#                 </div>
#                 """, unsafe_allow_html=True)
            
#             # Secondary metrics
#             st.markdown("<h3 class='sub-header'>Engagement Metrics</h3>", unsafe_allow_html=True)
            
#             # Add engagement metrics visualization here
#             # This section is incomplete in the original code


# Additional helper function needed for Tab 5
def get_correlation_explanation(metric1, metric2, corr_value):
    """Generate explanation text for correlation values between metrics"""
    
    explanations = {
        ('Views', 'Likes'): "Videos with more views tend to get more likes, showing a standard engagement pattern.",
        ('Likes', 'Views'): "Videos with more likes tend to get more views, showing a standard engagement pattern.",
        
        ('Views', 'Comments'): "Videos with more views generally attract more comments, showing higher audience investment.",
        ('Comments', 'Views'): "Videos with more comments generally attract more views, showing higher audience investment.",
        
        ('Likes', 'Comments'): "Videos that generate likes also tend to generate comments, showing consistent engagement.",
        ('Comments', 'Likes'): "Videos that generate comments also tend to generate likes, showing consistent engagement.",
        
        ('Views', 'Engagement Rate'): "Higher view counts don't necessarily correlate with higher engagement rates.",
        ('Engagement Rate', 'Views'): "Videos with higher engagement rates don't necessarily have more total views.",
        
        ('Duration (sec)', 'Views'): "Video length shows a relationship with view count, suggesting audience preferences for certain durations.",
        ('Views', 'Duration (sec)'): "View count shows a relationship with video length, suggesting audience preferences for certain durations.",
        
        ('Duration (sec)', 'Engagement Rate'): "Video length impacts how engaged viewers are with the content.",
        ('Engagement Rate', 'Duration (sec)'): "Engagement levels vary with video length, suggesting optimal duration ranges.",
        
        ('Tag Count', 'Views'): "The number of tags used shows a relationship with view performance.",
        ('Views', 'Tag Count'): "Videos with different view counts tend to have different numbers of tags.",
        
        ('Title Length', 'Views'): "The length of video titles has a relationship with view performance.",
        ('Views', 'Title Length'): "Videos with different view counts tend to have different title lengths.",
    }
    
    # Default explanation if specific pair not found
    default_explanation = f"These metrics show a {abs(corr_value):.2f} {'positive' if corr_value > 0 else 'negative'} correlation."
    
    # Return specific explanation if available, otherwise default
    return explanations.get((metric1, metric2), explanations.get((metric2, metric1), default_explanation))

def main():
    # Import required libraries at the top
    import pandas as pd
    import streamlit as st
    load_dotenv()
    api_key = os.getenv('API_KEY')
    # Initialize session state for API key
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    
    # Add YouTube logo and header
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown(get_youtube_logo(), unsafe_allow_html=True)
    with col2:
        st.markdown("<h1 class='main-header'>YouTube Analytics Hub</h1>", unsafe_allow_html=True)
    
    # Add animated loading indicator
    lottie_url = "https://assets2.lottiefiles.com/packages/lf20_rbtawnwz.json"
    lottie_animation = load_lottieurl(lottie_url)
    
    # Sidebar
    with st.sidebar:
        st.markdown("<h2 class='sidebar-header'>📈 Analytics Dashboard</h2>", unsafe_allow_html=True)
        
        # Input options
        option = st.radio("Choose Input Method", 
                         ["Enter Channel Details", "Use Sample Data", "Load Demo Data"])
        
        if option == "Enter Channel Details":
            st.markdown("<h3 style='margin-top:20px;'>Channel Information</h3>", unsafe_allow_html=True)
            
            # API key input with save functionality
            saved_key = st.session_state.api_key
            api_key = st.text_input("YouTube API Key", value=saved_key, type="password", 
                              help="Get your API key from Google Cloud Console")
            
            if api_key != saved_key:
                st.session_state.api_key = api_key
            
            # Channel ID with examples
            channel_id = st.text_input("Channel ID", value="",
                                help="E.g., UC_x5XG1OV2P6uZZ5FSM9Ttw (Google Developers)")
            
            # Example channel IDs
            st.markdown("<p style='font-size:0.8rem; color:#666;'>Try these channels:</p>", unsafe_allow_html=True)
            st.markdown("""
            <div style='font-size:0.8rem; color:#666;'>
            • UC_x5XG1OV2P6uZZ5FSM9Ttw (Google Developers)<br>
            • UCsBjURrPoezykLs9EqgamOA (Fireship)<br>
            • UCsBjURrPoezykLs9EqgamOA (MKBHD)
            </div>
            """, unsafe_allow_html=True)
            
            fetch_button = st.button("🔍 Fetch Channel Data", key="fetch", use_container_width=True)
            
            # Add information about API keys
            with st.expander("ℹ How to get a YouTube API Key"):
                st.markdown("""
                1. Go to [Google Cloud Console](https://console.cloud.google.com/)
                2. Create a new project
                3. Enable the YouTube Data API v3
                4. Create credentials (API Key)
                5. Copy your API key and use it here
                
                Note: YouTube API has daily quota limits. Each request uses some quota points.
                """)
        
        elif option == "Load Demo Data":
            # Demo data selection
            st.markdown("<h3 style='margin-top:20px;'>Select Demo Channel</h3>", unsafe_allow_html=True)
            demo_option = st.selectbox("Choose a demo channel", 
                                      ["Tech Channel", "Gaming Channel", "Educational Channel", "Music Channel"])
            
            load_demo = st.button("📂 Load Demo Data", key="load_demo", use_container_width=True)
            
        else:  # Use Sample Data
            st.markdown("<h3 style='margin-top:20px;'>Sample Data</h3>", unsafe_allow_html=True)
            load_sample = st.button("📂 Load Sample Data", key="load_sample", use_container_width=True)
    
    # Main content area
    channel_stats = None
    video_data = None
    comment_data = None
    
    # Handle data loading based on option
    if option == "Enter Channel Details" and fetch_button:
        if api_key and channel_id:
            with st.spinner("Fetching data from YouTube API..."):
                if lottie_animation:
                    st_lottie(lottie_animation, height=200, key="loading")
                channel_stats, video_data, comment_data = fetch_youtube_data(api_key, channel_id)
                if channel_stats and video_data:
                    save_data_to_files(channel_stats, video_data, comment_data)
                    st.success("Data fetched successfully!")
                else:
                    st.warning("⚠ Could not fetch data. Please check your API key and channel ID.")
        else:
            st.warning("⚠ Please enter both API Key and Channel ID")
    
    elif option == "Use Sample Data" and load_sample:
        with st.spinner("Loading sample data..."):
            channel_stats, video_data, comment_data = load_data_from_files()
            if not (channel_stats and video_data):
                st.warning("No sample data found. Please fetch data using API first.")
    
    elif option == "Load Demo Data" and load_demo:
        # This would load pre-saved demo data in a real app
        st.info("Demo data feature coming soon! Please use API method for now.")
        # In a real implementation, you would load demo data from files:
        # channel_stats, video_data, comment_data = load_demo_data(demo_option)
    
    # Process data if available
    if channel_stats and video_data:
        # Get enhanced dataframes
        enhanced_df = enhance_video_data(video_data)
        enhanced_channel = enhance_channel_data(channel_stats, enhanced_df)
        
        # Apply category names
        enhanced_df['Category Name'] = enhanced_df['Category ID'].apply(get_category_name)
        
        # Process comment data if available
        comment_df = pd.DataFrame()
        if comment_data:
            comment_df = analyze_comments(comment_data)
        
        # Generate insights and recommendations
        recommendations = generate_recommendations(enhanced_df, enhanced_channel)
        insights = get_trending_insights(enhanced_df)
        duration_data = parse_duration_data(enhanced_df)
        
        # Create dashboard layout with tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Channel Overview", 
            "🎬 Content Analysis", 
            "👥 Audience Insights", 
            "📈 Growth Strategy",
            "🔍 Deep Dive"
        ])
        
        with tab1:
            # Channel Overview Tab
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Channel header with thumbnail
                st.markdown(f"""
                <div style="display:flex; align-items:center; margin-bottom:20px;">
                    <img src="{enhanced_channel.get('Thumbnail URL', '')}" style="width:80px; height:80px; border-radius:50%; margin-right:15px;">
                    <div>
                        <h2 style="margin:0;">{enhanced_channel['Channel Name']}</h2>
                        <p style="margin:0; color:#606060;">{enhanced_channel.get('Subscribers', 0):,} subscribers • {enhanced_channel.get('Total Videos', 0)} videos</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Channel description
                if enhanced_channel.get('Description'):
                    with st.expander("📝 Channel Description"):
                        st.markdown(enhanced_channel['Description'])
            
            with col2:
                # Channel age and country
                created_date = pd.to_datetime(enhanced_channel['Channel Created'])
                st.markdown(f"""
                <div style="background:#f8f9fa; padding:15px; border-radius:10px; margin-bottom:20px;">
                    <p style="margin:0;"><b>Created:</b> {created_date.strftime('%b %d, %Y')}</p>
                    <p style="margin:0;"><b>Channel Age:</b> {enhanced_channel['Age Days'] // 365} years, {enhanced_channel['Age Days'] % 365} days</p>
                    <p style="margin:0;"><b>Country:</b> {enhanced_channel.get('Country', 'Not specified')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Key metrics
            st.markdown("<h3 class='sub-header'>Channel Performance</h3>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value">{enhanced_channel['Subscribers']:,}</p>
                    <p class="metric-label">Subscribers</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value">{enhanced_channel['Views']:,}</p>
                    <p class="metric-label">Total Views</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value">{enhanced_channel['Total Videos']:,}</p>
                    <p class="metric-label">Videos</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col4:
                avg_views = enhanced_df['Views'].mean()
                st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value">{int(avg_views):,}</p>
                    <p class="metric-label">Avg Views/Video</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Secondary metrics
            st.markdown("<h3 class='sub-header'>Engagement Metrics</h3>", unsafe_allow_html=True)
            
            # Add engagement metrics row
            eng_col1, eng_col2, eng_col3 = st.columns(3)
            
            with eng_col1:
                avg_engagement = enhanced_df['Engagement Rate'].mean()
                st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value">{avg_engagement:.2f}%</p>
                    <p class="metric-label">Avg Engagement Rate</p>
                </div>
                """, unsafe_allow_html=True)
                
            with eng_col2:
                avg_likes = enhanced_df['Likes'].mean()
                st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value">{int(avg_likes):,}</p>
                    <p class="metric-label">Avg Likes per Video</p>
                </div>
                """, unsafe_allow_html=True)
                
            with eng_col3:
                avg_comments = enhanced_df['Comments'].mean()
                st.markdown(f"""
                <div class="metric-card">
                    <p class="metric-value">{int(avg_comments):,}</p>
                    <p class="metric-label">Avg Comments per Video</p>
                </div>
                """, unsafe_allow_html=True)
                
            # Channel growth over time
            st.markdown("<h3 class='sub-header'>Channel Growth</h3>", unsafe_allow_html=True)
            
            # Growth chart - videos by month
            monthly_videos = enhanced_df.groupby('Year-Month')['Video ID'].count().reset_index()
            monthly_videos.columns = ['Month', 'Videos']
            
            # Convert to datetime for proper ordering
            monthly_videos['Month'] = pd.to_datetime(monthly_videos['Month'])
            monthly_videos = monthly_videos.sort_values('Month')
            monthly_videos['Month'] = monthly_videos['Month'].dt.strftime('%Y-%m')
            
            # Create plotly bar chart
            fig = px.bar(
                monthly_videos,
                x='Month',
                y='Videos',
                title='Videos Published by Month',
                labels={'Month': 'Month', 'Videos': 'Number of Videos'},
                color_discrete_sequence=['#FF0000']
            )
            
            fig.update_layout(
                xaxis_tickangle=-45,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Top performing videos
            st.markdown("<h3 class='sub-header'>Top Performing Videos</h3>", unsafe_allow_html=True)
            
            # Create thumbnail grid
            create_thumbnail_grid(enhanced_df, num_thumbnails=6)
            
        
        with tab2:
            # Content Analysis Tab
            st.markdown("<h2 class='sub-header'>Content Performance Analysis</h2>", unsafe_allow_html=True)
            
            # Duration analysis
            st.markdown("<h3 class='sub-header'>Video Duration Analysis</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 2])
            
            with col1:
                # Duration vs. views chart
                fig = px.bar(
                    duration_data,
                    x='Duration Bin',
                    y='Views',
                    title='Average Views by Video Duration',
                    labels={'Duration Bin': 'Duration', 'Views': 'Average Views'},
                    color_discrete_sequence=['#FF0000'],
                    text='Views'
                )
                
                fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
                
                fig.update_layout(
                    xaxis_tickangle=-45,
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            with col2:
                # Video count by duration
                fig = px.pie(
                    duration_data,
                    names='Duration Bin',
                    values='Video ID',
                    title='Video Count by Duration',
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.Reds
                )
                
                fig.update_traces(textposition='inside', textinfo='percent+label')
                
                fig.update_layout(
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Title & Tag Analysis
            st.markdown("<h3 class='sub-header'>Title & Tag Analysis</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Title word cloud
                st.markdown("<p style='text-align:center;'>Most Common Words in Video Titles</p>", unsafe_allow_html=True)
                
                wordcloud = create_wordcloud(enhanced_df, column='Title Words')
                if wordcloud:
                    # Convert wordcloud to image
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    st.pyplot(fig)
                else:
                    st.info("Not enough title data to create word cloud")
                    
            with col2:
                # Title feature performance
                title_features_df = pd.DataFrame({
                    'Feature': ['Has Question Mark', 'Has Number', 'Has Uppercase Word'],
                    'Avg Views': [
                        enhanced_df[enhanced_df['Has Question']]['Views'].mean(),
                        enhanced_df[enhanced_df['Has Number']]['Views'].mean(),
                        enhanced_df[enhanced_df['Has Uppercase Word']]['Views'].mean()
                    ],
                    'Regular Views': [
                        enhanced_df[~enhanced_df['Has Question']]['Views'].mean(),
                        enhanced_df[~enhanced_df['Has Number']]['Views'].mean(),
                        enhanced_df[~enhanced_df['Has Uppercase Word']]['Views'].mean()
                    ]
                })
                
                # Reshape for plotting
                title_features_long = pd.melt(
                    title_features_df, 
                    id_vars=['Feature'], 
                    value_vars=['Avg Views', 'Regular Views'],
                    var_name='Type', 
                    value_name='Views'
                )
                
                # Create bar chart
                fig = px.bar(
                    title_features_long,
                    x='Feature',
                    y='Views',
                    color='Type',
                    barmode='group',
                    title='Impact of Title Features on Views',
                    color_discrete_sequence=['#FF0000', '#666666']
                )
                
                fig.update_layout(
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Category Analysis
            st.markdown("<h3 class='sub-header'>Category Analysis</h3>", unsafe_allow_html=True)
            
            # Create category performance dataframe
            category_perf = enhanced_df.groupby('Category Name').agg({
                'Views': 'mean',
                'Engagement Rate': 'mean',
                'Video ID': 'count'
            }).reset_index()
            
            category_perf.columns = ['Category', 'Avg Views', 'Avg Engagement', 'Video Count']
            category_perf = category_perf.sort_values('Avg Views', ascending=False)
            
            # Display bar chart of category performance
            fig = px.bar(
                category_perf,
                x='Category',
                y='Avg Views',
                color='Video Count',
                title='Average Views by Category',
                labels={'Category': 'Video Category', 'Avg Views': 'Average Views', 'Video Count': 'Number of Videos'},
                color_continuous_scale='Reds',
                text='Video Count'
            )
            
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            
            fig.update_layout(
                xaxis_tickangle=-45,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Upload Pattern Analysis
            st.markdown("<h3 class='sub-header'>Upload Pattern Analysis</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Day of week analysis
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                day_performance = enhanced_df.groupby('Publish Day of Week').agg({
                    'Views': 'mean',
                    'Video ID': 'count'
                }).reset_index()
                
                # Reorder days
                day_performance['Publish Day of Week'] = pd.Categorical(
                    day_performance['Publish Day of Week'], 
                    categories=day_order, 
                    ordered=True
                )
                day_performance = day_performance.sort_values('Publish Day of Week')
                
                fig = px.line(
                    day_performance,
                    x='Publish Day of Week',
                    y='Views',
                    markers=True,
                    title='Average Views by Day of Week',
                    labels={'Publish Day of Week': 'Day', 'Views': 'Average Views'},
                    color_discrete_sequence=['#FF0000']
                )
                
                fig.update_layout(
                    xaxis_tickangle=0,
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            with col2:
                # Time of day analysis
                hour_performance = enhanced_df.groupby('Hour Published').agg({
                    'Views': 'mean',
                    'Video ID': 'count'
                }).reset_index()
                
                # Sort by hour
                hour_performance = hour_performance.sort_values('Hour Published')
                
                fig = px.line(
                    hour_performance,
                    x='Hour Published',
                    y='Views',
                    markers=True,
                    title='Average Views by Hour of Day',
                    labels={'Hour Published': 'Hour (24h)', 'Views': 'Average Views'},
                    color_discrete_sequence=['#FF0000']
                )
                
                fig.update_traces(mode='lines+markers')
                
                fig.update_layout(
                    xaxis=dict(tickmode='linear', dtick=2),
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Audience Insights Tab
            st.markdown("<h2 class='sub-header'>Audience Engagement Analysis</h2>", unsafe_allow_html=True)
            
            # Engagement metrics over time
            st.markdown("<h3 class='sub-header'>Engagement Trends</h3>", unsafe_allow_html=True)
            
            # Create time-series dataframe
            engagement_time = enhanced_df.groupby('Year-Month').agg({
                'Views': 'mean',
                'Likes': 'mean',
                'Comments': 'mean',
                'Engagement Rate': 'mean'
            }).reset_index()
            
            # Convert to datetime for proper ordering
            engagement_time['Year-Month'] = pd.to_datetime(engagement_time['Year-Month'])
            engagement_time = engagement_time.sort_values('Year-Month')
            engagement_time['Year-Month'] = engagement_time['Year-Month'].dt.strftime('%Y-%m')
            
            # Create engagement rate chart
            fig = px.line(
                engagement_time, 
                x='Year-Month', 
                y='Engagement Rate',
                title='Engagement Rate Trend Over Time',
                labels={'Year-Month': 'Month', 'Engagement Rate': 'Engagement Rate (%)'},
                markers=True,
                color_discrete_sequence=['#FF0000']
            )
            
            fig.update_layout(
                xaxis_tickangle=-45,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Likes vs. Comments Analysis
            col1, col2 = st.columns(2)
            
            with col1:
                # Likes trend
                fig = px.line(
                    engagement_time, 
                    x='Year-Month', 
                    y='Likes',
                    title='Average Likes per Video Over Time',
                    labels={'Year-Month': 'Month', 'Likes': 'Average Likes'},
                    markers=True,
                    color_discrete_sequence=['#FF0000']
                )
                
                fig.update_layout(
                    xaxis_tickangle=-45,
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            with col2:
                # Comments trend
                fig = px.line(
                    engagement_time, 
                    x='Year-Month', 
                    y='Comments',
                    title='Average Comments per Video Over Time',
                    labels={'Year-Month': 'Month', 'Comments': 'Average Comments'},
                    markers=True,
                    color_discrete_sequence=['#FF0000']
                )
                
                fig.update_layout(
                    xaxis_tickangle=-45,
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Comment Sentiment Analysis
            if not comment_df.empty:
                st.markdown("<h3 class='sub-header'>Comment Sentiment Analysis</h3>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Sentiment distribution
                    sentiment_counts = comment_df['Sentiment Category'].value_counts().reset_index()
                    sentiment_counts.columns = ['Sentiment', 'Count']
                    
                    # Create pie chart
                    colors = {'Positive': '#4CAF50', 'Neutral': '#2196F3', 'Negative': '#FF5252'}
                    fig = px.pie(
                        sentiment_counts,
                        names='Sentiment',
                        values='Count',
                        title='Comment Sentiment Distribution',
                        color='Sentiment',
                        color_discrete_map=colors,
                        hole=0.4
                    )
                    
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    
                    fig.update_layout(
                        margin=dict(l=20, r=20, t=40, b=20),
                        paper_bgcolor='rgba(0,0,0,0)',
                        legend_title_text=''
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                with col2:
                    # Top positive and negative comments
                    st.markdown("<h4>Top Positive Comments</h4>", unsafe_allow_html=True)
                    
                    positive_comments = comment_df.sort_values('Sentiment', ascending=False).head(3)
                    for i, row in positive_comments.iterrows():
                        st.markdown(f"""
                        <div style="border-left: 4px solid #4CAF50; padding-left: 10px; margin-bottom: 10px;">
                            <p style="font-style: italic;">"{row['Comment'][:150]}..."</p>
                            <p style="text-align: right; margin: 0; font-size: 0.8rem; color: #666;">
                                - {row['Author']} on "{row['Video Title'][:30]}..."
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("<h4>Top Negative Comments</h4>", unsafe_allow_html=True)
                    
                    negative_comments = comment_df.sort_values('Sentiment').head(3)
                    for i, row in negative_comments.iterrows():
                        st.markdown(f"""
                        <div style="border-left: 4px solid #FF5252; padding-left: 10px; margin-bottom: 10px;">
                            <p style="font-style: italic;">"{row['Comment'][:150]}..."</p>
                            <p style="text-align: right; margin: 0; font-size: 0.8rem; color: #666;">
                                - {row['Author']} on "{row['Video Title'][:30]}..."
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Comment word cloud
                st.markdown("<h4>Most Common Words in Comments</h4>", unsafe_allow_html=True)
                
                comment_text = ' '.join(comment_df['Comment'].tolist())
                if comment_text:
                    # Create word cloud from comment text
                    comment_wc = WordCloud(width=800, height=400, background_color='white', 
                                   max_words=100, colormap='viridis', 
                                   contour_width=1, contour_color='steelblue')
                    comment_wc.generate(comment_text)
                    
                    # Display word cloud
                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(comment_wc, interpolation='bilinear')
                    ax.axis('off')
                    st.pyplot(fig)
            else:
                st.info("No comment data available for sentiment analysis")
            
            # Audience retention proxy (using engagement vs. video length)
            st.markdown("<h3 class='sub-header'>Audience Retention Proxy</h3>", unsafe_allow_html=True)
            
            # Create scatter plot of duration vs. engagement
            fig = px.scatter(
                enhanced_df,
                x='Duration (sec)',
                y='Engagement Rate',
                color='Views',
                size='Views',
                hover_name='Title',
                title='Engagement Rate vs. Video Duration',
                labels={
                    'Duration (sec)': 'Video Duration (seconds)',
                    'Engagement Rate': 'Engagement Rate (%)',
                    'Views': 'Total Views'
                },
                color_continuous_scale='Reds'
            )
            
            fig.update_layout(
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            # Add trendline
            fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
            
            st.plotly_chart(fig, use_container_width=True)
        
 
# Growth Strategy Tab
        with tab4:
            # Growth Strategy Tab
            st.markdown("<h2 class='sub-header'>Growth Strategy & Recommendations</h2>", unsafe_allow_html=True)
            
            # Display insights
            st.markdown("<h3 class='sub-header'>Channel Insights</h3>", unsafe_allow_html=True)
            
            # Create columns for insights display
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
                st.markdown("<h4>Content Strategy Insights</h4>", unsafe_allow_html=True)
                
                # Display insights from analysis
                for insight in insights[:3]:
                    st.markdown(f"""
                    <div class="insight-item">
                        <div class="insight-icon">💡</div>
                        <div class="insight-text">{insight}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
                st.markdown("<h4>Audience Engagement Insights</h4>", unsafe_allow_html=True)
                
                # Display additional insights
                for insight in insights[3:6]:
                    st.markdown(f"""
                    <div class="insight-item">
                        <div class="insight-icon">✨</div>
                        <div class="insight-text">{insight}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Recommendations section
            st.markdown("<h3 class='sub-header'>Personalized Recommendations</h3>", unsafe_allow_html=True)

            # Create actionable recommendations cards
            rec_categories = {
                "Content Strategy": recommendations[:2],
                "Upload Schedule": recommendations[2:4],
                "Audience Engagement": recommendations[4:6],
                "Technical Optimization": recommendations[6:8]
            }

            # Display recommendations in expandable sections
            for category, recs in rec_categories.items():
                with st.expander(f"📌 {category}", expanded=True):
                    for i, rec in enumerate(recs):
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <h4>Recommendation {i+1}</h4>
                            <p>{rec['recommendation']}</p>
                            <div class="rec-reason">
                                <strong>Why:</strong> {rec.get('reason', 'No specific reason available')}
                            </div>
                            <div class="rec-action">
                                <strong>Action:</strong> {rec.get('action', 'No specific action available')}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
            # Growth opportunity analysis
            st.markdown("<h3 class='sub-header'>Growth Opportunity Analysis</h3>", unsafe_allow_html=True)
            
            # Create opportunity score metrics
            # Calculate opportunity scores based on channel data
            opportunity_data = {
                "Content Diversification": int(len(enhanced_df['Category ID'].unique()) / 10 * 100),
                "Upload Consistency": int(enhanced_channel.get('Consistency Score', 75)),
                "Keyword Optimization": int(enhanced_df['Tag Count'].mean() / 10 * 100),
                "Audience Engagement": int(enhanced_df['Engagement Rate'].replace([float('inf'), float('-inf')], np.nan).mean() * 10) if not np.isinf(enhanced_df['Engagement Rate'].replace([float('inf'), float('-inf')], np.nan).mean()) else 0    
        }
            
            # Create columns for opportunity scores
            cols = st.columns(len(opportunity_data))
            
            # Display opportunity scores
            for i, (metric, score) in enumerate(opportunity_data.items()):
                with cols[i]:
                    # Determine color based on score
                    if score >= 80:
                        color = "#4CAF50"  # Green
                    elif score >= 60:
                        color = "#FFC107"  # Yellow
                    else:
                        color = "#FF5252"  # Red
                        
                    st.markdown(f"""
                    <div class="score-card" style="text-align: center;">
                        <div class="score-circle" style="
                            width: 100px;
                            height: 100px;
                            border-radius: 50%;
                            background: conic-gradient({color} {score}%, #e0e0e0 0);
                            margin: 0 auto;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            position: relative;
                        ">
                            <div style="
                                width: 80px;
                                height: 80px;
                                border-radius: 50%;
                                background: #ffffff;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                position: absolute;
                                font-size: 24px;
                                font-weight: bold;
                                color: {color};
                            ">{score}%</div>
                        </div>
                        <p style="margin-top: 10px; font-weight: bold;">{metric}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Competitor analysis
            st.markdown("<h3 class='sub-header'>Competitor Benchmarking</h3>", unsafe_allow_html=True)
            
            # Create competitor data for benchmarking visualization
            comp_data = pd.DataFrame({
                'Metric': ['Subscribers', 'Avg Views', 'Engagement', 'Upload Frequency'],
                'Your Channel': [
                    enhanced_channel['Subscribers'] / 1000,
                    enhanced_df['Views'].mean() / 1000,
                    enhanced_df['Engagement Rate'].mean(),
                    len(enhanced_df) / (enhanced_channel['Age Days'] / 30)  # Videos per month
                ],
                'Competitor 1': [
                    enhanced_channel['Subscribers'] * 1.2 / 1000,
                    enhanced_df['Views'].mean() * 0.8 / 1000,
                    enhanced_df['Engagement Rate'].mean() * 1.1,
                    len(enhanced_df) / (enhanced_channel['Age Days'] / 30) * 1.3
                ],
                'Competitor 2': [
                    enhanced_channel['Subscribers'] * 0.7 / 1000,
                    enhanced_df['Views'].mean() * 1.2 / 1000,
                    enhanced_df['Engagement Rate'].mean() * 0.9,
                    len(enhanced_df) / (enhanced_channel['Age Days'] / 30) * 0.9
                ],
                'Industry Average': [
                    enhanced_channel['Subscribers'] * 0.9 / 1000,
                    enhanced_df['Views'].mean() * 0.9 / 1000,
                    enhanced_df['Engagement Rate'].mean() * 1.0,
                    len(enhanced_df) / (enhanced_channel['Age Days'] / 30) * 1.1
                ]
            })
            
            # Melt data for plotting
            comp_data_melted = pd.melt(
                comp_data, 
                id_vars=['Metric'], 
                var_name='Channel',
                value_name='Value'
            )
            
            # Create radar chart for competitor comparison
            fig = px.line_polar(
                comp_data_melted, 
                r='Value', 
                theta='Metric',
                color='Channel',
                line_close=True,
                color_discrete_sequence=['#FF0000', '#4CAF50', '#2196F3', '#9C27B0'],
                title='Competitive Landscape Analysis'
            )
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        showticklabels=False
                    )
                ),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5),
                margin=dict(l=20, r=20, t=60, b=20),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Growth projection
            st.markdown("<h3 class='sub-header'>Growth Projection</h3>", unsafe_allow_html=True)
            
            # Create simple projection model
            # Get current metrics
            current_subs = enhanced_channel['Subscribers']
            current_views = enhanced_channel['Views']
            channel_age_months = enhanced_channel['Age Days'] / 30
            
            # Calculate monthly growth rates
            sub_monthly_growth = current_subs / channel_age_months
            view_monthly_growth = current_views / channel_age_months
            
            # Create projection for next 12 months
            projection_months = 12
            months = list(range(1, projection_months + 1))
            projected_subs = [current_subs + (sub_monthly_growth * i) for i in months]
            projected_views = [current_views + (view_monthly_growth * i) for i in months]
            
            # Create projection dataframe
            projection_df = pd.DataFrame({
                'Month': [f"Month {i}" for i in months],
                'Projected Subscribers': projected_subs,
                'Projected Views': projected_views
            })
            
            # Display projection chart
            fig = px.line(
                projection_df,
                x='Month',
                y=['Projected Subscribers', 'Projected Views'],
                title='12-Month Growth Projection',
                labels={'value': 'Count', 'variable': 'Metric'},
                color_discrete_sequence=['#FF0000', '#4CAF50']
            )
            
            fig.update_layout(
                xaxis_tickangle=-45,
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend_title_text=''
            )
            
            # Add second y-axis for views
            fig.update_layout(
                yaxis=dict(title='Subscribers'),
                yaxis2=dict(
                    title='Views',
                    overlaying='y',
                    side='right',
                    showgrid=False
                )
            )
            
            # Update traces for second y-axis
            fig.data[1].update(yaxis='y2')
            
            st.plotly_chart(fig, use_container_width=True)

        with tab5:
            # Deep Dive Tab
            st.markdown("<h2 class='sub-header'>Deep Dive Analysis</h2>", unsafe_allow_html=True)
            
            # Video comparison tool
            st.markdown("<h3 class='sub-header'>Video Comparison Tool</h3>", unsafe_allow_html=True)
            
            # Create multi-select for videos
            top_videos = enhanced_df.sort_values('Views', ascending=False).head(15)
            selected_videos = st.multiselect(
                "Select videos to compare:",
                options=top_videos['Title'].tolist(),
                default=top_videos['Title'].tolist()[:3]
            )
            
            if selected_videos:
                # Filter data for selected videos
                selected_df = enhanced_df[enhanced_df['Title'].isin(selected_videos)]
                
                # Create metrics comparison
                metrics = ['Views', 'Likes', 'Comments', 'Engagement Rate', 'Duration (sec)']
                
                # Create comparison dataframe
                comparison_df = selected_df[['Title'] + metrics].set_index('Title')
                
                # Display as interactive table
                st.dataframe(
                    comparison_df.style.highlight_max(axis=0, color='#FFD700'),
                    use_container_width=True
                )
                
                # Create radar chart for video comparison
                # Normalize values for better visualization
                radar_df = comparison_df.copy()
                for col in radar_df.columns:
                    min_val = radar_df[col].min()
                    max_val = radar_df[col].max()
                    if max_val > min_val:  # Avoid division by zero
                        radar_df[col] = (radar_df[col] - min_val) / (max_val - min_val)
                    else:
                        radar_df[col] = 0  # Set to zero if all values are the same
                
                # Melt for radar chart
                radar_melted = pd.melt(
                    radar_df.reset_index(), 
                    id_vars=['Title'], 
                    var_name='Metric',
                    value_name='Normalized Value'
                )
                
                # Create radar chart
                fig = px.line_polar(
                    radar_melted, 
                    r='Normalized Value', 
                    theta='Metric', 
                    color='Title',
                    line_close=True,
                    title='Video Performance Comparison'
                )
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            showticklabels=False
                        )
                    ),
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Please select videos to compare")
            
            # Correlation Analysis
            st.markdown("<h3 class='sub-header'>Metric Correlation Analysis</h3>", unsafe_allow_html=True)
            
            # Select metrics to correlate
            corr_cols = ['Views', 'Likes', 'Comments', 'Engagement Rate', 'Duration (sec)', 'Tag Count', 'Title Length']
            
            # Calculate correlation matrix
            corr_matrix = enhanced_df[corr_cols].corr()
            
            # Create heatmap
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                color_continuous_scale='RdBu_r',
                zmin=-1, zmax=1,
                title='Correlation Between Metrics'
            )
            
            fig.update_layout(
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Key correlations explained
            st.markdown("<div class='insight-card'>", unsafe_allow_html=True)
            st.markdown("<h4>Key Correlations Explained</h4>", unsafe_allow_html=True)
            
            # Find most positive and negative correlations
            corr_pairs = []
            for i in range(len(corr_cols)):
                for j in range(i+1, len(corr_cols)):
                    corr_pairs.append((corr_cols[i], corr_cols[j], corr_matrix.iloc[i, j]))
            
            # Sort by absolute correlation
            corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
            
            # Display top correlations
            for pair in corr_pairs[:5]:
                if pair[2] > 0:
                    direction = "positive"
                    emoji = "📈"
                else:
                    direction = "negative"
                    emoji = "📉"
                
                st.markdown(f"""
                <div class="insight-item">
                    <div class="insight-icon">{emoji}</div>
                    <div class="insight-text">
                        <strong>{pair[0]} & {pair[1]}</strong>: {direction.capitalize()} correlation ({pair[2]:.2f}).
                        {get_correlation_explanation(pair[0], pair[1], pair[2])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Advanced Content Analysis
            st.markdown("<h3 class='sub-header'>Advanced Content Analysis</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Ensure necessary columns exist
                if 'Title Length' not in enhanced_df.columns:
                    enhanced_df['Title Length'] = enhanced_df['Title'].str.len()
                if 'Title Length Bin' not in enhanced_df.columns:
                    bins = [0, 20, 40, 60, 80, 100, float('inf')]
                    labels = ['0-20', '21-40', '41-60', '61-80', '81-100', '100+']
                    enhanced_df['Title Length Bin'] = pd.cut(enhanced_df['Title Length'], bins=bins, labels=labels)

                # Title length vs. views
                title_length_data = enhanced_df.groupby('Title Length Bin').agg({
                    'Views': 'mean',
                    'Video ID': 'count'
                }).reset_index()
               

            
            with col2:
                # Tag count vs. views
                                # Ensure 'Tag Count' exists
                if 'Tag Count' not in enhanced_df.columns:
                    enhanced_df['Tag Count'] = enhanced_df['Tags'].apply(lambda x: len(x) if isinstance(x, list) else 0)

                # Create 'Tag Count Bin' if missing
                if 'Tag Count Bin' not in enhanced_df.columns:
                    bins = [0, 5, 10, 15, 20, float('inf')]
                    labels = ['0-5', '6-10', '11-15', '16-20', '20+']
                    enhanced_df['Tag Count Bin'] = pd.cut(enhanced_df['Tag Count'], bins=bins, labels=labels)

                tag_count_data = enhanced_df.groupby(['Tag Count Bin'],observed=False).agg({
                    'Views': 'mean',
                    'Video ID': 'count'
                }).reset_index()
                
                fig = px.bar(
                    tag_count_data,
                    x='Tag Count Bin',
                    y='Views',
                    title='Average Views by Tag Count',
                    labels={'Tag Count Bin': 'Number of Tags', 'Views': 'Average Views'},
                    color_discrete_sequence=['#FF0000'],
                    text='Video ID'
                )
                
                fig.update_traces(texttemplate='%{text} videos', textposition='outside')
                
                fig.update_layout(
                    xaxis_tickangle=-45,
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Custom Analysis Tool
            st.markdown("<h3 class='sub-header'>Custom Analysis Tool</h3>", unsafe_allow_html=True)
            
            # Create flexible analysis tool
            col1, col2 = st.columns([1, 3])
            
            with col1:
                # Select metrics for analysis
                x_axis = st.selectbox(
                    "Select X-Axis Metric:",
                    options=['Views', 'Likes', 'Comments', 'Duration (sec)', 'Engagement Rate', 
                            'Tag Count', 'Title Length', 'Hour Published', 'Age (days)'],
                    index=0
                )
                
                y_axis = st.selectbox(
                    "Select Y-Axis Metric:",
                    options=['Views', 'Likes', 'Comments', 'Duration (sec)', 'Engagement Rate', 
                            'Tag Count', 'Title Length', 'Hour Published', 'Age (days)'],
                    index=4
                )
                
                color_metric = st.selectbox(
                    "Color By:",
                    options=['Category Name', 'Publish Day of Week', 'Has Question', 'Has Number', 'None'],
                    index=0
                )
                
                plot_type = st.radio(
                    "Plot Type:",
                    options=['Scatter', 'Bar', 'Line', 'Box'],
                    horizontal=True
                )
            
            with col2:
                # Create dynamic plot based on selections
                if color_metric == 'None':
                    color_col = None
                else:
                    color_col = color_metric
                
                if plot_type == 'Scatter':
                    fig = px.scatter(
                        enhanced_df,
                        x=x_axis,
                        y=y_axis,
                        color=color_col,
                        hover_name='Title',
                        title=f'{y_axis} vs {x_axis}',
                        labels={x_axis: x_axis, y_axis: y_axis},
                        trendline='ols' if color_col is None else None
                    )
                elif plot_type == 'Bar':
                    # For bar charts, we need aggregation
                    if color_col:
                        temp_df = enhanced_df.groupby(color_col)[y_axis].mean().reset_index()
                        fig = px.bar(
                            temp_df,
                            x=color_col,
                            y=y_axis,
                            title=f'Average {y_axis} by {color_col}',
                            color=color_col
                        )
                    else:
                        # Use another grouping if color_col is None
                        temp_df = enhanced_df.groupby('Year-Month')[y_axis].mean().reset_index()
                        fig = px.bar(
                            temp_df,
                            x='Year-Month',
                            y=y_axis,
                            title=f'Average {y_axis} Over Time'
                        )
                elif plot_type == 'Line':
                    # For line charts, we need a sequential x-axis
                    if x_axis in ['Hour Published', 'Age (days)']:
                        # These are already sequential
                        fig = px.line(
                            enhanced_df.sort_values(x_axis),
                            x=x_axis,
                            y=y_axis,
                            color=color_col,
                            title=f'{y_axis} vs {x_axis}'
                        )
                    else:
                        # Group by time for other metrics
                        temp_df = enhanced_df.groupby('Year-Month').agg({
                            y_axis: 'mean',
                            x_axis: 'mean'
                        }).reset_index()
                        
                        fig = px.line(
                            temp_df.sort_values('Year-Month'),
                            x='Year-Month',
                            y=[y_axis, x_axis],
                            title=f'{y_axis} and {x_axis} Over Time'
                        )
                else:  # Box Plot
                    fig = px.box(
                        enhanced_df,
                        x=color_col if color_col else 'Category Name',
                        y=y_axis,
                        color=color_col,
                        title=f'Distribution of {y_axis} by {color_col if color_col else "Category"}'
                    )
                
                fig.update_layout(
                    margin=dict(l=20, r=20, t=40, b=20),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Action plan generator section
            st.markdown("<h3 class='sub-header'>Custom Action Plan Generator</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Goals selection
                st.markdown("<h4>Select Your Goals</h4>", unsafe_allow_html=True)
                
                goal_increase_views = st.checkbox("Increase Views", value=True)
                goal_increase_engagement = st.checkbox("Increase Engagement", value=True)
                goal_grow_subscribers = st.checkbox("Grow Subscribers", value=True)
                goal_optimize_content = st.checkbox("Optimize Content Strategy", value=False)
                
                # Timeline selection
                timeline = st.radio(
                    "Timeline:",
                    options=["Short-term (1-3 months)", "Medium-term (3-6 months)", "Long-term (6-12 months)"],
                    horizontal=True
                )
            
            with col2:
                # Resource allocation
                st.markdown("<h4>Available Resources</h4>", unsafe_allow_html=True)
                
                time_investment = st.select_slider(
                    "Time Investment:",
                    options=["Minimal", "Moderate", "Significant"],
                    value="Moderate"
                )
                
                budget = st.select_slider(
                    "Budget:",
                    options=["No budget", "Limited", "Moderate", "High"],
                    value="Limited"
                )
                
                existing_content = st.number_input(
                    "Existing Content (# of videos):",
                    min_value=0,
                    max_value=1000,
                    value=len(enhanced_df),
                    step=10
                )
            
            # Generate action plan button
            if st.button("Generate Custom Action Plan", use_container_width=True):
                with st.spinner("Creating your customized action plan..."):
                    time.sleep(1)  # Simulate processing time
                    
                    # Create custom action plan based on selections
                    st.markdown("<div class='action-plan'>", unsafe_allow_html=True)
                    st.markdown("<h3>Your Customized YouTube Growth Action Plan</h3>", unsafe_allow_html=True)
                    
                    # Introduction based on goals
                    goals = []
                    if goal_increase_views:
                        goals.append("increasing views")
                    if goal_increase_engagement:
                        goals.append("improving engagement")
                    if goal_grow_subscribers:
                        goals.append("growing subscribers")
                    if goal_optimize_content:
                        goals.append("optimizing content strategy")
                    
                    goals_text = ", ".join(goals[:-1]) + (" and " + goals[-1] if len(goals) > 1 else goals[0])
                    
                    st.markdown(f"""
                    <p>Based on your channel analytics and selected goals of {goals_text}, 
                    here's your customized {timeline.lower()} action plan with {time_investment.lower()} time investment
                    and {budget.lower()} budget requirements.</p>
                    """, unsafe_allow_html=True)
                    
                    # Generate sections based on goals
                    if goal_increase_views:
                        st.markdown("<h4>🎯 View Growth Strategy</h4>", unsafe_allow_html=True)
                        
                        # Get best performing category and duration from the data
                        best_performing_category = category_perf.iloc[0]['Category']
                        best_duration_bin = duration_data.sort_values('Views', ascending=False).iloc[0]['Duration Bin']
                        best_day = day_performance.sort_values('Views', ascending=False).iloc[0]['Publish Day of Week']
                        best_hour = hour_performance.sort_values('Views', ascending=False).iloc[0]['Hour Published']
                        
                        st.markdown(f"""
                        <ol>
                            <li><strong>Content Focus:</strong> Create more {best_performing_category} content, your highest-performing category</li>
                            <li><strong>Optimal Video Length:</strong> Aim for videos in the {best_duration_bin} range, which drives the most views</li>
                            <li><strong>Upload Schedule:</strong> Post on {best_day}s at around {best_hour}:00, your best-performing time slot</li>
                            <li><strong>Thumbnails & Titles:</strong> Use high-contrast thumbnails with surprised expressions and numbers in titles</li>
                        </ol>
                        """, unsafe_allow_html=True)
                    
                    if goal_increase_engagement:
                        st.markdown("<h4>💬 Engagement Improvement Plan</h4>", unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <ol>
                            <li><strong>Community Building:</strong> Ask questions in your videos and respond to comments within the first hour</li>
                            <li><strong>Interactive Elements:</strong> Use polls, community posts, and end screens to encourage interaction</li>
                            <li><strong>Call-to-Actions:</strong> Include specific CTAs in your videos at optimal times (beginning, middle, end)</li>
                            <li><strong>Audience Recognition:</strong> Feature viewer comments/content to boost community participation</li>
                        </ol>
                        """, unsafe_allow_html=True)
                    
                    if goal_grow_subscribers:
                        st.markdown("<h4>📈 Subscriber Growth Tactics</h4>", unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <ol>
                            <li><strong>Content Series:</strong> Create binge-worthy series that hook viewers across multiple videos</li>
                            <li><strong>Consistent Branding:</strong> Ensure your channel has a distinct, recognizable style</li>
                            <li><strong>Strategic Collaborations:</strong> Partner with channels that have {int(enhanced_channel['Subscribers']*0.5):,} to {int(enhanced_channel['Subscribers']*2):,} subscribers</li>
                            <li><strong>Value Proposition:</strong> Clearly communicate why viewers should subscribe in first 30 seconds</li>
                        </ol>
                        """, unsafe_allow_html=True)
                    
                    if goal_optimize_content:
                        st.markdown("<h4>🔍 Content Optimization Strategy</h4>", unsafe_allow_html=True)
                        
                        # Get optimal tag count from data
                        best_tag_bin = tag_count_data.sort_values('Views', ascending=False).iloc[0]['Tag Count Bin']
                        optimal_tag_count = int(best_tag_bin.split('-')[0])
                        
                        st.markdown(f"""
                        <ol>
                            <li><strong>Keyword Research:</strong> Target keywords with high search volume but moderate competition</li>
                            <li><strong>Metadata Optimization:</strong> Use {optimal_tag_count}+ tags per video and detailed descriptions with timestamps</li>
                            <li><strong>Content Refresh:</strong> Update older popular videos with new thumbnails and end screens</li>
                            <li><strong>Analytics Review:</strong> Schedule monthly analytics review to adjust strategy based on performance</li>
                        </ol>
                        """, unsafe_allow_html=True)
                    
                    # Implementation timeline based on selected timeline
                    st.markdown("<h4>📅 Implementation Timeline</h4>", unsafe_allow_html=True)
                    
                    if timeline == "Short-term (1-3 months)":
                        st.markdown("""
                        <p><strong>Month 1:</strong> Optimize existing content metadata and thumbnails</p>
                        <p><strong>Month 2:</strong> Implement new content strategy with optimized formats</p>
                        <p><strong>Month 3:</strong> Review performance and refine approach</p>
                        """, unsafe_allow_html=True)
                    elif timeline == "Medium-term (3-6 months)":
                        st.markdown("""
                        <p><strong>Months 1-2:</strong> Audit content and develop new strategy</p>
                        <p><strong>Months 3-4:</strong> Implement new content formats and engagement tactics</p>
                        <p><strong>Months 5-6:</strong> Develop collaboration strategy and review progress</p>
                        """, unsafe_allow_html=True)
                    else:  # Long-term
                        st.markdown("""
                        <p><strong>Months 1-3:</strong> Content audit and strategy development</p>
                        <p><strong>Months 4-6:</strong> Implement new formats and engagement tactics</p>
                        <p><strong>Months 7-9:</strong> Scale successful strategies and test new content verticals</p>
                        <p><strong>Months 10-12:</strong> Review annual performance and develop next year plan</p>
                        """, unsafe_allow_html=True)
                    
                    # Expected results based on current metrics
            
if __name__ == "__main__":
    main()