"""
MTT Scenario models for AI poker coach.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from enum import Enum

Base = declarative_base()

class TournamentStage(str, Enum):
    EARLY = "early"
    MIDDLE = "middle"
    BUBBLE = "bubble"
    ITM = "itm"
    FINAL_TABLE = "final_table"

class Position(str, Enum):
    UTG = "UTG"
    UTG_1 = "UTG+1"
    UTG_2 = "UTG+2"
    MP = "MP"
    CO = "CO"
    BTN = "BTN"
    SB = "SB"
    BB = "BB"

class Street(str, Enum):
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"

class Action(str, Enum):
    FOLD = "fold"
    CALL = "call"
    RAISE = "raise"
    CHECK = "check"
    BET = "bet"
    ALL_IN = "all_in"

class Scenario(Base):
    """Database model for MTT scenarios."""
    
    __tablename__ = "scenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(String, unique=True, index=True)
    tournament_stage = Column(String, nullable=False)
    hero_position = Column(String, nullable=False)
    hero_stack = Column(Integer, nullable=False)
    hero_cards = Column(JSON, nullable=False)
    villain_positions = Column(JSON, nullable=False)
    blinds = Column(JSON, nullable=False)
    ante = Column(Integer, default=0)
    players_remaining = Column(Integer, nullable=False)
    total_players = Column(Integer, nullable=False)
    prize_pool = Column(Integer, nullable=False)
    current_payouts = Column(JSON, nullable=True)
    action_history = Column(JSON, nullable=False)
    current_street = Column(String, nullable=False)
    board = Column(JSON, nullable=False)
    pot_size = Column(Integer, nullable=False)
    to_call = Column(Integer, nullable=False)
    min_raise = Column(Integer, nullable=False)
    max_raise = Column(Integer, nullable=False)
    valid_actions = Column(JSON, nullable=False)
    scenario_description = Column(Text, nullable=False)
    key_concepts = Column(JSON, nullable=False)
    optimal_action = Column(JSON, nullable=False)
    alternative_actions = Column(JSON, nullable=False)
    difficulty_factors = Column(JSON, nullable=False)
    learning_objectives = Column(JSON, nullable=False)
    difficulty_level = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String, nullable=True)
    
    # Relationships
    evaluations = relationship("Evaluation", back_populates="scenario")

class ScenarioRequest(BaseModel):
    """Pydantic model for scenario generation requests."""
    
    tournament_stage: TournamentStage = Field(..., description="Stage of the tournament")
    stack_depth: int = Field(..., ge=1, le=200, description="Stack depth in big blinds")
    game_format: str = Field(default="MTT", description="Game format")
    difficulty: str = Field(default="intermediate", description="Difficulty level")
    player_id: str = Field(..., description="Player identifier")
    focus_area: Optional[str] = Field(None, description="Specific weakness to target")
    scenario_type: Optional[str] = Field(None, description="Type of scenario")

class ScenarioResponse(BaseModel):
    """Pydantic model for scenario responses."""
    
    scenario_id: str
    tournament_stage: str
    hero_position: str
    hero_stack: int
    hero_cards: List[str]
    villain_positions: List[Dict[str, Any]]
    blinds: Dict[str, int]
    ante: int
    players_remaining: int
    total_players: int
    prize_pool: int
    current_payouts: Optional[Dict[str, int]]
    action_history: List[str]
    current_street: str
    board: List[str]
    pot_size: int
    to_call: int
    min_raise: int
    max_raise: int
    valid_actions: List[str]
    scenario_description: str
    key_concepts: List[str]
    optimal_action: Dict[str, Any]
    alternative_actions: List[Dict[str, Any]]
    difficulty_factors: List[str]
    learning_objectives: List[str]
    difficulty_level: str
    created_at: datetime

class VillainProfile(BaseModel):
    """Model for opponent characteristics."""
    
    position: Position
    stack: int
    player_type: str = Field(default="unknown")
    vpip: Optional[float] = Field(None, ge=0, le=100)
    pfr: Optional[float] = Field(None, ge=0, le=100)
    aggression: Optional[float] = Field(None, ge=0, le=10)
    tendency: Optional[str] = Field(None)
    notes: Optional[str] = Field(None)

class OptimalAction(BaseModel):
    """Model for optimal action analysis."""
    
    action: Action
    amount: Optional[int] = Field(None, ge=0)
    reasoning: str
    gto_frequency: Optional[float] = Field(None, ge=0, le=1)
    ev_estimate: Optional[float] = Field(None)
    risk_assessment: Optional[str] = Field(None)

class AlternativeAction(BaseModel):
    """Model for alternative action analysis."""
    
    action: Action
    amount: Optional[int] = Field(None, ge=0)
    ev_difference: float
    reasoning: str
    frequency: Optional[float] = Field(None, ge=0, le=1)

class TournamentContext(BaseModel):
    """Model for tournament-specific context."""
    
    stage: TournamentStage
    players_remaining: int
    total_players: int
    prize_pool: int
    current_payouts: Optional[Dict[str, int]]
    average_stack: Optional[int]
    time_level: Optional[str]
    next_payout_jump: Optional[int]
    bubble_factor: Optional[float]
    icm_pressure: Optional[str]  # low, medium, high

class HandRange(BaseModel):
    """Model for hand range analysis."""
    
    range_description: str
    hand_categories: List[str]
    percentage: float
    example_hands: List[str]
    adjustments: Optional[Dict[str, str]]

class StackDepthContext(BaseModel):
    """Model for stack depth considerations."""
    
    effective_stack: int
    spr: Optional[float]  # Stack to Pot Ratio
    play_style: str  # deep, medium, short, micro
    key_factors: List[str]
    adjustments: List[str]

class ICMContext(BaseModel):
    """Model for ICM considerations."""
    
    icm_factor: float
    survival_premium: float
    risk_premium: float
    bubble_distance: int
    payout_structure: Dict[str, int]
    recommendations: List[str]

# Utility functions for scenario generation
def calculate_stack_depth(stack: int, big_blind: int) -> int:
    """Calculate stack depth in big blinds."""
    return stack // big_blind

def determine_play_style(stack_depth: int) -> str:
    """Determine play style based on stack depth."""
    if stack_depth >= 50:
        return "deep"
    elif stack_depth >= 20:
        return "medium"
    elif stack_depth >= 10:
        return "short"
    else:
        return "micro"

def calculate_pot_odds(to_call: int, pot_size: int) -> float:
    """Calculate pot odds."""
    return to_call / (pot_size + to_call)

def calculate_spr(effective_stack: int, pot_size: int) -> float:
    """Calculate Stack to Pot Ratio."""
    return effective_stack / pot_size if pot_size > 0 else float('inf')

def is_bubble_situation(players_remaining: int, paid_spots: int) -> bool:
    """Determine if current situation is bubble."""
    return players_remaining <= paid_spots * 1.2  # Within 20% of bubble

def calculate_icm_factor(stack: int, average_stack: int, players_remaining: int) -> float:
    """Calculate ICM factor (simplified)."""
    if stack == 0:
        return 0.0
    
    stack_ratio = stack / average_stack
    position_factor = 1.0 / players_remaining
    
    # Simplified ICM calculation
    if stack_ratio > 2.0:
        return min(1.0, 0.8 + (stack_ratio - 2.0) * 0.1)
    elif stack_ratio > 1.0:
        return 0.6 + (stack_ratio - 1.0) * 0.2
    else:
        return max(0.1, 0.6 * stack_ratio)

class ScenarioGenerator:
    """Utility class for scenario generation helpers."""
    
    @staticmethod
    def generate_hand_combo() -> List[str]:
        """Generate a random hand combination."""
        # This would integrate with poker hand generation logic
        pass
    
    @staticmethod
    def generate_board(street: Street) -> List[str]:
        """Generate board cards based on street."""
        # This would integrate with board generation logic
        pass
    
    @staticmethod
    def calculate_pot_size(action_history: List[str], blinds: Dict[str, int]) -> int:
        """Calculate pot size from action history."""
        # This would parse action history and calculate pot
        pass
    
    @staticmethod
    def determine_valid_actions(
        stack: int, 
        to_call: int, 
        pot_size: int, 
        street: Street
    ) -> List[str]:
        """Determine valid actions for current situation."""
        actions = []
        
        if to_call > 0:
            actions.append("fold")
            if stack >= to_call:
                actions.append("call")
        else:
            actions.append("check")
        
        if stack > to_call:
            actions.append("raise" if to_call > 0 else "bet")
        
        if stack <= to_call:
            actions.append("all_in")
        
        return actions