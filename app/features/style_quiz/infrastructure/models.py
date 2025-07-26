from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class StyleDNA(Base):
    """StyleDNA model for storing user's style profile."""
    
    __tablename__ = "style_dna"
    
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
        unique=True,  # One-to-one relationship
        index=True
    )
    
    # Quiz responses stored as JSONB
    quiz_responses = Column(
        JSONB,
        nullable=False,
        default=dict
    )
    
    # Calculated style profile stored as JSONB
    style_profile = Column(
        JSONB,
        nullable=False,
        default=dict
    )
    
    # Style preferences extracted from quiz
    preferred_styles = Column(
        JSONB,
        nullable=True,
        default=list
    )
    
    # Color preferences
    preferred_colors = Column(
        JSONB,
        nullable=True,
        default=list
    )
    
    # Lifestyle factors
    lifestyle_factors = Column(
        JSONB,
        nullable=True,
        default=dict
    )
    
    # Version for tracking quiz updates
    version = Column(
        String(10),
        nullable=False,
        default="1.0"
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
    user = relationship("User", back_populates="style_dna")
    
    def __repr__(self) -> str:
        return f"<StyleDNA(id={self.id}, user_id={self.user_id}, version={self.version})>"


# Alias for backward compatibility
StyleDNAModel = StyleDNA
