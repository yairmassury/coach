"""
AI Coach API endpoints - Dedicated AI coaching routes.
"""

from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..config.database import get_db
from ..models.evaluation import EvaluationRequest
from ..models.scenario import ScenarioRequest, TournamentStage
from ..services.ai_coach_service import ai_coach_service
from ..services.coaching_service import coaching_service
from ..services.ai_providers.manager import ai_provider_manager

router = APIRouter(prefix="/ai", tags=["ai-coach"])

@router.post("/scenario")
async def ai_generate_scenario(
    game_type: str = "MTT",
    tournament_stage: TournamentStage = TournamentStage.MIDDLE,
    stack_depth: int = 30,
    player_id: str = "default",
    difficulty: str = "intermediate",
    focus_area: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Generate MTT scenario using AI coach."""
    
    try:
        request = ScenarioRequest(
            tournament_stage=tournament_stage,
            stack_depth=stack_depth,
            difficulty=difficulty,
            player_id=player_id,
            focus_area=focus_area,
            game_format=game_type
        )
        
        scenario = await ai_coach_service.generate_scenario(request, db)
        
        return {
            "id": scenario.scenario_id,
            "hero_position": scenario.hero_position,
            "hero_cards": scenario.hero_cards,
            "board": scenario.board,
            "pot_size": scenario.pot_size,
            "to_call": scenario.to_call,
            "valid_actions": scenario.valid_actions,
            "scenario_description": scenario.scenario_description,
            "blinds": scenario.blinds,
            "ante": scenario.ante,
            "hero_stack": scenario.hero_stack,
            "villain_positions": scenario.villain_positions,
            "tournament_stage": scenario.tournament_stage,
            "players_remaining": scenario.players_remaining,
            "action_required": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate")
async def ai_evaluate_decision(
    scenario_id: str,
    action: str,
    player_id: str,
    amount: Optional[int] = None,
    time_taken: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Evaluate player decision using AI coach."""
    
    try:
        player_context = await ai_coach_service._get_player_context(player_id, db)
        request = EvaluationRequest(
            scenario_id=scenario_id,
            player_id=player_id,
            player_action=action,
            player_amount=amount,
            time_taken=time_taken,
            player_context=player_context.to_dict() if player_context else None
        )
        
        evaluation = await ai_coach_service.evaluate_decision(request, db)
        
        return {
            "correct": evaluation.correct,
            "optimal_action": (evaluation.optimal_action or {}).get("action", "unknown"),
            "optimal_amount": (evaluation.optimal_action or {}).get("amount", 0),
            "ev_difference": (evaluation.ev_analysis or {}).get("ev_difference", 0),
            "leak_identified": (evaluation.mistake_analysis or {}).get("leak_type", "none"),
            "explanation": (evaluation.coaching_feedback or {}).get("immediate_feedback", ""),
            "coaching_tip": (evaluation.coaching_feedback or {}).get("improvement_tip", ""),
            "improvement_areas": evaluation.key_concepts or [],
            "severity": (evaluation.mistake_analysis or {}).get("severity", 0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/progress/{player_id}")
async def get_ai_progress(
    player_id: str,
    db: Session = Depends(get_db)
):
    """Get AI-generated progress report."""
    
    try:
        progress = await ai_coach_service.get_progress_report(player_id, db)
        
        return {
            "overall_skill": progress.get("overall_accuracy", 0) * 100,
            "improvement_rate": progress.get("improvement_rate", 0),
            "biggest_leaks": progress.get("biggest_leaks", []),
            "recommended_focus": progress.get("recommended_focus", []),
            "stats": {
                "total_hands": progress.get("total_scenarios", 0),
                "win_rate": progress.get("overall_accuracy", 0) * 100,
                "accuracy_trend": progress.get("accuracy_trend", [])
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/coaching-plan/{player_id}")
async def get_coaching_plan(
    player_id: str,
    session_goals: List[str] = Query(default=None),
    db: Session = Depends(get_db)
):
    """Get AI-generated coaching plan."""
    
    if session_goals is None:
        session_goals = []
    
    try:
        coaching_plan = await ai_coach_service.generate_coaching_plan(
            player_id=player_id,
            session_goals=session_goals,
            db=db
        )
        
        return {
            "current_focus": coaching_plan.get("priority_areas", ["general_improvement"])[0],
            "exercises": coaching_plan.get("targeted_exercises", []),
            "concepts_to_study": coaching_plan.get("conceptual_learning", []),
            "estimated_sessions": coaching_plan.get("practice_structure", {}).get("sessions_needed", 5)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/coaching-session/start")
async def start_ai_coaching_session(
    player_id: str,
    session_goals: Optional[List[str]] = None,
    db: Session = Depends(get_db)
):
    """Start an AI coaching session."""
    
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

@router.get("/weakness-analysis/{player_id}")
async def get_weakness_analysis(
    player_id: str,
    limit: int = Query(20, ge=5, le=100),
    db: Session = Depends(get_db)
):
    """Get AI-powered weakness analysis."""
    
    try:
        from ..models.evaluation import Evaluation
        
        recent_evaluations = db.query(Evaluation).filter(Evaluation.player_id == player_id).order_by(Evaluation.created_at.desc()).limit(limit).all()
        
        analysis = await ai_coach_service._analyze_weaknesses(
            player_id=player_id,
            recent_evaluations=recent_evaluations
        )
        return analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/player-context/{player_id}")
async def get_player_context(
    player_id: str,
    db: Session = Depends(get_db)
):
    """Get player context and learning profile."""
    
    try:
        player_context = await ai_coach_service._get_player_context(player_id, db)
        
        if not player_context:
            raise HTTPException(status_code=404, detail="Player not found")
        
        return {
            "player_id": player_context.player_id,
            "skill_level": player_context.skill_level,
            "total_scenarios": player_context.total_scenarios,
            "total_sessions": player_context.total_sessions,
            "accuracy_trend": player_context.accuracy_trend,
            "weaknesses": player_context.weaknesses,
            "focus_areas": player_context.focus_areas,
            "preferred_difficulty": player_context.preferred_difficulty,
            "improvement_rate": player_context.improvement_rate,
            "last_session": player_context.last_session
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/player-context/{player_id}/initialize")
async def initialize_player_context(
    player_id: str,
    skill_level: str = "intermediate",
    db: Session = Depends(get_db)
):
    """Initialize a new player context."""
    
    try:
        from ..models.player_context import PlayerContextManager
        
        # Check if player already exists
        existing_context = await ai_coach_service._get_player_context(player_id, db)
        if existing_context:
            return {"message": "Player already exists", "player_id": player_id}
        
        # Create new player context
        player_context = PlayerContextManager.create_new_player(player_id, skill_level)
        db.add(player_context)
        db.commit()
        
        return {
            "message": "Player context initialized",
            "player_id": player_id,
            "skill_level": skill_level
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scenario-recommendations/{player_id}")
async def get_scenario_recommendations(
    player_id: str,
    db: Session = Depends(get_db)
):
    """Get AI-driven scenario recommendations."""
    
    try:
        from ..models.player_context import PlayerContextManager
        
        player_context = await ai_coach_service._get_player_context(player_id, db)
        
        if not player_context:
            raise HTTPException(status_code=404, detail="Player not found")
        
        recommendations = PlayerContextManager.get_next_scenario_recommendations(player_context)
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback/detailed")
async def get_detailed_feedback(
    evaluation_id: str,
    db: Session = Depends(get_db)
):
    """Get detailed AI feedback for an evaluation."""
    
    try:
        from ..models.evaluation import Evaluation
        
        evaluation = db.query(Evaluation).filter(Evaluation.evaluation_id == evaluation_id).first()
        
        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        
        return {
            "evaluation_id": evaluation.evaluation_id,
            "immediate_feedback": (evaluation.coaching_feedback or {}).get("immediate_feedback", ""),
            "concept_explanation": (evaluation.coaching_feedback or {}).get("concept_explanation", ""),
            "improvement_tip": (evaluation.coaching_feedback or {}).get("improvement_tip", ""),
            "practice_suggestion": (evaluation.coaching_feedback or {}).get("practice_suggestion", ""),
            "performance_impact": evaluation.performance_impact or {},
            "key_concepts": evaluation.key_concepts or [],
            "difficulty_assessment": evaluation.difficulty_assessment or {},
            "follow_up_scenarios": evaluation.follow_up_scenarios or []
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/global")
async def get_global_stats(
    db: Session = Depends(get_db)
):
    """Get global statistics for the application."""
    
    try:
        from ..models.evaluation import Evaluation
        from ..models.scenario import Scenario
        
        total_evaluations = db.query(Evaluation).count()
        total_scenarios = db.query(Scenario).count()
        
        return {
            "total_evaluations": total_evaluations,
            "total_scenarios": total_scenarios
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI Provider Management Endpoints
@router.get("/providers/status")
async def get_ai_providers_status():
    """Get status of all AI providers."""
    
    try:
        from ..config.settings import get_settings
        settings = get_settings()
        
        # Configure and get provider status
        ai_provider_manager.configure_from_env(settings)
        await ai_provider_manager.initialize()
        
        status = await ai_provider_manager.get_provider_status()
        available_providers = await ai_provider_manager.get_available_providers()
        preferred_provider = await ai_provider_manager.get_preferred_provider()
        
        return {
            "available_providers": available_providers,
            "preferred_provider": preferred_provider,
            "provider_status": status,
            "total_providers": len(status),
            "healthy_providers": len([p for p in status.values() if p.healthy])
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "available_providers": [],
            "preferred_provider": None,
            "provider_status": {},
            "total_providers": 0,
            "healthy_providers": 0
        }

@router.get("/providers/test/{provider_name}")
async def test_ai_provider(provider_name: str):
    """Test a specific AI provider."""
    
    try:
        from ..config.settings import get_settings
        settings = get_settings()
        
        ai_provider_manager.configure_from_env(settings)
        await ai_provider_manager.initialize()
        
        response = await ai_provider_manager.generate_text(
            prompt="Hello, this is a test. Please respond with 'Hello from [provider name]'",
            preferred_provider=provider_name,
            max_tokens=50
        )
        
        return {
            "status": "success",
            "provider": response.provider,
            "model": response.model,
            "response": response.content,
            "usage": response.usage
        }
        
    except Exception as e:
        return {
            "status": "error",
            "provider": provider_name,
            "error": str(e)
        }

# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check for AI coach service."""
    
    return {
        "status": "healthy",
        "service": "ai-coach",
        "timestamp": datetime.now(timezone.utc),
        "version": "1.0.0"
    }