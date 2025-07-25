from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid


@dataclass
class StyleDNA:
    """StyleDNA domain entity representing a user's style profile."""
    
    id: uuid.UUID
    user_id: uuid.UUID
    quiz_responses: Dict[str, Any]
    style_profile: Dict[str, Any]
    preferred_styles: List[str] = field(default_factory=list)
    preferred_colors: List[str] = field(default_factory=list)
    lifestyle_factors: Dict[str, Any] = field(default_factory=dict)
    version: str = "1.0"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Post-initialization validation."""
        if not self.quiz_responses:
            raise ValueError("Quiz responses are required")
        
        if not self.style_profile:
            raise ValueError("Style profile is required")
    
    @classmethod
    def create_from_quiz(
        cls,
        user_id: uuid.UUID,
        quiz_responses: Dict[str, Any]
    ) -> "StyleDNA":
        """Create StyleDNA from quiz responses."""
        # Generate style profile from quiz responses
        style_profile = cls._calculate_style_profile(quiz_responses)
        preferred_styles = cls._extract_preferred_styles(quiz_responses)
        preferred_colors = cls._extract_preferred_colors(quiz_responses)
        lifestyle_factors = cls._extract_lifestyle_factors(quiz_responses)
        
        return cls(
            id=uuid.uuid4(),
            user_id=user_id,
            quiz_responses=quiz_responses,
            style_profile=style_profile,
            preferred_styles=preferred_styles,
            preferred_colors=preferred_colors,
            lifestyle_factors=lifestyle_factors,
            version="1.0"
        )
    
    @staticmethod
    def _calculate_style_profile(quiz_responses: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate style profile from quiz responses."""
        # This is a simplified calculation - in a real app, this would be more complex
        profile = {
            "style_confidence": quiz_responses.get("style_confidence", 5),
            "occasion_focus": quiz_responses.get("primary_occasions", []),
            "comfort_priority": quiz_responses.get("comfort_level", 5),
            "trend_following": quiz_responses.get("trend_interest", 3),
            "budget_consciousness": quiz_responses.get("budget_range", "medium"),
            "sustainability_focus": quiz_responses.get("sustainability_important", False)
        }
        
        # Calculate overall style score
        profile["overall_score"] = (
            profile["style_confidence"] * 0.3 +
            profile["comfort_priority"] * 0.2 +
            profile["trend_following"] * 0.2 +
            (5 if profile["sustainability_focus"] else 3) * 0.3
        )
        
        return profile
    
    @staticmethod
    def _extract_preferred_styles(quiz_responses: Dict[str, Any]) -> List[str]:
        """Extract preferred styles from quiz responses."""
        styles = []
        
        if "preferred_styles" in quiz_responses:
            styles.extend(quiz_responses["preferred_styles"])
        
        if "style_inspiration" in quiz_responses:
            styles.extend(quiz_responses["style_inspiration"])
        
        # Remove duplicates and return
        return list(set(styles))
    
    @staticmethod
    def _extract_preferred_colors(quiz_responses: Dict[str, Any]) -> List[str]:
        """Extract preferred colors from quiz responses."""
        colors = []
        
        if "favorite_colors" in quiz_responses:
            colors.extend(quiz_responses["favorite_colors"])
        
        if "avoid_colors" in quiz_responses:
            # Store colors to avoid with negative prefix
            avoid_colors = [f"avoid_{color}" for color in quiz_responses["avoid_colors"]]
            colors.extend(avoid_colors)
        
        return colors
    
    @staticmethod
    def _extract_lifestyle_factors(quiz_responses: Dict[str, Any]) -> Dict[str, Any]:
        """Extract lifestyle factors from quiz responses."""
        return {
            "work_environment": quiz_responses.get("work_environment", "office"),
            "activity_level": quiz_responses.get("activity_level", "moderate"),
            "social_events": quiz_responses.get("social_frequency", "sometimes"),
            "travel_frequency": quiz_responses.get("travel_frequency", "rarely"),
            "season_preference": quiz_responses.get("favorite_season", "spring"),
            "body_type_confidence": quiz_responses.get("body_confidence", 5)
        }
    
    def update_from_quiz(self, quiz_responses: Dict[str, Any]) -> "StyleDNA":
        """Update StyleDNA from new quiz responses and return updated entity."""
        from datetime import datetime
        
        updated_style_dna = StyleDNA(
            id=self.id,
            user_id=self.user_id,
            quiz_responses=quiz_responses,
            style_profile=self._calculate_style_profile(quiz_responses),
            preferred_styles=self._extract_preferred_styles(quiz_responses),
            preferred_colors=self._extract_preferred_colors(quiz_responses),
            lifestyle_factors=self._extract_lifestyle_factors(quiz_responses),
            version=self.version,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )
        
        return updated_style_dna
    
    def update_profile(self, updates: Dict[str, Any]) -> "StyleDNA":
        """Update specific profile fields and return updated entity."""
        from datetime import datetime
        
        # Create updated entity with selective updates
        updated_style_dna = StyleDNA(
            id=self.id,
            user_id=self.user_id,
            quiz_responses=self.quiz_responses,
            style_profile=self.style_profile,
            preferred_styles=updates.get("preferred_styles", self.preferred_styles),
            preferred_colors=updates.get("preferred_colors", self.preferred_colors),
            lifestyle_factors=updates.get("lifestyle_factors", self.lifestyle_factors),
            version=self.version,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )
        
        return updated_style_dna
    
    def get_style_recommendations(self) -> Dict[str, Any]:
        """Get style recommendations based on the profile."""
        return {
            "recommended_styles": self.preferred_styles[:3],  # Top 3 styles
            "recommended_colors": [
                color for color in self.preferred_colors 
                if not color.startswith("avoid_")
            ][:5],  # Top 5 colors
            "avoid_colors": [
                color.replace("avoid_", "") for color in self.preferred_colors 
                if color.startswith("avoid_")
            ],
            "key_occasions": self.style_profile.get("occasion_focus", []),
            "comfort_level": self.style_profile.get("comfort_priority", 5),
            "trend_affinity": self.style_profile.get("trend_following", 3)
        }
    
    def matches_lifestyle(self, item_tags: Dict[str, Any]) -> float:
        """Calculate how well an item matches the user's lifestyle (0-1 score)."""
        score = 0.0
        total_factors = 0
        
        # Check work environment compatibility
        if "occasion" in item_tags:
            total_factors += 1
            work_env = self.lifestyle_factors.get("work_environment", "office")
            if work_env in item_tags["occasion"] or "versatile" in item_tags.get("occasion", []):
                score += 0.3
        
        # Check activity level compatibility
        if "comfort" in item_tags:
            total_factors += 1
            activity_level = self.lifestyle_factors.get("activity_level", "moderate")
            comfort_rating = item_tags.get("comfort", 3)
            if activity_level == "high" and comfort_rating >= 4:
                score += 0.3
            elif activity_level == "low" and comfort_rating >= 2:
                score += 0.3
            elif activity_level == "moderate":
                score += 0.3
        
        # Check style preference match
        if "style" in item_tags:
            total_factors += 1
            item_style = item_tags.get("style", "")
            if item_style in self.preferred_styles:
                score += 0.4
        
        return score / max(total_factors, 1) if total_factors > 0 else 0.5
