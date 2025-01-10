# Haystack Subtitle Collection

This project details the process for collecting and processing YouTube auto-generated captions for the Haystack Conference playlists.

## Installation

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Get the list of all videos (this isn't working to get just a flat list of playlists - removing the extra slash doesn't help)
```bash
yt-dlp --flat-playlist -J "https://www.youtube.com/@OpenSourceConnections//playlists" > data/playlists.json
```

Make it pretty
```bash
jsonlint -p data/playlists.json > data/playlists-pretty.json 
```
