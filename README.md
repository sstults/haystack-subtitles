# Haystack Subtitle Collection

This project details the process for collecting and processing YouTube auto-generated captions for the Haystack Conference playlists.

## Installation

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Then add a `.env` file to the project's root directory that contains your OPENAI_API_KEY.


## Handy Commnads
Get the list of all videos (this isn't working to get just a flat list of playlists - removing the extra slash doesn't help)
```bash
yt-dlp --flat-playlist -J "https://www.youtube.com/@OpenSourceConnections//playlists" > data/playlists.json
```

Download the captions for Haystack EU 2024
```bash
yt-dlp --windows-filenames --write-description --write-auto-subs  --skip-download --sub-lang en https://www.youtube.com/playlist\?list\=PLCoJWKqBHERvq9-C7L8gyHA2aibuSkOTH
```

Download the captions for Haystack US 2024
```bash
yt-dlp --windows-filenames --write-description --write-auto-subs  --skip-download --sub-lang en https://www.youtube.com/playlist\?list\=PLCoJWKqBHERs3G3WLLgRsgN5GgzRYtB2K
```
