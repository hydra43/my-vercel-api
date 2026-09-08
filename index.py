from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/api")
def root():
    return {"status": "success", "message": "API is online and ready!"}

@app.get("/api/song")
def get_song(q: str):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'default_search': 'ytsearch1',
            'noplaylist': True,
            'quiet': True,
            'skip_download': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['mweb']
                }
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(q, download=False)
            if 'entries' in info:
                video_info = info['entries'][0]
            else:
                video_info = info
                
            title = video_info.get('title', 'Unknown Title')
            audio_url = video_info.get('url', '')
            
            if not audio_url:
                formats = video_info.get('formats', [])
                for f in formats:
                    if f.get('url') and f.get('acodec') != 'none':
                        audio_url = f['url']
                        break
            
            if not audio_url:
                raise HTTPException(status_code=404, detail="Audio URL not found")
                
            return {
                "status": "success",
                "title": title,
                "downloadUrl": audio_url
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
