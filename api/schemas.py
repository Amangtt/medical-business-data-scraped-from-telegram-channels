from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# 📌 Schema for Telegram business messages
class MedicalBusinessBase(BaseModel):
    channel_title: str
    channel_username: Optional[str] = None
    message_id: Optional[int] = None
    message: Optional[str] = None
    message_date: Optional[datetime] = None
    media_path: Optional[str] = None
    emoji_used: Optional[str] = None
    youtube_links: Optional[str] = None


class MedicalBusinessCreate(MedicalBusinessBase):
    """Schema for creating a new medical business record"""
    pass


class MedicalBusinessResponse(MedicalBusinessBase):
    """Schema for returning a medical business record"""
    id: int

    class Config:
        orm_mode = True


# 📌 Schema for Object Detection results
class ObjectDetectionBase(BaseModel):
    filename: str
    class_label: str
    confidence: Optional[float] = None
    bbox: Optional[str] = None


class ObjectDetectionCreate(ObjectDetectionBase):
    """Schema for creating a new object detection record"""
    pass


class ObjectDetectionResponse(ObjectDetectionBase):
    """Schema for returning an object detection record"""
    id: int

    class Config:
        orm_mode = True
