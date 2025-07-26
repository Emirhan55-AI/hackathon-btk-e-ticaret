from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class ClothingItem(Base):
    """ClothingItem model for wardrobe management."""
    
    __tablename__ = "clothing_items"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    name = Column(
        String(255),
        nullable=False
    )
    
    category = Column(
        String(100),
        nullable=False,
        index=True
    )
    
    brand = Column(
        String(100),
        nullable=True
    )
    
    color = Column(
        String(50),
        nullable=True,
        index=True
    )
    
    size = Column(
        String(20),
        nullable=True
    )
    
    image_url = Column(
        Text,
        nullable=True
    )
    
    # AI-generated tags stored as JSONB
    ai_tags = Column(
        JSONB,
        nullable=True,
        default=dict
    )
    
    # User-modified tags stored as JSONB
    user_tags = Column(
        JSONB,
        nullable=True,
        default=dict
    )
    
    description = Column(
        Text,
        nullable=True
    )
    
    is_favorite = Column(
        "is_favorite",
        nullable=False,
        default=False
    )
    
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    # Relationships
    user = relationship("User", back_populates="clothing_items")
    
    def __repr__(self) -> str:
        return f"<ClothingItem(id={self.id}, name={self.name}, category={self.category})>"
