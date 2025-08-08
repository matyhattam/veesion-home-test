import cv2, os, httpx

from fastapi import HTTPException
from .database import SessionLocal

VIDEO_SERVER = os.getenv("VIDEO_SERVER", "http://localhost:8080")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def fetch_video(video_path: str) -> bytes:
    video_url = f"{VIDEO_SERVER}{video_path}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(video_url)
            response.raise_for_status()
            return response.content
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Video server not reachable")
    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="Video not found on server")


def extract_resolution(video_bytes: bytes) -> str:
    tmp_file = "temp_video.avi"
    with open(tmp_file, "wb") as f:
        f.write(video_bytes)

    cap = cv2.VideoCapture(tmp_file)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    os.remove(tmp_file)

    return f"{width}x{height}"
