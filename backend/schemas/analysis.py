"""
Analysis schemas for AI poker coaching.
"""

from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class LeakAnalysisSchema(BaseModel):
    """Schema for leak analysis."""
    
    leak_type: str
    severity: int = Field(ge=1, le=10)
    frequency: str  # rare, occasional, frequent, constant
    description: str
    category: str
    examples: List[str] = Field(default_factory=list)
    improvement_suggestions: List[str] = Field(default_factory=list)

class ConceptMasterySchema(BaseModel):
    """Schema for concept mastery tracking."""
    
    concept_name: str
    mastery_level: float = Field(ge=0, le=1)
    accuracy_rate: float = Field(ge=0, le=1)
    exposure_count: int = Field(ge=0)
    last_practiced: Optional[datetime] = None
    needs_reinforcement: bool = False
    trend: List[float] = Field(default_factory=list)

class PerformanceMetricsSchema(BaseModel):
    """Schema for performance metrics."""
    
    overall_accuracy: float = Field(ge=0, le=1)
    preflop_accuracy: float = Field(ge=0, le=1)
    postflop_accuracy: float = Field(ge=0, le=1)
    tournament_accuracy: float = Field(ge=0, le=1)
    avg_decision_time: float = Field(ge=0)
    improvement_rate: float = Field(ge=-1, le=1)
    consistency_score: float = Field(ge=0, le=1)

class WeaknessProfileSchema(BaseModel):
    """Schema for weakness profile."""
    
    preflop: Dict[str, float] = Field(default_factory=dict)
    postflop: Dict[str, float] = Field(default_factory=dict)
    tournament: Dict[str, float] = Field(default_factory=dict)
    mental: Dict[str, float] = Field(default_factory=dict)
    technical: Dict[str, float] = Field(default_factory=dict)

class StrengthProfileSchema(BaseModel):
    """Schema for strength profile."""
    
    preflop: Dict[str, float] = Field(default_factory=dict)
    postflop: Dict[str, float] = Field(default_factory=dict)
    tournament: Dict[str, float] = Field(default_factory=dict)
    mental: Dict[str, float] = Field(default_factory=dict)
    technical: Dict[str, float] = Field(default_factory=dict)

class LearningPathSchema(BaseModel):
    """Schema for learning path recommendations."""
    
    current_level: str
    next_milestone: str
    recommended_concepts: List[str]
    practice_areas: List[str]
    estimated_time: int = Field(ge=1)  # in hours
    difficulty_progression: List[str]

class ProgressMilestoneSchema(BaseModel):
    """Schema for progress milestones."""
    
    milestone_id: str
    milestone_type: str
    description: str
    target_value: float
    current_value: float
    achieved: bool
    achieved_date: Optional[datetime] = None
    reward: Optional[str] = None

class SkillAssessmentSchema(BaseModel):
    """Schema for skill assessment."""
    
    overall_skill: float = Field(ge=0, le=100)
    skill_breakdown: Dict[str, float]
    skill_level: str
    confidence_intervals: Dict[str, List[float]]
    assessment_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CompetencyMatrixSchema(BaseModel):
    """Schema for competency matrix."""
    
    beginner_skills: List[str]
    intermediate_skills: List[str]
    advanced_skills: List[str]
    expert_skills: List[str]
    current_competencies: List[str]
    next_targets: List[str]

class LearningAnalyticsSchema(BaseModel):
    """Schema for learning analytics."""
    
    total_study_time: float
    active_learning_time: float
    concept_retention_rate: float
    skill_acquisition_rate: float
    plateau_indicators: List[str]
    breakthrough_moments: List[Dict[str, Any]]

class PersonalizationSchema(BaseModel):
    """Schema for personalization settings."""
    
    learning_style: str  # visual, auditory, kinesthetic, reading
    preferred_pace: str  # slow, medium, fast
    challenge_preference: str  # low, medium, high
    feedback_style: str  # brief, detailed, comprehensive
    motivation_factors: List[str]

class AdaptiveLearningSchema(BaseModel):
    """Schema for adaptive learning parameters."""
    
    current_difficulty: float = Field(ge=0.1, le=1.0)
    learning_velocity: float = Field(ge=0, le=1)
    attention_span: int = Field(ge=5, le=120)  # minutes
    optimal_session_length: int = Field(ge=10, le=180)  # minutes
    break_frequency: int = Field(ge=1, le=10)  # per session

class PatternRecognitionSchema(BaseModel):
    """Schema for pattern recognition in player behavior."""
    
    decision_patterns: Dict[str, List[str]]
    error_patterns: Dict[str, int]
    improvement_patterns: Dict[str, float]
    time_patterns: Dict[str, float]
    consistency_patterns: Dict[str, float]

class PredictiveAnalysisSchema(BaseModel):
    """Schema for predictive analysis."""
    
    predicted_improvement: float
    confidence_interval: List[float]
    time_to_next_level: int  # in hours
    bottleneck_factors: List[str]
    success_probability: float = Field(ge=0, le=1)

class BenchmarkingSchema(BaseModel):
    """Schema for benchmarking against other players."""
    
    percentile_rank: int = Field(ge=1, le=100)
    peer_comparison: Dict[str, float]
    relative_strengths: List[str]
    relative_weaknesses: List[str]
    improvement_potential: float

class LearningEfficiencySchema(BaseModel):
    """Schema for learning efficiency metrics."""
    
    concepts_per_hour: float
    accuracy_improvement_rate: float
    time_to_mastery: Dict[str, int]
    retention_rate: float = Field(ge=0, le=1)
    transfer_learning_score: float = Field(ge=0, le=1)

class MotivationAnalysisSchema(BaseModel):
    """Schema for motivation analysis."""
    
    engagement_level: float = Field(ge=0, le=1)
    motivation_factors: List[str]
    burnout_indicators: List[str]
    satisfaction_score: float = Field(ge=0, le=10)
    goal_alignment: float = Field(ge=0, le=1)

class StudyPlanSchema(BaseModel):
    """Schema for study plan generation."""
    
    plan_duration: int  # in days
    daily_goals: List[str]
    weekly_milestones: List[str]
    concept_schedule: Dict[str, List[str]]
    practice_schedule: Dict[str, int]
    assessment_schedule: List[datetime]

class RecommendationEngineSchema(BaseModel):
    """Schema for recommendation engine output."""
    
    next_concepts: List[str]
    practice_scenarios: List[str]
    difficulty_adjustment: str
    session_structure: Dict[str, Any]
    learning_resources: List[str]

class AnalysisReportSchema(BaseModel):
    """Schema for comprehensive analysis report."""
    
    player_id: str
    report_date: datetime
    analysis_period: Dict[str, datetime]
    executive_summary: str
    detailed_findings: Dict[str, Any]
    recommendations: List[str]
    action_items: List[str]
    next_review_date: datetime