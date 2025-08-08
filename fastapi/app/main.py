import logging

from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .database import engine, Base
from .schemas import Alert
from .models import AlertModel
from .utils import get_db, fetch_video, extract_resolution

logger = logging.getLogger("uvicorn.error")

app = FastAPI()

# Create all tables, ok for a small take home, to manage migrations properly I would use Alembic
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/alerts")
async def receive_alert(alert: Alert, db: Session = Depends(get_db)):
    video_bytes = await fetch_video(alert.video)

    try:
        resolution = extract_resolution(video_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to extract resolution: {e}"
        )

    db_alert = AlertModel(
        uuid=alert.uuid,
        video=alert.video,
        timestamp=alert.timestamp,
        store=alert.store,
        resolution=resolution,
    )

    try:
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Alert with this UUID already exists"
        )

    date_str = datetime.fromtimestamp(alert.timestamp).strftime("%Y-%m-%d %H:%M:%S")

    # We simulate notification to the console
    logger.info(
        f"[Notification] Store: {alert.store} | Date: {date_str} | Resolution: {resolution}"
    )

    return {"status": "success", "resolution": resolution}
