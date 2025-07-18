"""
Player context models for tracking weaknesses and progress.
"""

from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
# relationship import removed - not used in this file
from pydantic import BaseModel, Field
from enum import Enum

from ..config.database import Base

class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class PlayerContext(Base):
    """Database model for player context and progress."""
    
    __tablename__ = "player_contexts"
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, unique=True, index=True)
    skill_level = Column(String, nullable=False)
    total_scenarios = Column(Integer, default=0)
    correct_decisions = Column(Integer, default=0)
    total_sessions = Column(Integer, default=0)
    total_session_time = Column(Float, default=0.0)
    
    # Weakness tracking
    weaknesses = Column(JSON, nullable=False)
    strength_areas = Column(JSON, nullable=False)
    focus_areas = Column(JSON, nullable=False)
    
    # Progress metrics
    accuracy_trend = Column(JSON, nullable=False)
    ev_trend = Column(JSON, nullable=False)
    improvement_rate = Column(Float, default=0.0)
    
    # Learning preferences
    preferred_difficulty = Column(String, default="intermediate")
    learning_style = Column(String, default="balanced")
    session_length_preference = Column(Integer, default=30)
    
    # Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_session = Column(DateTime, nullable=True)

class PlayerContextResponse(BaseModel):
    """Pydantic model for player context responses."""
    
    player_id: str
    skill_level: SkillLevel
    total_scenarios: int
    correct_decisions: int
    total_sessions: int
    total_session_time: float
    weaknesses: Dict[str, Any]
    strength_areas: Dict[str, Any]
    focus_areas: List[str]
    accuracy_trend: List[float]
    ev_trend: List[float]
    improvement_rate: float
    preferred_difficulty: str
    learning_style: str
    session_length_preference: int
    created_at: datetime
    updated_at: datetime
    last_session: Optional[datetime]

class WeaknessProfile(BaseModel):
    """Model for player weakness analysis."""
    
    preflop: Dict[str, float] = Field(default_factory=dict)
    postflop: Dict[str, float] = Field(default_factory=dict)
    tournament: Dict[str, float] = Field(default_factory=dict)
    mental: Dict[str, float] = Field(default_factory=dict)
    technical: Dict[str, float] = Field(default_factory=dict)

class StrengthProfile(BaseModel):
    """Model for player strength analysis."""
    
    preflop: Dict[str, float] = Field(default_factory=dict)
    postflop: Dict[str, float] = Field(default_factory=dict)
    tournament: Dict[str, float] = Field(default_factory=dict)
    mental: Dict[str, float] = Field(default_factory=dict)
    technical: Dict[str, float] = Field(default_factory=dict)

class LearningPreferences(BaseModel):
    """Model for learning preferences."""
    
    preferred_difficulty: str = Field(default="intermediate")
    learning_style: str = Field(default="balanced")  # visual, analytical, practical
    session_length_preference: int = Field(default=30, ge=5, le=180)
    focus_areas: List[str] = Field(default_factory=list)
    scenario_preferences: List[str] = Field(default_factory=list)
    feedback_style: str = Field(default="detailed")  # brief, detailed, comprehensive

class PerformanceMetrics(BaseModel):
    """Model for performance metrics."""
    
    overall_accuracy: float = Field(..., ge=0, le=1)
    preflop_accuracy: float = Field(..., ge=0, le=1)
    postflop_accuracy: float = Field(..., ge=0, le=1)
    tournament_accuracy: float = Field(..., ge=0, le=1)
    avg_decision_time: float = Field(..., ge=0)
    improvement_rate: float = Field(..., ge=-1, le=1)
    consistency_score: float = Field(..., ge=0, le=1)
    confidence_level: float = Field(..., ge=0, le=1)

class SessionSummary(BaseModel):
    """Model for session summary."""
    
    session_id: str
    player_id: str
    start_time: datetime
    end_time: datetime
    duration: float
    scenarios_completed: int
    correct_decisions: int
    accuracy_rate: float
    concepts_practiced: List[str]
    leaks_identified: List[str]
    improvements_made: List[str]
    next_focus_areas: List[str]
    session_notes: Optional[str] = Field(None)

class ProgressMilestone(BaseModel):
    """Model for progress milestones."""
    
    milestone_id: str
    player_id: str
    milestone_type: str  # accuracy, consistency, concept_mastery
    description: str
    target_value: float
    current_value: float
    achieved: bool
    achieved_date: Optional[datetime] = Field(None)
    reward: Optional[str] = Field(None)

