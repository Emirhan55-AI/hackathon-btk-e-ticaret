# 🧠 AURA AI - RCI QUALITY ASSURANCE ENGINE
# Recursive Criticism and Improvement System for AI Output Validation

from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import logging
from datetime import datetime
import asyncio
import numpy as np
from abc import ABC, abstractmethod

# Configure comprehensive logging for RCI quality tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ValidationStatus(Enum):
    """
    Enum representing the possible validation statuses for AI outputs.
    Used to categorize the quality and appropriateness of AI recommendations.
    """
    APPROVED = "approved"              # High quality, ready for user
    NEEDS_IMPROVEMENT = "needs_improvement"  # Fixable issues identified
    REJECTED = "rejected"              # Critical issues, should not be shown
    PENDING_REVALIDATION = "pending_revalidation"  # Awaiting re-check after fixes

class CriticalityLevel(Enum):
    """
    Enum for categorizing the severity of validation issues.
    Helps prioritize which problems need immediate attention.
    """
    LOW = "low"           # Minor style preferences, optional improvements
    MEDIUM = "medium"     # Noticeable issues that affect user experience
    HIGH = "high"         # Significant problems that could cause user dissatisfaction
    CRITICAL = "critical" # Severe issues that could harm user trust or safety

@dataclass
class ValidationCriteria:
    """
    Data structure defining the criteria used to validate AI outputs.
    Contains all the rules and thresholds for quality assessment.
    """
    # Color harmony validation parameters
    color_harmony_threshold: float = 0.7    # Minimum acceptable color harmony score
    max_color_contrast: float = 0.8          # Maximum allowed color contrast
    
    # Style coherence validation parameters  
    style_coherence_threshold: float = 0.75  # Minimum style consistency score
    formality_gap_tolerance: int = 2         # Max formality level difference allowed
    
    # Occasion appropriateness parameters
    occasion_match_threshold: float = 0.8    # Minimum occasion appropriateness score
    context_relevance_threshold: float = 0.7 # Minimum context relevance score
    
    # User preference alignment parameters
    preference_match_threshold: float = 0.75 # Minimum user preference alignment
    age_appropriateness_threshold: float = 0.8 # Minimum age appropriateness score
    
    # Overall quality thresholds
    minimum_overall_score: float = 0.7       # Overall passing score
    critical_issue_threshold: float = 0.5    # Score below which issues are critical

@dataclass
class ValidationIssue:
    """
    Data structure representing a specific validation issue found in AI output.
    Contains details about the problem and suggested improvements.
    """
    category: str                    # Type of issue (color, style, occasion, etc.)
    description: str                 # Human-readable description of the issue
    criticality: CriticalityLevel   # How severe this issue is
    confidence: float               # How confident we are this is actually an issue
    improvement_suggestion: str     # Specific suggestion for fixing this issue
    affected_components: List[str]  # Which parts of the recommendation are affected
    validation_rule_id: str        # ID of the validation rule that caught this issue

@dataclass
class ValidationResult:
    """
    Comprehensive result of validating an AI output.
    Contains scores, issues, improvements, and alternatives.
    """
    # Basic identification and metadata
    output_id: str                      # Unique identifier for this validation
    service_source: str                 # Which AI service generated the original output
    timestamp: datetime                 # When this validation was performed
    
    # Overall validation outcome
    status: ValidationStatus            # Overall approval status
    overall_score: float               # Overall quality score (0-1)
    confidence: float                  # Confidence in the validation results
    
    # Detailed scoring breakdown
    color_harmony_score: float         # Score for color combination quality
    style_coherence_score: float       # Score for style consistency
    occasion_appropriateness_score: float  # Score for occasion matching
    user_preference_score: float       # Score for user preference alignment
    
    # Issues and improvements
    issues: List[ValidationIssue]      # List of all issues found
    critical_issues: List[ValidationIssue]  # Subset of critical issues only
    improvement_suggestions: List[str] # Concrete improvement suggestions
    alternative_recommendations: List[Dict] # Alternative options generated
    
    # Metadata for tracking and learning
    validation_duration_ms: float     # How long validation took
    revalidation_required: bool       # Whether this needs to be checked again
    learning_feedback: Dict[str, Any] # Data for improving future validations

class AIOutputValidator(ABC):
    """
    Abstract base class for AI output validators.
    Each validator specializes in checking specific aspects of AI recommendations.
    """
    
    @abstractmethod
    def validate(self, ai_output: Dict[str, Any], context: Dict[str, Any]) -> Tuple[float, List[ValidationIssue]]:
        """
        Validate a specific aspect of an AI output.
        
        Args:
            ai_output: The AI recommendation to validate
            context: Additional context (user profile, occasion, etc.)
            
        Returns:
            Tuple of (score, list_of_issues)
        """
        pass
    
    @abstractmethod
    def get_validator_name(self) -> str:
        """Return the name of this validator for logging and tracking."""
        pass

