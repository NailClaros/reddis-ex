from dotenv import load_dotenv
import os
import redis
import json
load_dotenv()
"""Basic connection example.
"""

#cloud sintance
r = redis.Redis(
    host=f'{os.getenv("host")}',
    port=f'{os.getenv("port")}',
    decode_responses=True,
    username=f'{os.getenv("un")}',
    password=f'{os.getenv("pw")}'
    )

#local instance
# r = redis.Redis(host='localhost', port=6379, decode_responses=True)

print("Setting foo to bar")
r.set('foo', 'bar')
# True
print("foo:" + r.get('foo'))

print("\n\nTheoretical history logic--")
print("""data=\n
    {
    "songName": "Shape of You",
    "artistName": "Ed Sheeran",
    "songLang": "en",
    "songLyric": "The club isn't the best place to find a lover...",
    "albumCover": "https://link-to-cover-art.com/shape-of-you.jpg",
    "song_key": "song:abcd1234efgh5678"
  },
  {
    "songName": "Perfect",
    "artistName": "Ed Sheeran",
    "songLang": "en",
    "songLyric": "I found a love for me...",
    "albumCover": "https://link-to-cover-art.com/perfect.jpg",
    "song_key": "song:ijkl9012mnop3456"
  }  
      """)

v1 = {
    'code': 3,
    "songName": "Shape of You",
    "artistName": "Ed Sheeran",
    "songLang": "en",
    "songLyric": "The club isn't the best place to find a lover...",
    "albumCover": "https://link-to-cover-art.com/shape-of-you.jpg",
    "song_key": "song:abcd1234efgh5678"
  }

v2 = {
    "code": 3,
    "songName": "Perfect",
    "artistName": "Ed Sheeran",
    "songLang": "en",
    "songLyric": "I found a love for me...",
    "albumCover": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "song_key": "song:ijkl9012mnop3456"
  }

r.set('song:abcd1234efgh5678', json.dumps(v1))
r.set('song:ijkl9012mnop3456', json.dumps(v2))

print("creating a user 2452 with history []")
r.set('2452', json.dumps([])) ##comment this line and rerun for viewing dup checks <-------------------------
print(f"2452:{r.get('2452')}")
print("adding song to history")

def add_to_history(user_id, song_data, song_key):
    """
    Add a song to the user's history, ensuring no duplicate entries
    (same song name and artist name).
    """
    # key = f"user:{user_id}"  # Key for Redis
    existing_history = r.get(user_id)  # Get existing history

    # Parse existing history or initialize an empty list if not found
    history = json.loads(existing_history) if existing_history else []

    
    # Check for duplicates based on song name and artist name
    is_duplicate = any(
        isinstance(song, dict) and
        song.get('songName') == song_data.get('songName') and
        song.get('artistName') == song_data.get('artistName')
        for song in history
    )


    # If not a duplicate, add the new song data with the song_key
    if not is_duplicate:
        history.append(song_key)  # Append the song to history

        # Save the updated history back to Redis
        r.set(user_id, json.dumps(history))
        print(f"History updated for user {user_id}: {history}")
    else:
        print(f"Duplicate song not added for user {user_id}: {song_data['songName']} by {song_data['artistName']}------------------------------------------------------")

# Example usage
add_to_history('2452', v1, 'song:abcd1234efgh5678')
print(f"2452:{r.get('2452')}")
add_to_history('2452', v2, 'song:ijkl9012mnop3456')
print("\nHistory-------")
for song in json.loads(r.get('2452')):
    print(song)
    print(r.get(song), end="\n\n")