class ConceptMastery(BaseModel):
    """Model for concept mastery tracking."""
    
    concept_id: str
    concept_name: str
    mastery_level: float = Field(..., ge=0, le=1)
    accuracy_rate: float = Field(..., ge=0, le=1)
    exposure_count: int = Field(..., ge=0)
    last_practiced: Optional[datetime] = Field(None)
    needs_reinforcement: bool = Field(default=False)
    mastery_trend: List[float] = Field(default_factory=list)

class AdaptiveLearning(BaseModel):
    """Model for adaptive learning parameters."""
    
    current_difficulty: float = Field(..., ge=0.1, le=1.0)
    learning_velocity: float = Field(..., ge=0, le=1)
    challenge_preference: float = Field(..., ge=0, le=1)
    error_tolerance: float = Field(..., ge=0, le=1)
    concept_priorities: Dict[str, float] = Field(default_factory=dict)
    next_scenario_type: Optional[str] = Field(None)

# Default weakness categories and subcategories
DEFAULT_WEAKNESS_CATEGORIES = {
    "preflop": {
        "opening_ranges": 0.0,
        "three_bet_frequency": 0.0,
        "blind_defense": 0.0,
        "position_awareness": 0.0,
        "stack_depth_adjustments": 0.0,
        "steal_frequency": 0.0,
        "limping_tendencies": 0.0,
        "isolation_play": 0.0
    },
    "postflop": {
        "cbet_frequency": 0.0,
        "bet_sizing": 0.0,
        "bluff_frequency": 0.0,
        "value_betting": 0.0,
        "pot_control": 0.0,
        "board_reading": 0.0,
        "range_analysis": 0.0,
        "fold_equity": 0.0,
        "draw_play": 0.0,
        "river_decisions": 0.0
    },
    "tournament": {
        "icm_awareness": 0.0,
        "bubble_play": 0.0,
        "final_table_dynamics": 0.0,
        "stack_preservation": 0.0,
        "aggression_timing": 0.0,
        "payout_structure": 0.0,
        "risk_assessment": 0.0,
        "chip_accumulation": 0.0
    },
    "mental": {
        "tilt_control": 0.0,
        "decision_speed": 0.0,
        "confidence_level": 0.0,
        "focus_maintenance": 0.0,
        "pressure_handling": 0.0,
        "learning_consistency": 0.0,
        "self_assessment": 0.0
    },
    "technical": {
        "pot_odds_calculation": 0.0,
        "implied_odds": 0.0,
        "ev_calculations": 0.0,
        "combinatorics": 0.0,
        "probability_estimation": 0.0,
        "stack_management": 0.0,
        "bet_sizing_theory": 0.0
    }
}

# Utility functions for player context management
def initialize_player_context(player_id: str, skill_level: str) -> PlayerContext:
    """Initialize a new player context."""
    return PlayerContext(
        player_id=player_id,
        skill_level=skill_level,
        weaknesses=DEFAULT_WEAKNESS_CATEGORIES.copy(),
        strength_areas={},
        focus_areas=["position_awareness", "basic_math", "tournament_dynamics"],
        accuracy_trend=[],
        ev_trend=[],
        improvement_rate=0.0
    )

def update_weakness_score(
    current_weaknesses: Dict[str, Any],
    leak_type: str,
    severity: int,
    decay_factor: float = 0.95
) -> Dict[str, Any]:
    """Update weakness scores based on new evaluation."""
    
    # Apply decay to all weaknesses
    for category in current_weaknesses:
        for weakness in current_weaknesses[category]:
            current_weaknesses[category][weakness] *= decay_factor
    
    # Update specific weakness
    if '.' in leak_type:
        category, weakness = leak_type.split('.', 1)
        if category in current_weaknesses and weakness in current_weaknesses[category]:
            current_weaknesses[category][weakness] = min(
                100.0,
                current_weaknesses[category][weakness] + severity * 2
            )
    
    return current_weaknesses

def calculate_improvement_rate(accuracy_trend: List[float], window: int = 10) -> float:
    """Calculate improvement rate based on accuracy trend."""
    if len(accuracy_trend) < 2:
        return 0.0
    
    recent_trend = accuracy_trend[-window:] if len(accuracy_trend) >= window else accuracy_trend
    
    if len(recent_trend) < 2:
        return 0.0
    
    # Simple linear regression slope
    n = len(recent_trend)
    x_mean = (n - 1) / 2
    y_mean = sum(recent_trend) / n
    
    numerator = sum((i - x_mean) * (y - y_mean) for i, y in enumerate(recent_trend))
    denominator = sum((i - x_mean) ** 2 for i in range(n))
    
    return numerator / denominator if denominator != 0 else 0.0

