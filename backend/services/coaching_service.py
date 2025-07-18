"""
Coaching service - High-level coaching operations.
"""

from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from .ai_coach_service import ai_coach_service
from ..models.scenario import ScenarioRequest, ScenarioResponse
from ..models.evaluation import EvaluationRequest, EvaluationResponse
from ..models.player_context import PlayerContext, PlayerContextManager

class CoachingService:
    """High-level coaching service orchestrating AI coach operations."""
    
    def __init__(self):
        self.ai_coach = ai_coach_service
    
    async def start_coaching_session(
        self,
        player_id: str,
        session_goals: List[str],
        db: Session
    ) -> Dict[str, Any]:
        """Start a new coaching session."""
        
        try:
            # Get player context
            player_context = await self.ai_coach._get_player_context(player_id, db)
            
            # Generate coaching plan
            coaching_plan = await self.ai_coach.generate_coaching_plan(
                player_id,
                session_goals,
                db
            )
            
            # Get first scenario recommendation
            recommendations = PlayerContextManager.get_next_scenario_recommendations(player_context)
            
            return {
                "session_id": f"session_{datetime.utcnow().timestamp()}",
                "player_id": player_id,
                "coaching_plan": coaching_plan,
                "recommendations": recommendations,
                "session_goals": session_goals,
                "started_at": datetime.utcnow()
            }
            
        except Exception as e:
            raise Exception(f"Error starting coaching session: {str(e)}")
    
    async def get_next_scenario(
        self,
        player_id: str,
        preferences: Dict[str, Any],
        db: Session
    ) -> ScenarioResponse:
        """Get the next scenario for a player."""
        
        try:
            # Get player context for personalization
            player_context = await self.ai_coach._get_player_context(player_id, db)
            
            # Build scenario request
            scenario_request = ScenarioRequest(
                tournament_stage=preferences.get("tournament_stage", "middle"),
                stack_depth=preferences.get("stack_depth", 30),
                difficulty=preferences.get("difficulty", player_context.preferred_difficulty),
                player_id=player_id,
                focus_area=preferences.get("focus_area", player_context.focus_areas[0] if player_context.focus_areas else None),
                game_format=preferences.get("game_format", "MTT"),
                scenario_type=preferences.get("scenario_type", "general")
            )
            
            # Generate scenario
            scenario = await self.ai_coach.generate_scenario(scenario_request, db)
            
            return scenario
            
        except Exception as e:
            raise Exception(f"Error getting next scenario: {str(e)}")
    
    async def submit_decision(
        self,
        scenario_id: str,
        player_id: str,
        player_action: str,
        player_amount: Optional[int] = None,
        time_taken: Optional[float] = None,
        db: Session = None
    ) -> EvaluationResponse:
        """Submit and evaluate a player decision."""
        
        try:
            # Build evaluation request
            evaluation_request = EvaluationRequest(
                scenario_id=scenario_id,
                player_id=player_id,
                player_action=player_action,
                player_amount=player_amount,
                time_taken=time_taken
            )
            
            # Evaluate decision
            evaluation = await self.ai_coach.evaluate_decision(evaluation_request, db)
            
            return evaluation
            
        except Exception as e:
            raise Exception(f"Error submitting decision: {str(e)}")
    
    async def get_player_progress(
        self,
        player_id: str,
        db: Session
    ) -> Dict[str, Any]:
        """Get comprehensive player progress report."""
        
        try:
            # Get progress report from AI coach
            progress_report = await self.ai_coach.get_progress_report(player_id, db)
            
            # Add additional coaching insights
            coaching_insights = await self._generate_coaching_insights(player_id, db)
            
            return {
                **progress_report,
                "coaching_insights": coaching_insights
            }
            
        except Exception as e:
            raise Exception(f"Error getting player progress: {str(e)}")
    
    async def get_session_summary(
        self,
        player_id: str,
        session_start: datetime,
        db: Session
    ) -> Dict[str, Any]:
        """Generate session summary."""
        
        try:
            # Get evaluations from this session
            session_evaluations = await self.ai_coach._get_recent_evaluations(player_id, db, limit=50)
            
            # Filter evaluations to this session
            session_evaluations = [
                eval for eval in session_evaluations
                if eval.created_at >= session_start
            ]
            
            if not session_evaluations:
                return {
                    "message": "No scenarios completed in this session",
                    "session_duration": 0,
                    "scenarios_completed": 0
                }
            
            # Calculate session metrics
            correct_decisions = sum(1 for eval in session_evaluations if eval.correct)
            total_scenarios = len(session_evaluations)
            accuracy_rate = correct_decisions / total_scenarios if total_scenarios > 0 else 0
            
            # Get concepts practiced
            concepts_practiced = set()
            leaks_identified = set()
            
            for eval in session_evaluations:
                concepts_practiced.update(eval.key_concepts)
                if eval.mistake_analysis:
                    leaks_identified.add(eval.mistake_analysis.get("leak_type", "unknown"))
            
            session_duration = (datetime.utcnow() - session_start).total_seconds() / 60  # minutes
            
            return {
                "session_duration": session_duration,
                "scenarios_completed": total_scenarios,
                "correct_decisions": correct_decisions,
                "accuracy_rate": accuracy_rate,
                "concepts_practiced": list(concepts_practiced),
                "leaks_identified": list(leaks_identified),
                "session_start": session_start,
                "session_end": datetime.utcnow()
            }
            
        except Exception as e:
            raise Exception(f"Error generating session summary: {str(e)}")
    
    async def get_adaptive_difficulty(
        self,
        player_id: str,
        db: Session
    ) -> Dict[str, Any]:
        """Get adaptive difficulty recommendations."""
        
        try:
            player_context = await self.ai_coach._get_player_context(player_id, db)
            recent_evaluations = await self.ai_coach._get_recent_evaluations(player_id, db, limit=10)
            
            if not recent_evaluations:
                return {
                    "recommended_difficulty": "intermediate",
                    "reasoning": "No recent evaluations available"
                }
            
            # Calculate recent performance
            recent_accuracy = sum(1 for eval in recent_evaluations if eval.correct) / len(recent_evaluations)
            
            # Adjust difficulty based on performance
            if recent_accuracy > 0.8:
                recommended_difficulty = "advanced"
                reasoning = "High accuracy suggests ready for more challenging scenarios"
            elif recent_accuracy > 0.6:
                recommended_difficulty = "intermediate"
                reasoning = "Good accuracy, maintain current difficulty"
            else:
                recommended_difficulty = "beginner"
                reasoning = "Lower accuracy suggests need for easier scenarios"
            
            return {
                "recommended_difficulty": recommended_difficulty,
                "reasoning": reasoning,
                "recent_accuracy": recent_accuracy,
                "total_evaluations": len(recent_evaluations)
            }
            
        except Exception as e:
            raise Exception(f"Error getting adaptive difficulty: {str(e)}")
    
    async def _generate_coaching_insights(
        self,
        player_id: str,
        db: Session
    ) -> Dict[str, Any]:
        """Generate additional coaching insights."""
        
        try:
            player_context = await self.ai_coach._get_player_context(player_id, db)
            
            # Calculate session frequency
            sessions_per_week = 0
            if player_context.last_session:
                days_since_last = (datetime.utcnow() - player_context.last_session).days
                if days_since_last > 0:
                    sessions_per_week = player_context.total_sessions / (days_since_last / 7)
            
            # Generate insights
            insights = []
            
            if sessions_per_week < 2:
                insights.append("Consider increasing session frequency to 2-3 times per week for better improvement")
            
            if player_context.improvement_rate < 0.01:
                insights.append("Improvement rate is slow - consider focusing on specific weakness areas")
            
            if len(player_context.focus_areas) > 3:
                insights.append("Too many focus areas - consider narrowing down to 2-3 key areas")
            
            return {
                "insights": insights,
                "sessions_per_week": sessions_per_week,
                "days_since_last_session": (datetime.utcnow() - player_context.last_session).days if player_context.last_session else None
            }
            
        except Exception as e:
            return {"error": f"Error generating insights: {str(e)}"}

# Create singleton instance
coaching_service = CoachingService()