from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/")
def root():
    return {"status": "success", "message": "API is online and ready!"}

@app.get("/ytsearch")
def yt_search(q: str):
    try:
        ydl_opts = {
            'default_search': 'ytsearch5',
            'noplaylist': True,
            'quiet': True,
            'skip_download': True,
            'socket_timeout': 30,
            'extractor_args': {
                'youtube': {
                    'player_client': ['web_creator']
                }
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch5:{q}", download=False)
            entries = info.get('entries', [])
            
            results = []
            for entry in entries:
                results.append({
                    "title": entry.get('title', 'Unknown Title'),
                    "url": f"https://www.youtube.com/watch?v={entry.get('id')}",
                    "duration": entry.get('duration_string', 'N/A'),
                    "channel": entry.get('uploader', 'Unknown'),
                    "thumbnail": entry.get('thumbnail', '')
                })
                
            return {"results": results}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ytmp3")
def yt_mp3(url: str):
    try:
        ydl_opts = {
            'format': 'bestaudio',
            'noplaylist': True,
            'quiet': True,
            'skip_download': True,
            'socket_timeout': 30,
            'extractor_args': {
                'youtube': {
                    'player_client': ['web_creator']
                }
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get('title', 'Unknown Title')
            author = info.get('uploader', 'Unknown')
            audio_url = info.get('url', '')
            
            if not audio_url:
                formats = info.get('formats', [])
                for f in formats:
                    if f.get('url') and f.get('acodec') != 'none':
                        audio_url = f['url']
                        break
            
            if not audio_url:
                raise HTTPException(status_code=404, detail="Audio URL not found")
                
            return {
                "success": True,
                "title": title,
                "author": author,
                "url": audio_url
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
