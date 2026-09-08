from fastapi import FastAPI, HTTPException
import subprocess

app = FastAPI()

@app.get("/api")
def root():
    return {"status": "success", "message": "API is online and ready!"}

@app.get("/api/song")
def get_song(q: str):
    try:
        # yt-dlp ব্যবহার করে ইউটিউব থেকে গান বা অডিওর তথ্য খোঁজার লজিক
        ydl_opts = [
            "yt-dlp",
            f"ytsearch1:{q}",
            "--get-url",
            "--get-title",
            "--get-duration"
        ]
        result = subprocess.run(ydl_opts, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split("\n")
        
        if len(lines) >= 2:
            title = lines[0]
            audio_url = lines[1]
            return {
                "status": "success",
                "title": title,
                "downloadUrl": audio_url
            }
        else:
            raise HTTPException(status_code=404, detail="Song not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
