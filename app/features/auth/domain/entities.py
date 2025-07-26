from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class User:
    """User domain entity representing a user in the system."""
    
    id: uuid.UUID
    email: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Post-initialization validation."""
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email address")
        
        if self.full_name and len(self.full_name.strip()) == 0:
            self.full_name = None
    
    @classmethod
    def create_new(cls, email: str, full_name: Optional[str] = None) -> "User":
        """Create a new user instance."""
        return cls(
            id=uuid.uuid4(),
            email=email.lower().strip(),
            full_name=full_name.strip() if full_name else None,
            is_active=True,
            is_verified=False
        )
    
    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True
    
    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False
    
    def verify(self) -> None:
        """Mark user as verified."""
        self.is_verified = True
    
    def is_valid_for_login(self) -> bool:
        """Check if user can login."""
        return self.is_active and self.is_verified
