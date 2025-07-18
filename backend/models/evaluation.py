"""
Evaluation models for AI poker coach decisions.
"""

from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from enum import Enum

from ..config.database import Base

class LeakCategory(str, Enum):
    PREFLOP = "preflop"
    POSTFLOP = "postflop"
    TOURNAMENT = "tournament"
    MENTAL = "mental"
    TECHNICAL = "technical"

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Evaluation(Base):
    """Database model for decision evaluations."""
    
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(String, unique=True, index=True)
    scenario_id = Column(String, ForeignKey("scenarios.scenario_id"), nullable=False)
    player_id = Column(String, nullable=False)
    player_action = Column(String, nullable=False)
    player_amount = Column(Integer, nullable=True)
    time_taken = Column(Float, nullable=True)
    correct = Column(Boolean, nullable=False)
    optimal_action = Column(JSON, nullable=False)
    ev_analysis = Column(JSON, nullable=False)
    mistake_analysis = Column(JSON, nullable=True)
    coaching_feedback = Column(JSON, nullable=False)
    performance_impact = Column(JSON, nullable=False)
    key_concepts = Column(JSON, nullable=False)
    difficulty_assessment = Column(JSON, nullable=False)
    follow_up_scenarios = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    scenario = relationship("Scenario", back_populates="evaluations")

class EvaluationRequest(BaseModel):
    """Pydantic model for evaluation requests."""
    
    scenario_id: str
    player_id: str
    player_action: str
    player_amount: Optional[int] = Field(None, ge=0)
    time_taken: Optional[float] = Field(None, ge=0)
    player_context: Optional[Dict[str, Any]] = Field(None)

class EvaluationResponse(BaseModel):
    """Pydantic model for evaluation responses."""
    
    evaluation_id: str
    scenario_id: str
    player_action: str
    correct: bool
    optimal_action: Dict[str, Any]
    ev_analysis: Dict[str, Any]
    mistake_analysis: Optional[Dict[str, Any]]
    coaching_feedback: Dict[str, Any]
    performance_impact: Dict[str, Any]
    key_concepts: List[str]
    difficulty_assessment: Dict[str, Any]
    follow_up_scenarios: Optional[List[str]]
    created_at: datetime

class OptimalActionAnalysis(BaseModel):
    """Model for optimal action analysis."""
    
    action: str
    amount: Optional[int] = Field(None, ge=0)
    reasoning: str
    gto_frequency: Optional[float] = Field(None, ge=0, le=1)
    ev_estimate: Optional[float] = Field(None)
    confidence: Optional[float] = Field(None, ge=0, le=1)

class EVAnalysis(BaseModel):
    """Model for Expected Value analysis."""
    
    player_action_ev: float
    optimal_action_ev: float
    ev_difference: float
    ev_explanation: str
    pot_odds: Optional[float] = Field(None, ge=0, le=1)
    implied_odds: Optional[float] = Field(None)
    fold_equity: Optional[float] = Field(None, ge=0, le=1)
    calculation_method: Optional[str] = Field(None)

class MistakeAnalysis(BaseModel):
    """Model for mistake analysis."""
    
    leak_type: str
    severity: int = Field(..., ge=1, le=10)
    category: LeakCategory
    frequency: str  # rare, occasional, frequent, constant
    description: str
    root_cause: Optional[str] = Field(None)
    pattern_indicator: Optional[bool] = Field(None)
    previous_occurrences: Optional[int] = Field(None, ge=0)

class CoachingFeedback(BaseModel):
    """Model for coaching feedback."""
    
    immediate_feedback: str
    concept_explanation: str
    improvement_tip: str
    practice_suggestion: str
    confidence_building: Optional[str] = Field(None)
    warning_signs: Optional[List[str]] = Field(None)

class PerformanceImpact(BaseModel):
    """Model for performance impact assessment."""
    
    short_term: str
    long_term: str
    tournament_impact: str
    ev_impact: Optional[float] = Field(None)
    frequency_impact: Optional[str] = Field(None)
    skill_development: Optional[str] = Field(None)

class DifficultyAssessment(BaseModel):
    """Model for difficulty assessment."""
    
    scenario_difficulty: int = Field(..., ge=1, le=10)
    decision_difficulty: int = Field(..., ge=1, le=10)
    common_mistake: bool
    skill_level_required: str
    time_pressure_factor: Optional[int] = Field(None, ge=1, le=10)
    information_complexity: Optional[int] = Field(None, ge=1, le=10)

class PlayerDecision(BaseModel):
    """Model for player decision tracking."""
    
    action: str
    amount: Optional[int] = Field(None, ge=0)
    reasoning: Optional[str] = Field(None)
    confidence: Optional[float] = Field(None, ge=0, le=1)
    time_taken: Optional[float] = Field(None, ge=0)
    decision_context: Optional[Dict[str, Any]] = Field(None)