class ColorHarmonyValidator(AIOutputValidator):
    """
    Validator that checks if the colors in a recommendation work well together.
    Uses color theory principles to assess harmony and contrast.
    """
    
    def __init__(self):
        # Initialize color theory knowledge base
        # These dictionaries contain color relationships and harmony rules
        self.color_wheel = {
            # Primary colors and their properties
            "red": {"hue": 0, "warmth": 1.0, "energy": 0.9},
            "orange": {"hue": 30, "warmth": 1.0, "energy": 0.8},
            "yellow": {"hue": 60, "warmth": 0.8, "energy": 0.7},
            "green": {"hue": 120, "warmth": 0.0, "energy": 0.5},
            "blue": {"hue": 240, "warmth": -0.8, "energy": 0.3},
            "purple": {"hue": 270, "warmth": -0.5, "energy": 0.6},
            "pink": {"hue": 330, "warmth": 0.5, "energy": 0.7},
            "brown": {"hue": 30, "warmth": 0.3, "energy": 0.2},
            "black": {"hue": 0, "warmth": 0.0, "energy": 0.1},
            "white": {"hue": 0, "warmth": 0.0, "energy": 0.9},
            "gray": {"hue": 0, "warmth": 0.0, "energy": 0.5}
        }
        
        # Define which color combinations work well together
        self.harmonious_combinations = {
            "complementary": [("red", "green"), ("blue", "orange"), ("yellow", "purple")],
            "analogous": [("red", "orange"), ("blue", "green"), ("yellow", "green")],
            "triadic": [("red", "blue", "yellow"), ("orange", "green", "purple")],
            "neutral_safe": [("black", "white"), ("gray", "white"), ("brown", "beige")]
        }
        
    def validate(self, ai_output: Dict[str, Any], context: Dict[str, Any]) -> Tuple[float, List[ValidationIssue]]:
        """
        Validate the color harmony of an AI fashion recommendation.
        
        This function analyzes the colors in a fashion recommendation to determine
        if they work well together according to color theory principles.
        """
        issues = []  # List to collect any color harmony issues found
        
        # Extract colors from the AI recommendation
        colors = self._extract_colors_from_output(ai_output)
        
        if len(colors) < 2:
            # If there's only one color, it's automatically harmonious
            logger.info("Single color detected, automatically harmonious")
            return 1.0, []
        
        # Check for common color harmony violations
        harmony_score = 0.0
        total_combinations = 0
        
        # Analyze each pair of colors in the recommendation
        for i in range(len(colors)):
            for j in range(i + 1, len(colors)):
                color1, color2 = colors[i], colors[j]
                combination_score = self._analyze_color_pair(color1, color2)
                harmony_score += combination_score
                total_combinations += 1
                
                # If this combination is problematic, create an issue
                if combination_score < 0.5:
                    issue = ValidationIssue(
                        category="color_harmony",
                        description=f"Color combination {color1} + {color2} may be jarring or inappropriate",
                        criticality=CriticalityLevel.MEDIUM if combination_score < 0.3 else CriticalityLevel.LOW,
                        confidence=0.8,
                        improvement_suggestion=self._suggest_color_improvement(color1, color2),
                        affected_components=[color1, color2],
                        validation_rule_id="color_harmony_pair_analysis"
                    )
                    issues.append(issue)
        
        # Calculate overall harmony score
        if total_combinations > 0:
            harmony_score = harmony_score / total_combinations
        else:
            harmony_score = 1.0  # No combinations to analyze
            
        logger.info(f"Color harmony analysis complete: score={harmony_score:.2f}, issues={len(issues)}")
        return harmony_score, issues
    
    def _extract_colors_from_output(self, ai_output: Dict[str, Any]) -> List[str]:
        """
        Extract color information from an AI recommendation.
        Handles various formats that AI services might use to specify colors.
        """
        colors = []
        
        # Check different possible locations for color information
        if "colors" in ai_output:
            if isinstance(ai_output["colors"], list):
                colors.extend(ai_output["colors"])
            else:
                colors.append(ai_output["colors"])
                
        if "items" in ai_output:
            # Extract colors from individual clothing items
            for item in ai_output.get("items", []):
                if isinstance(item, dict) and "color" in item:
                    colors.append(item["color"])
                    
        # Normalize color names to our color wheel vocabulary
        normalized_colors = []
        for color in colors:
            normalized = self._normalize_color_name(color.lower())
            if normalized:
                normalized_colors.append(normalized)
                
        return normalized_colors
    
    def _normalize_color_name(self, color_name: str) -> Optional[str]:
        """
        Convert various color name formats to our standard color wheel names.
        Handles synonyms and variations in color naming.
        """
        # Dictionary mapping various color names to our standard names
        color_mappings = {
            "crimson": "red", "scarlet": "red", "burgundy": "red", "maroon": "red",
            "navy": "blue", "teal": "blue", "turquoise": "blue", "azure": "blue",
            "lime": "green", "emerald": "green", "forest": "green", "olive": "green",
            "lavender": "purple", "violet": "purple", "magenta": "purple", "indigo": "purple",
            "gold": "yellow", "lemon": "yellow", "cream": "yellow", "ivory": "white",
            "tan": "brown", "beige": "brown", "khaki": "brown", "bronze": "brown",
            "silver": "gray", "charcoal": "gray", "slate": "gray"
        }
        
        # First check if it's already a standard color
        if color_name in self.color_wheel:
            return color_name
            
        # Then check our mappings
        if color_name in color_mappings:
            return color_mappings[color_name]
            
        # If we can't recognize the color, log it and return None
        logger.warning(f"Unrecognized color name: {color_name}")
        return None
    
    def _analyze_color_pair(self, color1: str, color2: str) -> float:
        """
        Analyze how well two colors work together.
        Returns a score from 0.0 (terrible) to 1.0 (excellent).
        """
        # Check if this is a known harmonious combination
        for combo_type, combinations in self.harmonious_combinations.items():
            for combo in combinations:
                if (color1 in combo and color2 in combo) or (color2 in combo and color1 in combo):
                    logger.debug(f"Found harmonious {combo_type} combination: {color1} + {color2}")
                    return 0.9  # High score for known good combinations
        
        # Get color properties for analysis
        color1_props = self.color_wheel.get(color1, {})
        color2_props = self.color_wheel.get(color2, {})
        
        if not color1_props or not color2_props:
            # If we don't have data for one of the colors, give a neutral score
            return 0.6
        
        # Calculate hue difference (how different the colors are on the color wheel)
        hue1 = color1_props.get("hue", 0)
        hue2 = color2_props.get("hue", 0)
        hue_diff = abs(hue1 - hue2)
        hue_diff = min(hue_diff, 360 - hue_diff)  # Handle wrap-around
        
        # Calculate warmth compatibility (warm colors with warm, cool with cool)
        warmth1 = color1_props.get("warmth", 0)
        warmth2 = color2_props.get("warmth", 0)
        warmth_compatibility = 1.0 - abs(warmth1 - warmth2) / 2.0
        
        # Calculate energy compatibility (high energy colors can clash)
        energy1 = color1_props.get("energy", 0.5)
        energy2 = color2_props.get("energy", 0.5)
        energy_compatibility = 1.0 - abs(energy1 - energy2) / 2.0
        
        # Combine factors to get overall compatibility score
        if hue_diff < 30:  # Very similar colors (analogous)
            score = 0.8 + 0.2 * warmth_compatibility
        elif 150 < hue_diff < 210:  # Opposite colors (complementary)
            score = 0.7 + 0.3 * energy_compatibility
        elif hue_diff > 300:  # Nearly opposite
            score = 0.5 + 0.5 * warmth_compatibility
        else:  # Random combinations
            score = 0.4 + 0.3 * warmth_compatibility + 0.3 * energy_compatibility
            
        logger.debug(f"Color pair analysis {color1}+{color2}: hue_diff={hue_diff}, score={score:.2f}")
        return max(0.0, min(1.0, score))  # Ensure score is between 0 and 1
    
    def _suggest_color_improvement(self, color1: str, color2: str) -> str:
        """
        Generate a specific suggestion for improving a problematic color combination.
        Provides actionable advice for better color harmony.
        """
        # Get color properties to understand the issue
        color1_props = self.color_wheel.get(color1, {})
        color2_props = self.color_wheel.get(color2, {})
        
        # Check if the issue is high contrast
        if color1_props and color2_props:
            warmth1 = color1_props.get("warmth", 0)
            warmth2 = color2_props.get("warmth", 0)
            
            if abs(warmth1 - warmth2) > 1.5:
                return f"Try replacing {color2} with a warmer tone to match {color1}, or add a neutral bridge color like gray or beige"
        
        # Provide general improvement suggestions
        suggestions = [
            f"Consider softening the contrast by choosing a lighter or darker shade of {color2}",
            f"Add a neutral color (white, gray, or beige) to balance {color1} and {color2}",
            f"Replace {color2} with a color that's more harmonious with {color1}",
            f"Use {color2} as a small accent rather than a main color with {color1}"
        ]
        
        # Return a contextually appropriate suggestion
        return suggestions[0]  # For now, return the first suggestion
    
    def get_validator_name(self) -> str:
        """Return the name of this validator for identification purposes."""
        return "ColorHarmonyValidator"