def identify_top_weaknesses(weaknesses: Dict[str, Any], top_n: int = 5) -> List[str]:
    """Identify top weaknesses across all categories."""
    all_weaknesses = []
    
    for category, weakness_dict in weaknesses.items():
        for weakness, score in weakness_dict.items():
            all_weaknesses.append((f"{category}.{weakness}", score))
    
    # Sort by score (descending) and return top N
    all_weaknesses.sort(key=lambda x: x[1], reverse=True)
    return [weakness for weakness, score in all_weaknesses[:top_n]]

def recommend_focus_areas(
    weaknesses: Dict[str, Any],
    skill_level: str,
    session_count: int
) -> List[str]:
    """Recommend focus areas based on player profile."""
    
    focus_areas = []
    
    # Skill level based recommendations
    if skill_level == "beginner":
        focus_areas.extend([
            "preflop.opening_ranges",
            "preflop.position_awareness",
            "technical.pot_odds_calculation"
        ])
    elif skill_level == "intermediate":
        focus_areas.extend([
            "postflop.bet_sizing",
            "tournament.icm_awareness",
            "postflop.range_analysis"
        ])
    else:  # advanced
        focus_areas.extend([
            "tournament.final_table_dynamics",
            "postflop.fold_equity",
            "mental.pressure_handling"
        ])
    
    # Add top weaknesses
    top_weaknesses = identify_top_weaknesses(weaknesses, 3)
    focus_areas.extend(top_weaknesses)
    
    # Remove duplicates and limit to 5
    return list(set(focus_areas))[:5]

def calculate_skill_progression(
    accuracy_trend: List[float],
    concept_mastery: Dict[str, float],
    session_count: int
) -> Dict[str, Any]:
    """Calculate overall skill progression."""
    
    if not accuracy_trend:
        return {
            "current_skill": 0.0,
            "skill_velocity": 0.0,
            "mastery_level": 0.0,
            "progression_stage": "beginner"
        }
    
    current_accuracy = accuracy_trend[-1] if accuracy_trend else 0.0
    improvement_rate = calculate_improvement_rate(accuracy_trend)
    avg_mastery = sum(concept_mastery.values()) / len(concept_mastery) if concept_mastery else 0.0
    
    # Calculate composite skill score
    skill_score = (current_accuracy * 0.5) + (avg_mastery * 0.3) + (min(session_count / 100, 1.0) * 0.2)
    
    # Determine progression stage
    if skill_score < 0.4:
        stage = "beginner"
    elif skill_score < 0.7:
        stage = "intermediate"
    elif skill_score < 0.9:
        stage = "advanced"
    else:
        stage = "expert"
    
    return {
        "current_skill": skill_score,
        "skill_velocity": improvement_rate,
        "mastery_level": avg_mastery,
        "progression_stage": stage
    }

class PlayerContextManager:
    """Manager class for player context operations."""
    
    @staticmethod
    def create_new_player(player_id: str, skill_level: str) -> PlayerContext:
        """Create a new player context."""
        return initialize_player_context(player_id, skill_level)
    
    @staticmethod
    def update_from_evaluation(
        context: PlayerContext,
        evaluation_data: Dict[str, Any]
    ) -> PlayerContext:
        """Update player context from evaluation."""
        # Update weaknesses if mistake was made
        if not evaluation_data.get('correct', True):
            mistake_analysis = evaluation_data.get('mistake_analysis', {})
            if mistake_analysis:
                # Get current weaknesses as dict, ensuring it's not None
                current_weaknesses = context.weaknesses or DEFAULT_WEAKNESS_CATEGORIES.copy()
                # Update weaknesses and set back to the model
                context.weaknesses = update_weakness_score(
                    current_weaknesses,
                    mistake_analysis.get('leak_type', ''),
                    mistake_analysis.get('severity', 0)
                )
        
        # Update accuracy trend
        new_accuracy = 1.0 if evaluation_data.get('correct', False) else 0.0
        
        # Ensure accuracy_trend is a list
        if context.accuracy_trend is None:
            context.accuracy_trend = []
        
        context.accuracy_trend.append(new_accuracy)
        
        # Limit trend history
        if len(context.accuracy_trend) > 100:
            context.accuracy_trend = context.accuracy_trend[-100:]
        
        # Update focus areas
        context.focus_areas = recommend_focus_areas(
            context.weaknesses or {},
            context.skill_level or "intermediate",
            context.total_sessions or 0
        )
        
        return context
    
    @staticmethod
    def get_next_scenario_recommendations(
        context: PlayerContext
    ) -> Dict[str, Any]:
        """Get recommendations for next scenario."""
        
        top_weaknesses = identify_top_weaknesses(context.weaknesses or {}, 3)
        
        return {
            "focus_weakness": top_weaknesses[0] if top_weaknesses else None,
            "difficulty_level": context.preferred_difficulty,
            "scenario_types": context.focus_areas,
            "session_goals": top_weaknesses[:2]
        }