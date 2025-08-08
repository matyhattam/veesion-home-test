from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, StringConstraints

# We check that the video is a valid format
VideoStr = Annotated[
    str, StringConstraints(pattern=r"(?i)^.*\.(mp4|avi|mov|mkv|webm)$")
]


class Alert(BaseModel):
    uuid: UUID
    video: VideoStr
    timestamp: float
    store: str
