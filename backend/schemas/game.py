"""
Game schemas for MTT poker coaching.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class ScenarioGenerationRequest(BaseModel):
    """Schema for scenario generation requests."""
    
    game_type: str = Field(default="MTT", description="Type of game")
    tournament_stage: str = Field(..., description="Stage of tournament")
    stack_depth: int = Field(..., ge=1, le=200, description="Stack depth in BB")
    player_id: str = Field(..., description="Player identifier")
    difficulty: str = Field(default="intermediate", description="Difficulty level")
    focus_area: Optional[str] = Field(None, description="Specific area to focus on")

class ScenarioGenerationResponse(BaseModel):
    """Schema for scenario generation responses."""
    
    id: str
    hero_position: str
    hero_cards: List[str]
    hero_stack: int
    villain_positions: List[Dict[str, Any]]
    blinds: Dict[str, int]
    ante: int
    players_remaining: int
    board: List[str]
    pot_size: int
    to_call: int
    valid_actions: List[str]
    scenario_description: str
    tournament_stage: str
    action_required: bool = True

class DecisionEvaluationRequest(BaseModel):
    """Schema for decision evaluation requests."""
    
    scenario_id: str = Field(..., description="Scenario identifier")
    action: str = Field(..., description="Player action")
    player_id: str = Field(..., description="Player identifier")
    amount: Optional[int] = Field(None, ge=0, description="Action amount")
    time_taken: Optional[float] = Field(None, ge=0, description="Time taken in seconds")

class DecisionEvaluationResponse(BaseModel):
    """Schema for decision evaluation responses."""
    
    correct: bool
    optimal_action: str
    optimal_amount: Optional[int] = None
    ev_difference: float
    leak_identified: Optional[str] = None
    explanation: str
    coaching_tip: str
    improvement_areas: List[str]
    severity: int = Field(ge=0, le=10)

class PlayerStatsResponse(BaseModel):
    """Schema for player statistics."""
    
    total_scenarios: int
    correct_decisions: int
    accuracy_rate: float = Field(ge=0, le=1)
    avg_decision_time: float = Field(ge=0)

class SessionStartRequest(BaseModel):
    """Schema for starting a coaching session."""
    
    player_id: str
    session_goals: List[str] = Field(default_factory=list)

class SessionStartResponse(BaseModel):
    """Schema for session start response."""
    
    session_id: str
    player_id: str
    coaching_plan: Dict[str, Any]
    recommendations: Dict[str, Any]
    started_at: datetime

class SessionSummaryRequest(BaseModel):
    """Schema for session summary request."""
    
    player_id: str
    session_start: datetime

class SessionSummaryResponse(BaseModel):
    """Schema for session summary response."""
    
    session_duration: float
    scenarios_completed: int
    correct_decisions: int
    accuracy_rate: float
    concepts_practiced: List[str]
    leaks_identified: List[str]
    session_start: datetime
    session_end: datetime

class ProgressReportResponse(BaseModel):
    """Schema for progress report."""
    
    overall_skill: float = Field(ge=0, le=100)
    improvement_rate: float
    biggest_leaks: List[Dict[str, Any]]
    recommended_focus: List[str]
    stats: Dict[str, Any]

class CoachingPlanResponse(BaseModel):
    """Schema for coaching plan."""
    
    current_focus: str
    exercises: List[Dict[str, Any]]
    concepts_to_study: List[str]
    estimated_sessions: int = Field(ge=1)

class WeaknessAnalysisResponse(BaseModel):
    """Schema for weakness analysis."""
    
    analysis: Dict[str, Any]
    recommendations: List[str]
    priority_areas: List[str]

class PlayerContextResponse(BaseModel):
    """Schema for player context."""
    
    player_id: str
    skill_level: str
    total_scenarios: int
    total_sessions: int
    accuracy_trend: List[float]
    weaknesses: Dict[str, Any]
    focus_areas: List[str]
    preferred_difficulty: str
    improvement_rate: float
    last_session: Optional[datetime] = None

class ScenarioRecommendationResponse(BaseModel):
    """Schema for scenario recommendations."""
    
    focus_weakness: Optional[str] = None
    difficulty_level: str
    scenario_types: List[str]
    session_goals: List[str]

class AdaptiveDifficultyResponse(BaseModel):
    """Schema for adaptive difficulty."""
    
    recommended_difficulty: str
    reasoning: str
    recent_accuracy: float
    total_evaluations: int

class DetailedFeedbackResponse(BaseModel):
    """Schema for detailed feedback."""
    
    evaluation_id: str
    immediate_feedback: str
    concept_explanation: str
    improvement_tip: str
    practice_suggestion: str
    performance_impact: Dict[str, Any]
    key_concepts: List[str]
    difficulty_assessment: Dict[str, Any]
    follow_up_scenarios: Optional[List[str]] = None

class GlobalStatsResponse(BaseModel):
    """Schema for global statistics."""
    
    total_evaluations: int
    total_players: int
    recent_evaluations: int
    avg_accuracy: float
    popular_concepts: List[str]

class HealthCheckResponse(BaseModel):
    """Schema for health check."""
    
    status: str
    service: str
    timestamp: datetime
    version: str

# Tournament-specific schemas
class TournamentContextSchema(BaseModel):
    """Schema for tournament context."""
    
    stage: str
    players_remaining: int
    total_players: int
    prize_pool: int
    current_payouts: Optional[Dict[str, int]] = None
    bubble_factor: Optional[float] = None

class ICMContextSchema(BaseModel):
    """Schema for ICM context."""
    
    icm_factor: float
    survival_premium: float
    risk_premium: float
    bubble_distance: int
    payout_structure: Dict[str, int]

class HandRangeSchema(BaseModel):
    """Schema for hand range."""
    
    range_description: str
    hand_categories: List[str]
    percentage: float = Field(ge=0, le=100)
    example_hands: List[str]

class VillainProfileSchema(BaseModel):
    """Schema for villain profile."""
    
    position: str
    stack: int
    player_type: str = "unknown"
    vpip: Optional[float] = Field(None, ge=0, le=100)
    pfr: Optional[float] = Field(None, ge=0, le=100)
    aggression: Optional[float] = Field(None, ge=0, le=10)
    notes: Optional[str] = None

# Error schemas
class ErrorResponse(BaseModel):
    """Schema for error responses."""
    
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ValidationErrorResponse(BaseModel):
    """Schema for validation errors."""
    
    error: str = "Validation Error"
    details: List[Dict[str, Any]]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# API Response wrappers
class APIResponse(BaseModel):
    """Generic API response wrapper."""
    
    success: bool = True
    data: Any
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PaginatedResponse(BaseModel):
    """Schema for paginated responses."""
    
    items: List[Any]
    total: int
    page: int = Field(ge=1)
    per_page: int = Field(ge=1, le=100)
    pages: int = Field(ge=1)
    has_next: bool
    has_prev: bool