import requests
import csv

# ================== CONFIG SECTION ====================
API_KEY = 'YOUR_API_KEY'  # <<< Replace this with your actual YouTube Data API v3 key
SEARCH_QUERY = 'Carry minati'  # <<< Search keyword (can loop different keywords to get diverse channels)
MAX_CHANNELS = 10  # <<< How many channels you want
OUTPUT_CSV = 'youtube_channels.csv'
# ======================================================

def search_channels(api_key, query, max_results=50):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'channel',
        'maxResults': max_results,
        'key': api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['items']

def collect_channel_data(api_key, search_query, max_channels):
    channels = []
    fetched = 0
    while fetched < max_channels:
        batch_size = min(50, max_channels - fetched)
        results = search_channels(api_key, search_query, batch_size)
        for item in results:
            channel_title = item['snippet']['channelTitle']
            channel_id = item['snippet']['channelId']
            channels.append((channel_title, channel_id))
            fetched += 1
    return channels

def write_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Channel Name', 'Channel ID'])  # header
        writer.writerows(data)

def main():
    print("🔵 Collecting YouTube channels...")
    channels = collect_channel_data(API_KEY, SEARCH_QUERY, MAX_CHANNELS)
    write_to_csv(OUTPUT_CSV, channels)
    print(f"✅ CSV file '{OUTPUT_CSV}' generated successfully with {len(channels)} channels!")

if __name__ == "__main__":
    main()