class LeakPattern(BaseModel):
    """Model for leak pattern analysis."""
    
    leak_type: str
    occurrences: int
    severity_trend: List[int]
    context_factors: List[str]
    improvement_rate: Optional[float] = Field(None)
    last_occurrence: Optional[datetime] = Field(None)
    recommended_action: Optional[str] = Field(None)

class ConceptMastery(BaseModel):
    """Model for concept mastery tracking."""
    
    concept: str
    mastery_level: float = Field(..., ge=0, le=1)
    accuracy_rate: float = Field(..., ge=0, le=1)
    improvement_trend: List[float]
    last_tested: Optional[datetime] = Field(None)
    needs_reinforcement: bool = Field(default=False)

class SessionStats(BaseModel):
    """Model for session statistics."""
    
    scenarios_completed: int
    correct_decisions: int
    accuracy_rate: float
    avg_decision_time: float
    concepts_practiced: List[str]
    leaks_identified: List[str]
    improvement_areas: List[str]
    session_duration: float
    ev_gained: Optional[float] = Field(None)

class ProgressTracking(BaseModel):
    """Model for progress tracking."""
    
    player_id: str
    skill_level: str
    overall_accuracy: float
    improvement_rate: float
    sessions_completed: int
    total_scenarios: int
    mastered_concepts: List[str]
    active_leaks: List[str]
    next_milestones: List[str]
    last_session: Optional[datetime] = Field(None)

# Utility functions for evaluation
def calculate_ev_difference(player_ev: float, optimal_ev: float) -> float:
    """Calculate EV difference between player and optimal action."""
    return player_ev - optimal_ev

def determine_mistake_severity(ev_difference: float, pot_size: int) -> int:
    """Determine mistake severity based on EV difference."""
    if ev_difference >= 0:
        return 0  # No mistake
    
    ev_loss_ratio = abs(ev_difference) / pot_size
    
    if ev_loss_ratio < 0.05:
        return 2  # Minor mistake
    elif ev_loss_ratio < 0.15:
        return 4  # Moderate mistake
    elif ev_loss_ratio < 0.30:
        return 6  # Significant mistake
    elif ev_loss_ratio < 0.50:
        return 8  # Major mistake
    else:
        return 10  # Critical mistake

def categorize_leak(action: str, scenario_context: Dict[str, Any]) -> str:
    """Categorize the type of leak based on action and context."""
    street = scenario_context.get("current_street", "preflop")
    
    if street == "preflop":
        if action in ["fold", "call", "raise"]:
            return "preflop.range_selection"
        return "preflop.general"
    
    elif street in ["flop", "turn", "river"]:
        if "bet" in action or "raise" in action:
            return "postflop.aggression"
        elif "fold" in action:
            return "postflop.defense"
        else:
            return "postflop.general"
    
    return "general.decision_making"

def assess_learning_difficulty(scenario_data: Dict[str, Any]) -> int:
    """Assess learning difficulty of scenario."""
    difficulty = 1
    
    # Add complexity factors
    if scenario_data.get("current_street") != "preflop":
        difficulty += 1
    
    if scenario_data.get("tournament_stage") in ["bubble", "final_table"]:
        difficulty += 2
    
    stack_depth = scenario_data.get("hero_stack", 0) // scenario_data.get("blinds", {}).get("big", 100)
    if stack_depth < 15:
        difficulty += 1
    
    if len(scenario_data.get("villain_positions", [])) > 1:
        difficulty += 1
    
    return min(difficulty, 10)

def generate_follow_up_scenarios(
    evaluation: EvaluationResponse,
    player_weaknesses: List[str]
) -> List[str]:
    """Generate follow-up scenario suggestions."""
    scenarios = []
    
    if evaluation.mistake_analysis:
        leak_type = evaluation.mistake_analysis.get("leak_type", "")
        scenarios.append(f"Similar {leak_type} scenarios")
    
    for concept in evaluation.key_concepts:
        if concept in player_weaknesses:
            scenarios.append(f"Reinforcement scenarios for {concept}")
    
    return scenarios[:3]  # Limit to 3 suggestions

class EvaluationEngine:
    """Engine for processing evaluations."""
    
    @staticmethod
    def process_evaluation(
        scenario: Dict[str, Any],
        player_action: str,
        player_context: Optional[Dict[str, Any]] = None
    ) -> EvaluationResponse:
        """Process a complete evaluation."""
        # This would integrate with the AI service
        pass
    
    @staticmethod
    def update_player_context(
        player_id: str,
        evaluation: EvaluationResponse
    ) -> Dict[str, Any]:
        """Update player context based on evaluation."""
        # This would update the player's weakness profile
        pass
    
    @staticmethod
    def generate_coaching_plan(
        player_id: str,
        recent_evaluations: List[EvaluationResponse]
    ) -> Dict[str, Any]:
        """Generate personalized coaching plan."""
        # This would analyze patterns and create coaching recommendations
        pass