class StyleCoherenceValidator(AIOutputValidator):
    """
    Validator that checks if all elements in a recommendation have consistent style.
    Ensures that formal pieces aren't mixed inappropriately with casual pieces.
    """
    
    def __init__(self):
        # Define formality levels for different clothing items and styles
        # Higher numbers = more formal
        self.formality_levels = {
            # Formal wear (high formality)
            "suit": 5, "blazer": 4, "dress_shirt": 4, "tie": 5, "dress_shoes": 4,
            "cocktail_dress": 4, "evening_gown": 5, "formal_dress": 4,
            
            # Business casual (medium-high formality)
            "chinos": 3, "button_down": 3, "polo_shirt": 2, "loafers": 3,
            "blouse": 3, "pencil_skirt": 3, "cardigan": 2,
            
            # Casual wear (low formality)
            "jeans": 1, "t_shirt": 1, "sneakers": 1, "hoodie": 1,
            "casual_dress": 2, "sandals": 1, "shorts": 1,
            
            # Very casual/athletic (very low formality)
            "sweatpants": 0, "athletic_wear": 0, "flip_flops": 0
        }
        
        # Define style categories that should be consistent
        self.style_categories = {
            "formal": ["suit", "blazer", "dress_shirt", "tie", "dress_shoes", "formal_dress"],
            "business_casual": ["chinos", "button_down", "polo_shirt", "loafers", "blouse"],
            "casual": ["jeans", "t_shirt", "sneakers", "casual_dress", "cardigan"],
            "athletic": ["sweatpants", "athletic_wear", "sneakers", "hoodie"],
            "bohemian": ["flowy_dress", "sandals", "accessories", "natural_fabrics"],
            "vintage": ["retro_pieces", "classic_cuts", "traditional_patterns"]
        }
    
    def validate(self, ai_output: Dict[str, Any], context: Dict[str, Any]) -> Tuple[float, List[ValidationIssue]]:
        """
        Validate the style coherence of an AI fashion recommendation.
        
        Checks if all items in the recommendation have compatible styles
        and appropriate formality levels for the context.
        """
        issues = []
        
        # Extract clothing items from the AI output
        items = self._extract_items_from_output(ai_output)
        
        if len(items) < 2:
            # Can't have style conflicts with only one item
            logger.info("Single item detected, style coherence automatically valid")
            return 1.0, []
        
        # Analyze formality level consistency
        formality_score, formality_issues = self._analyze_formality_consistency(items, context)
        issues.extend(formality_issues)
        
        # Analyze style category consistency
        style_score, style_issues = self._analyze_style_consistency(items)
        issues.extend(style_issues)
        
        # Calculate overall style coherence score
        overall_score = (formality_score + style_score) / 2.0
        
        logger.info(f"Style coherence analysis complete: score={overall_score:.2f}, issues={len(issues)}")
        return overall_score, issues
    
    def _extract_items_from_output(self, ai_output: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract individual clothing items from the AI recommendation.
        Handles various formats that AI services might use.
        """
        items = []
        
        # Check for items list
        if "items" in ai_output and isinstance(ai_output["items"], list):
            items.extend(ai_output["items"])
        
        # Check for individual item fields
        item_fields = ["top", "bottom", "shoes", "accessories", "outerwear"]
        for field in item_fields:
            if field in ai_output:
                item_data = ai_output[field]
                if isinstance(item_data, dict):
                    items.append(item_data)
                elif isinstance(item_data, str):
                    items.append({"type": field, "name": item_data})
        
        return items
    
    def _analyze_formality_consistency(self, items: List[Dict], context: Dict) -> Tuple[float, List[ValidationIssue]]:
        """
        Check if the formality levels of all items are consistent and appropriate.
        """
        issues = []
        
        # Get formality level for each item
        formality_levels = []
        for item in items:
            item_type = self._identify_item_type(item)
            formality = self.formality_levels.get(item_type, 2)  # Default to medium formality
            formality_levels.append((item_type, formality))
        
        if not formality_levels:
            return 1.0, []
        
        # Calculate formality range and average
        formalities = [f[1] for f in formality_levels]
        min_formality = min(formalities)
        max_formality = max(formalities)
        avg_formality = sum(formalities) / len(formalities)
        formality_range = max_formality - min_formality
        
        # Check for excessive formality gaps
        if formality_range > 3:  # More than 3 levels apart is problematic
            issue = ValidationIssue(
                category="style_coherence",
                description=f"Large formality gap: mixing very formal and very casual items",
                criticality=CriticalityLevel.HIGH,
                confidence=0.9,
                improvement_suggestion="Choose items with more similar formality levels, or add bridge pieces",
                affected_components=[f"{item[0]} (level {item[1]})" for item in formality_levels],
                validation_rule_id="formality_gap_check"
            )
            issues.append(issue)
        
        # Check context appropriateness
        expected_formality = self._get_expected_formality_for_context(context)
        if expected_formality and abs(avg_formality - expected_formality) > 1.5:
            issue = ValidationIssue(
                category="style_coherence",
                description=f"Outfit formality ({avg_formality:.1f}) doesn't match occasion expectation ({expected_formality})",
                criticality=CriticalityLevel.MEDIUM,
                confidence=0.8,
                improvement_suggestion=f"Adjust items to better match the {context.get('occasion', 'occasion')} formality level",
                affected_components=[item[0] for item in formality_levels],
                validation_rule_id="context_formality_match"
            )
            issues.append(issue)
        
        # Calculate score based on consistency and appropriateness
        consistency_score = max(0.0, 1.0 - (formality_range / 5.0))  # Penalize large gaps
        if expected_formality:
            appropriateness_score = max(0.0, 1.0 - abs(avg_formality - expected_formality) / 3.0)
            overall_score = (consistency_score + appropriateness_score) / 2.0
        else:
            overall_score = consistency_score
        
        return overall_score, issues
    
    def _analyze_style_consistency(self, items: List[Dict]) -> Tuple[float, List[ValidationIssue]]:
        """
        Check if items belong to compatible style categories.
        """
        issues = []
        
        # Identify style categories for each item
        item_styles = []
        for item in items:
            item_type = self._identify_item_type(item)
            styles = self._get_style_categories_for_item(item_type)
            item_styles.append((item_type, styles))
        
        # Find common style categories
        if item_styles:
            common_styles = set(item_styles[0][1])
            for item_type, styles in item_styles[1:]:
                common_styles = common_styles.intersection(set(styles))
            
            # If no common styles, look for conflicts
            if not common_styles:
                issue = ValidationIssue(
                    category="style_coherence", 
                    description="Items belong to incompatible style categories",
                    criticality=CriticalityLevel.MEDIUM,
                    confidence=0.7,
                    improvement_suggestion="Choose items that share at least one style category",
                    affected_components=[item[0] for item in item_styles],
                    validation_rule_id="style_category_compatibility"
                )
                issues.append(issue)
                return 0.3, issues
            else:
                # Score based on how many style categories are shared
                return min(1.0, len(common_styles) / 2.0), issues
        
        return 1.0, issues
    
    def _identify_item_type(self, item: Dict[str, Any]) -> str:
        """
        Identify the type of clothing item from its description.
        """
        # Check explicit type field
        if "type" in item:
            return item["type"].lower().replace(" ", "_")
        
        # Check name field for type identification
        if "name" in item:
            name = item["name"].lower()
            # Simple keyword matching for common items
            if "suit" in name or "blazer" in name:
                return "blazer"
            elif "shirt" in name and ("dress" in name or "button" in name):
                return "dress_shirt"
            elif "jeans" in name:
                return "jeans"
            elif "sneakers" in name or "athletic" in name:
                return "sneakers"
            # Add more pattern matching as needed
        
        # Default fallback
        return "unknown_item"
    
    def _get_style_categories_for_item(self, item_type: str) -> List[str]:
        """
        Get the style categories that an item type belongs to.
        """
        categories = []
        for style, items in self.style_categories.items():
            if item_type in items:
                categories.append(style)
        
        # If no specific categories found, infer from formality
        if not categories:
            formality = self.formality_levels.get(item_type, 2)
            if formality >= 4:
                categories.append("formal")
            elif formality >= 2:
                categories.append("business_casual")
            else:
                categories.append("casual")
        
        return categories
    
    def _get_expected_formality_for_context(self, context: Dict[str, Any]) -> Optional[float]:
        """
        Determine the expected formality level based on the context/occasion.
        """
        occasion = context.get("occasion", "").lower()
        
        formality_map = {
            "work": 3.5, "business": 4.0, "office": 3.5, "meeting": 4.0,
            "formal": 5.0, "black_tie": 5.0, "wedding": 4.5, "cocktail": 4.0,
            "dinner": 3.0, "date": 2.5, "party": 2.0,
            "casual": 1.5, "weekend": 1.0, "home": 0.5,
            "gym": 0.0, "exercise": 0.0, "sports": 0.0
        }
        
        return formality_map.get(occasion)
    
    def get_validator_name(self) -> str:
        """Return the name of this validator for identification purposes."""
        return "StyleCoherenceValidator"

class RCIQualityEngine:
    """
    Main engine for the Recursive Criticism and Improvement system.
    Coordinates multiple validators and generates comprehensive quality assessments.
    """
    
    def __init__(self, criteria: Optional[ValidationCriteria] = None):
        """
        Initialize the RCI Quality Engine with validation criteria and validators.
        
        Args:
            criteria: Custom validation criteria, or None to use defaults
        """
        # Set up validation criteria (rules for what constitutes good recommendations)
        self.criteria = criteria or ValidationCriteria()
        
        # Initialize all available validators
        self.validators = [
            ColorHarmonyValidator(),
            StyleCoherenceValidator(),
            # Additional validators can be added here in the future
        ]
        
        # Set up logging for quality tracking
        logger.info(f"RCI Quality Engine initialized with {len(self.validators)} validators")
        logger.info(f"Validation criteria: min_score={self.criteria.minimum_overall_score}")
    
    async def validate_ai_output(self, ai_output: Dict[str, Any], context: Dict[str, Any]) -> ValidationResult:
        """
        Perform comprehensive validation of an AI recommendation.
        
        This is the main entry point for the RCI system. It runs all validators
        and generates a complete quality assessment with improvement suggestions.
        
        Args:
            ai_output: The AI recommendation to validate
            context: Additional context (user profile, occasion, etc.)
            
        Returns:
            Complete validation result with scores, issues, and improvements
        """
        start_time = datetime.now()
        
        # Generate unique ID for this validation
        output_id = f"val_{int(start_time.timestamp())}_{hash(str(ai_output)) % 10000}"
        
        logger.info(f"Starting validation {output_id} for output from {context.get('service_source', 'unknown')}")
        
        # Run all validators in parallel for efficiency
        validation_tasks = []
        for validator in self.validators:
            task = asyncio.create_task(self._run_validator_safely(validator, ai_output, context))
            validation_tasks.append(task)
        
        # Wait for all validators to complete
        validator_results = await asyncio.gather(*validation_tasks)
        
        # Aggregate results from all validators
        all_issues = []
        scores = {}
        
        for i, (validator_score, validator_issues) in enumerate(validator_results):
            validator_name = self.validators[i].get_validator_name()
            scores[validator_name] = validator_score
            all_issues.extend(validator_issues)
            
            logger.debug(f"{validator_name}: score={validator_score:.2f}, issues={len(validator_issues)}")
        
        # Calculate overall quality score
        overall_score = self._calculate_overall_score(scores)
        
        # Determine validation status
        status = self._determine_validation_status(overall_score, all_issues)
        
        # Generate improvement suggestions
        improvements = self._generate_improvement_suggestions(all_issues, ai_output, context)
        
        # Generate alternative recommendations if needed
        alternatives = self._generate_alternatives(ai_output, all_issues) if status != ValidationStatus.APPROVED else []
        
        # Identify critical issues
        critical_issues = [issue for issue in all_issues if issue.criticality == CriticalityLevel.CRITICAL]
        
        # Calculate how long validation took
        duration = (datetime.now() - start_time).total_seconds() * 1000
        
        # Create comprehensive validation result
        result = ValidationResult(
            output_id=output_id,
            service_source=context.get("service_source", "unknown"),
            timestamp=start_time,
            status=status,
            overall_score=overall_score,
            confidence=self._calculate_confidence(scores, all_issues),
            color_harmony_score=scores.get("ColorHarmonyValidator", 0.5),
            style_coherence_score=scores.get("StyleCoherenceValidator", 0.5),
            occasion_appropriateness_score=0.8,  # Placeholder - implement in future validator
            user_preference_score=0.8,  # Placeholder - implement in future validator
            issues=all_issues,
            critical_issues=critical_issues,
            improvement_suggestions=improvements,
            alternative_recommendations=alternatives,
            validation_duration_ms=duration,
            revalidation_required=(status == ValidationStatus.NEEDS_IMPROVEMENT),
            learning_feedback={}  # Temporarily disabled to debug the issue
        )
        
        # Generate learning feedback after result is created (temporarily disabled)
        # result.learning_feedback = self._generate_learning_feedback(ai_output, result)
        
        logger.info(f"Validation {output_id} complete: status={status.value}, score={overall_score:.2f}, duration={duration:.1f}ms")
        
        return result
    
    async def _run_validator_safely(self, validator: AIOutputValidator, ai_output: Dict, context: Dict) -> Tuple[float, List[ValidationIssue]]:
        """
        Run a validator with error handling to prevent one validator from breaking the whole system.
        
        Args:
            validator: The validator to run
            ai_output: The AI output to validate
            context: Validation context
            
        Returns:
            Tuple of (score, issues) or default values if validator fails
        """
        try:
            return validator.validate(ai_output, context)
        except Exception as e:
            logger.error(f"Validator {validator.get_validator_name()} failed: {str(e)}")
            # Return neutral score and an issue about the validator failure
            error_issue = ValidationIssue(
                category="system_error",
                description=f"Validator {validator.get_validator_name()} encountered an error",
                criticality=CriticalityLevel.LOW,
                confidence=1.0,
                improvement_suggestion="System will retry validation",
                affected_components=["validation_system"],
                validation_rule_id="validator_error_handling"
            )
            return 0.5, [error_issue]
    
    def _calculate_overall_score(self, scores: Dict[str, float]) -> float:
        """
        Calculate the overall quality score from individual validator scores.
        
        Uses weighted averaging where some validators are more important than others.
        """
        if not scores:
            return 0.0
        
        # Define weights for different validators (sum should equal 1.0)
        weights = {
            "ColorHarmonyValidator": 0.4,      # Color is very important in fashion
            "StyleCoherenceValidator": 0.4,    # Style consistency is also crucial
            # Future validators will get portions of the remaining 0.2
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for validator_name, score in scores.items():
            weight = weights.get(validator_name, 0.1)  # Default weight for new validators
            weighted_sum += score * weight
            total_weight += weight
        
        # Normalize by actual total weight (in case we don't have all expected validators)
        if total_weight > 0:
            return weighted_sum / total_weight
        else:
            return sum(scores.values()) / len(scores)  # Simple average as fallback
    
    def _determine_validation_status(self, overall_score: float, issues: List[ValidationIssue]) -> ValidationStatus:
        """
        Determine the overall validation status based on score and issues found.
        """
        # Check for critical issues first
        has_critical = any(issue.criticality == CriticalityLevel.CRITICAL for issue in issues)
        if has_critical:
            return ValidationStatus.REJECTED
        
        # Check overall score against thresholds
        if overall_score >= self.criteria.minimum_overall_score:
            return ValidationStatus.APPROVED
        elif overall_score >= self.criteria.critical_issue_threshold:
            return ValidationStatus.NEEDS_IMPROVEMENT
        else:
            return ValidationStatus.REJECTED
    
    def _calculate_confidence(self, scores: Dict[str, float], issues: List[ValidationIssue]) -> float:
        """
        Calculate confidence in the validation results.
        Higher confidence when validators agree and issues are clear.
        """
        if not scores:
            return 0.5
        
        # Calculate variance in scores (lower variance = higher confidence)
        score_values = list(scores.values())
        mean_score = sum(score_values) / len(score_values)
        variance = sum((score - mean_score) ** 2 for score in score_values) / len(score_values)
        consistency_confidence = max(0.0, 1.0 - variance)
        
        # Calculate issue confidence (average of individual issue confidences)
        if issues:
            issue_confidence = sum(issue.confidence for issue in issues) / len(issues)
        else:
            issue_confidence = 0.9  # High confidence when no issues found
        
        # Combine factors
        overall_confidence = (consistency_confidence + issue_confidence) / 2.0
        return max(0.1, min(1.0, overall_confidence))  # Clamp between 0.1 and 1.0
    
    def _generate_improvement_suggestions(self, issues: List[ValidationIssue], ai_output: Dict, context: Dict) -> List[str]:
        """
        Generate concrete, actionable improvement suggestions based on identified issues.
        """
        suggestions = []
        
        # Collect unique improvement suggestions from issues
        unique_suggestions = set()
        for issue in issues:
            if issue.improvement_suggestion and issue.improvement_suggestion not in unique_suggestions:
                unique_suggestions.add(issue.improvement_suggestion)
                suggestions.append(issue.improvement_suggestion)
        
        # Add general suggestions based on overall patterns
        if len([i for i in issues if i.category == "color_harmony"]) > 1:
            suggestions.append("Consider using a more limited color palette with better harmony")
        
        if len([i for i in issues if i.category == "style_coherence"]) > 1:
            suggestions.append("Ensure all pieces belong to compatible style categories")
        
        # Sort suggestions by priority (critical issues first)
        critical_suggestions = []
        other_suggestions = []
        
        for issue in issues:
            if issue.criticality in [CriticalityLevel.CRITICAL, CriticalityLevel.HIGH]:
                if issue.improvement_suggestion not in critical_suggestions:
                    critical_suggestions.append(issue.improvement_suggestion)
            else:
                if issue.improvement_suggestion not in other_suggestions:
                    other_suggestions.append(issue.improvement_suggestion)
        
        return critical_suggestions + other_suggestions
    
    def _generate_alternatives(self, ai_output: Dict, issues: List[ValidationIssue]) -> List[Dict]:
        """
        Generate alternative recommendations that address identified issues.
        """
        alternatives = []
        
        # For now, provide basic alternative suggestions
        # In a full implementation, this would use the AI services to generate actual alternatives
        
        if any(issue.category == "color_harmony" for issue in issues):
            alternatives.append({
                "type": "color_adjustment",
                "description": "Use neutral colors (white, gray, beige) to create a safer color palette",
                "confidence": 0.8
            })
        
        if any(issue.category == "style_coherence" for issue in issues):
            alternatives.append({
                "type": "style_adjustment", 
                "description": "Choose pieces from the same formality level and style category",
                "confidence": 0.9
            })
        
        return alternatives
    
    def _generate_learning_feedback(self, ai_output: Dict, result: ValidationResult) -> Dict[str, Any]:
        """
        Generate feedback data that can be used to improve future AI recommendations.
        """
        return {
            "validation_patterns": {
                "color_issues": len([i for i in result.issues if i.category == "color_harmony"]),
                "style_issues": len([i for i in result.issues if i.category == "style_coherence"]),
                "overall_quality": result.overall_score
            },
            "improvement_areas": [issue.category for issue in result.critical_issues],
            "successful_aspects": self._identify_successful_aspects(ai_output, result),
            "timestamp": result.timestamp.isoformat()
        }
    
    def _identify_successful_aspects(self, ai_output: Dict, result: ValidationResult) -> List[str]:
        """
        Identify what aspects of the AI output were successful for reinforcement learning.
        """
        successful_aspects = []
        
        if result.color_harmony_score > 0.8:
            successful_aspects.append("excellent_color_harmony")
        
        if result.style_coherence_score > 0.8:
            successful_aspects.append("excellent_style_coherence")
        
        if result.overall_score > 0.9:
            successful_aspects.append("outstanding_overall_quality")
        
        return successful_aspects
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the RCI system configuration and capabilities.
        """
        return {
            "system_name": "AURA RCI Quality Assurance Engine",
            "version": "1.0.0",
            "active_validators": [v.get_validator_name() for v in self.validators],
            "validation_criteria": {
                "minimum_overall_score": self.criteria.minimum_overall_score,
                "color_harmony_threshold": self.criteria.color_harmony_threshold,
                "style_coherence_threshold": self.criteria.style_coherence_threshold
            },
            "capabilities": [
                "Color harmony validation",
                "Style coherence checking",
                "Improvement suggestion generation",
                "Alternative recommendation creation",
                "Learning feedback generation"
            ]
        }

# Factory function to create a configured RCI engine
def create_rci_engine(custom_criteria: Optional[ValidationCriteria] = None) -> RCIQualityEngine:
    """
    Factory function to create a properly configured RCI Quality Engine.
    
    Args:
        custom_criteria: Optional custom validation criteria
        
    Returns:
        Configured RCI Quality Engine ready for use
    """
    logger.info("Creating new RCI Quality Engine instance")
    return RCIQualityEngine(criteria=custom_criteria)

# Example usage and testing functions
async def validate_fashion_recommendation(recommendation: Dict[str, Any], context: Dict[str, Any]) -> ValidationResult:
    """
    High-level function to validate a fashion recommendation using the RCI system.
    
    Args:
        recommendation: The AI-generated fashion recommendation
        context: Context including user profile, occasion, etc.
        
    Returns:
        Complete validation result
    """
    engine = create_rci_engine()
    return await engine.validate_ai_output(recommendation, context)

if __name__ == "__main__":
    # Example usage for testing
    async def test_rci_system():
        """Test the RCI system with example recommendations."""
        
        # Test case 1: Problematic color combination
        test_recommendation_1 = {
            "items": [
                {"type": "shirt", "color": "red", "name": "Red dress shirt"},
                {"type": "pants", "color": "green", "name": "Green formal pants"}
            ],
            "colors": ["red", "green"],
            "style_tags": ["business", "formal"]
        }
        
        test_context_1 = {
            "service_source": "combination_engine",
            "occasion": "work",
            "user_preferences": {"style": "conservative"}
        }
        
        print("Testing problematic red + green combination...")
        result_1 = await validate_fashion_recommendation(test_recommendation_1, test_context_1)
        print(f"Result: {result_1.status.value}, Score: {result_1.overall_score:.2f}")
        print(f"Issues found: {len(result_1.issues)}")
        print(f"Improvements: {result_1.improvement_suggestions[:2]}")  # Show first 2 suggestions
        print()
        
        # Test case 2: Good combination
        test_recommendation_2 = {
            "items": [
                {"type": "dress", "color": "black", "name": "Black cocktail dress"},
                {"type": "shoes", "color": "red", "name": "Red statement heels"}
            ],
            "colors": ["black", "red"],
            "style_tags": ["elegant", "formal"]
        }
        
        test_context_2 = {
            "service_source": "recommendation_engine",
            "occasion": "dinner",
            "user_preferences": {"style": "bold"}
        }
        
        print("Testing classic black + red combination...")
        result_2 = await validate_fashion_recommendation(test_recommendation_2, test_context_2)
        print(f"Result: {result_2.status.value}, Score: {result_2.overall_score:.2f}")
        print(f"Issues found: {len(result_2.issues)}")
        print()
        
        # Show system summary
        engine = create_rci_engine()
        summary = engine.get_validation_summary()
        print("RCI System Summary:")
        print(f"Active validators: {', '.join(summary['active_validators'])}")
        print(f"Capabilities: {len(summary['capabilities'])} features available")
    
    # Run the test
    asyncio.run(test_rci_system())
