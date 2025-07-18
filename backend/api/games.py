"""
Game API endpoints - MTT scenario and evaluation endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from ..models.scenario import ScenarioRequest, ScenarioResponse, TournamentStage
from ..models.evaluation import EvaluationRequest, EvaluationResponse
from ..services.coaching_service import coaching_service
from ..config.database import get_db

router = APIRouter(prefix="/games", tags=["games"])

@router.post("/scenario/generate", response_model=ScenarioResponse)
async def generate_scenario(
    request: ScenarioRequest,
    db: Session = Depends(get_db)
):
    """Generate a new MTT scenario."""
    
    try:
        scenario = await coaching_service.get_next_scenario(
            player_id=request.player_id,
            preferences={
                "tournament_stage": request.tournament_stage,
                "stack_depth": request.stack_depth,
                "difficulty": request.difficulty,
                "focus_area": request.focus_area,
                "game_format": request.game_format,
                "scenario_type": request.scenario_type or 'general'
            },
            db=db
        )
        
        return scenario
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/scenario/evaluate", response_model=EvaluationResponse)
async def evaluate_decision(
    request: EvaluationRequest,
    db: Session = Depends(get_db)
):
    """Evaluate a player's decision."""
    
    try:
        evaluation = await coaching_service.submit_decision(
            scenario_id=request.scenario_id,
            player_id=request.player_id,
            player_action=request.player_action,
            player_amount=request.player_amount,
            time_taken=request.time_taken,
            db=db
        )
        
        return evaluation
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scenario/{scenario_id}")
async def get_scenario(
    scenario_id: str,
    db: Session = Depends(get_db)
):
    """Get a single scenario by ID."""
    
    try:
        from ..models.scenario import Scenario
        
        scenario = db.query(Scenario).filter(Scenario.scenario_id == scenario_id).first()
        
        if not scenario:
            raise HTTPException(status_code=404, detail="Scenario not found")
            
        return scenario
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/evaluation/{evaluation_id}")
async def get_evaluation(
    evaluation_id: str,
    db: Session = Depends(get_db)
):
    """Get a single evaluation by ID."""
    
    try:
        from ..models.evaluation import Evaluation
        
        evaluation = db.query(Evaluation).filter(Evaluation.evaluation_id == evaluation_id).first()
        
        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")
            
        return evaluation
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/player/{player_id}/scenarios")
async def get_player_scenarios(
    player_id: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get scenarios encountered by a player."""
    
    try:
        from ..models.scenario import Scenario
        from ..models.evaluation import Evaluation
        
        # Get all evaluation for player
        evaluations = db.query(Evaluation).filter(Evaluation.player_id == player_id).all()
        scenario_ids = [eval.scenario_id for eval in evaluations]
        
        # Get scenarios
        scenarios = db.query(Scenario).filter(Scenario.scenario_id.in_(scenario_ids)).limit(limit).offset(offset).all()
        
        return scenarios
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/player/{player_id}/evaluations")
async def get_player_evaluations(
    player_id: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get evaluations for a player."""
    
    try:
        from ..models.evaluation import Evaluation
        
        evaluations = db.query(Evaluation).filter(Evaluation.player_id == player_id).limit(limit).offset(offset).all()
        
        return evaluations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/player/{player_id}/stats")
async def get_player_stats(
    player_id: str,
    db: Session = Depends(get_db)
):
    """Get player statistics."""
    
    try:
        from ..models.evaluation import Evaluation
        
        evaluations = db.query(Evaluation).filter(Evaluation.player_id == player_id).all()
        total_scenarios = len(evaluations)
        correct_decisions = sum(1 for eval in evaluations if eval.correct)
        
        return {
            "total_scenarios": total_scenarios,
            "correct_decisions": correct_decisions,
            "accuracy": correct_decisions / total_scenarios if total_scenarios > 0 else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/start")
async def start_session(
    player_id: str,
    session_goals: Optional[List[str]] = None,
    db: Session = Depends(get_db)
):
    """Start a new coaching session."""

    if session_goals is None:
        session_goals = []
    try:
        session = await coaching_service.start_coaching_session(
            player_id=player_id,
            session_goals=session_goals,
            db=db
        )
        
        return session
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/session/summary")
async def get_session_summary(
    player_id: str,
    session_start: datetime,
    db: Session = Depends(get_db)
):
    """Get session summary."""
    
    try:
        summary = await coaching_service.get_session_summary(
            player_id=player_id,
            session_start=session_start,
            db=db
        )
        
        return summary
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/difficulty/adaptive/{player_id}")
async def get_adaptive_difficulty(
    player_id: str,
    db: Session = Depends(get_db)
):
    """Get adaptive difficulty recommendation."""
    
    try:
        difficulty = await coaching_service.get_adaptive_difficulty(
            player_id=player_id,
            db=db
        )
        
        return difficulty
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Legacy endpoints for backward compatibility
@router.post("/generate-scenario")
async def generate_scenario_legacy(
    tournament_stage: str = "middle",
    stack_depth: int = 30,
    difficulty: str = "intermediate",
    player_id: str = "default",
    focus_area: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Legacy endpoint for scenario generation."""
    
    # Convert string to enum
    stage_enum = TournamentStage(tournament_stage) if tournament_stage in [e.value for e in TournamentStage] else TournamentStage.MIDDLE
    
    request = ScenarioRequest(
        tournament_stage=stage_enum,
        stack_depth=stack_depth,
        difficulty=difficulty,
        player_id=player_id,
        focus_area=focus_area,
        scenario_type="general"
    )
    
    return await generate_scenario(request, db)

@router.post("/evaluate-decision")
async def evaluate_decision_legacy(
    scenario_id: str,
    player_id: str,
    player_action: str,
    player_amount: Optional[int] = None,
    time_taken: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Legacy endpoint for decision evaluation."""
    
    player_context = await coaching_service._get_player_context(player_id, db)
    request = EvaluationRequest(
        scenario_id=scenario_id,
        player_id=player_id,
        player_action=player_action,
        player_amount=player_amount,
        time_taken=time_taken,
        player_context=player_context.to_dict() if player_context else None
    )
    
    try:
        evaluation = await coaching_service.submit_decision(
            scenario_id=request.scenario_id,
            player_id=request.player_id,
            player_action=request.player_action,
            player_amount=request.player_amount,
            time_taken=request.time_taken,
            db=db
        )
        
        return evaluation
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))