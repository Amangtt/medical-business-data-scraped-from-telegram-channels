from sqlalchemy import Column, Integer, String, DateTime, Text,Float
from database import Base

class Item(Base):
    __tablename__ = "medical_businesses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_title = Column(String(255), nullable=False)
    channel_username = Column(String(100), nullable=True)
    message_id = Column(Integer, nullable=True)
    message = Column(Text, nullable=True)
    message_date = Column(DateTime, nullable=True)  # TIMESTAMP in SQL
    media_path = Column(Text, nullable=True)
    emoji_used = Column(Text, nullable=True) 
    youtube_links = Column(Text, nullable=True)

# 📌 Table 2: Stores object detection results
class ObjectDetection(Base):
    __tablename__ = "object_detection"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    class_label = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=True)
    bbox = Column(Text, nullable=True)  # JSON option available if needed