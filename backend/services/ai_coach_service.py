"""
AI Coach Service - Core AI integration for poker coaching.
"""

import json
import uuid
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from sqlalchemy.orm import Session

from ..models.scenario import Scenario, ScenarioRequest, ScenarioResponse
from ..models.evaluation import Evaluation, EvaluationRequest, EvaluationResponse
from ..models.player_context import PlayerContext, PlayerContextManager
from ..prompts.scenario_prompts import (
    build_scenario_prompt,
    build_postflop_scenario_prompt,
    build_bubble_scenario_prompt,
    COACHING_SYSTEM_PROMPT
)
from ..prompts.evaluation_prompts import (
    build_evaluation_prompt,
    build_weakness_analysis_prompt,
    build_coaching_plan_prompt
)
from ..config.settings import get_settings

settings = get_settings()

class AICoachService:
    """Core AI service for poker coaching."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL or "gpt-4o"
        self.temperature = 0.7
        self.max_tokens = 2000
        self.player_contexts = {}  # In-memory cache for player contexts
    
    async def generate_scenario(
        self,
        request: ScenarioRequest,
        db: Session
    ) -> ScenarioResponse:
        """Generate a new MTT scenario using AI."""
        
        try:
            # Get player context for personalization
            player_context = await self._get_player_context(request.player_id, db)
            
            # Build the prompt based on request parameters
            prompt = self._build_scenario_prompt(request, player_context)
            
            # Generate scenario using OpenAI
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": COACHING_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Parse the response
            scenario_data = self._parse_scenario_response(response.choices[0].message.content)
            
            # Save to database
            scenario = await self._save_scenario(scenario_data, db)
            
            return ScenarioResponse(**scenario_data)
            
        except Exception as e:
            raise Exception(f"Error generating scenario: {str(e)}")
    
    async def evaluate_decision(
        self,
        request: EvaluationRequest,
        db: Session
    ) -> EvaluationResponse:
        """Evaluate a player's decision using AI."""
        
        try:
            # Get scenario and player context
            scenario = db.query(Scenario).filter(
                Scenario.scenario_id == request.scenario_id
            ).first()
            
            if not scenario:
                raise Exception("Scenario not found")
            
            player_context = await self._get_player_context(request.player_id, db)
            
            # Build evaluation prompt
            scenario_data = self._scenario_to_dict(scenario)
            prompt = build_evaluation_prompt(
                scenario_data,
                request.player_action,
                player_context.__dict__ if player_context else None,
                request.time_taken
            )
            
            # Generate evaluation using OpenAI
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": COACHING_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Parse the response
            evaluation_data = self._parse_evaluation_response(response.choices[0].message.content)
            
            # Save to database
            evaluation = await self._save_evaluation(evaluation_data, request, db)
            
            # Update player context
            await self._update_player_context(request.player_id, evaluation_data, db)
            
            return EvaluationResponse(**evaluation_data)
            
        except Exception as e:
            raise Exception(f"Error evaluating decision: {str(e)}")
    
    async def generate_coaching_plan(
        self,
        player_id: str,
        session_goals: List[str],
        db: Session
    ) -> Dict[str, Any]:
        """Generate a personalized coaching plan."""
        
        try:
            # Get player context and recent evaluations
            player_context = await self._get_player_context(player_id, db)
            recent_evaluations = await self._get_recent_evaluations(player_id, db, limit=20)
            
            # Analyze weaknesses
            weakness_analysis = await self._analyze_weaknesses(player_id, recent_evaluations)
            
            # Build coaching plan prompt
            prompt = build_coaching_plan_prompt(
                player_context.__dict__ if player_context else {},
                weakness_analysis,
                session_goals
            )
            
            # Generate plan using OpenAI
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": COACHING_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Parse and return the coaching plan
            coaching_plan = self._parse_coaching_plan_response(response.choices[0].message.content)
            return coaching_plan
            
        except Exception as e:
            raise Exception(f"Error generating coaching plan: {str(e)}")
    
    async def get_progress_report(
        self,
        player_id: str,
        db: Session
    ) -> Dict[str, Any]:
        """Generate a progress report for a player."""
        
        try:
            player_context = await self._get_player_context(player_id, db)
            recent_evaluations = await self._get_recent_evaluations(player_id, db, limit=50)
            
            if not player_context:
                return {"error": "Player not found"}
            
            # Calculate progress metrics
            progress_metrics = self._calculate_progress_metrics(player_context, recent_evaluations)
            
            return {
                "player_id": player_id,
                "skill_level": player_context.skill_level,
                "overall_accuracy": progress_metrics["overall_accuracy"],
                "improvement_rate": progress_metrics["improvement_rate"],
                "sessions_completed": player_context.total_sessions,
                "total_scenarios": player_context.total_scenarios,
                "biggest_leaks": progress_metrics["biggest_leaks"],
                "strength_areas": progress_metrics["strength_areas"],
                "recommended_focus": progress_metrics["recommended_focus"],
                "accuracy_trend": player_context.accuracy_trend[-20:],
                "last_session": player_context.last_session
            }
            
        except Exception as e:
            raise Exception(f"Error generating progress report: {str(e)}")
    
    def _build_scenario_prompt(
        self,
        request: ScenarioRequest,
        player_context: Optional[PlayerContext]
    ) -> str:
        """Build the scenario generation prompt."""
        
        # Determine focus area based on player weaknesses
        focus_area = request.focus_area
        if not focus_area and player_context:
            focus_areas = player_context.focus_areas
            if focus_areas:
                focus_area = focus_areas[0]
        
        # Select appropriate prompt template
        if request.tournament_stage == "bubble":
            return build_bubble_scenario_prompt(
                players_remaining=45,  # Default values
                paid_spots=36,
                stack_depth=request.stack_depth,
                difficulty=request.difficulty
            )
        elif request.scenario_type == "postflop":
            return build_postflop_scenario_prompt(
                request.tournament_stage,
                request.stack_depth,
                "flop",  # Default street
                focus_area,
                request.difficulty
            )
        else:
            return build_scenario_prompt(
                request.tournament_stage,
                request.stack_depth,
                focus_area,
                request.difficulty,
                request.game_format
            )
    
    def _parse_scenario_response(self, response_content: str) -> Dict[str, Any]:
        """Parse the AI response into scenario data."""
        
        try:
            # Extract JSON from response
            json_start = response_content.find('{')
            json_end = response_content.rfind('}') + 1
            json_content = response_content[json_start:json_end]
            
            scenario_data = json.loads(json_content)
            
            # Add metadata
            scenario_data["scenario_id"] = str(uuid.uuid4())
            scenario_data["created_at"] = datetime.utcnow()
            
            return scenario_data
            
        except (json.JSONDecodeError, ValueError) as e:
            raise Exception(f"Failed to parse scenario response: {str(e)}")
    
    def _parse_evaluation_response(self, response_content: str) -> Dict[str, Any]:
        """Parse the AI response into evaluation data."""
        
        try:
            # Extract JSON from response
            json_start = response_content.find('{')
            json_end = response_content.rfind('}') + 1
            json_content = response_content[json_start:json_end]
            
            evaluation_data = json.loads(json_content)
            
            # Add metadata
            evaluation_data["evaluation_id"] = str(uuid.uuid4())
            evaluation_data["created_at"] = datetime.utcnow()
            
            return evaluation_data
            
        except (json.JSONDecodeError, ValueError) as e:
            raise Exception(f"Failed to parse evaluation response: {str(e)}")
    
    def _parse_coaching_plan_response(self, response_content: str) -> Dict[str, Any]:
        """Parse the AI response into coaching plan data."""
        
        try:
            # Extract JSON from response
            json_start = response_content.find('{')
            json_end = response_content.rfind('}') + 1
            json_content = response_content[json_start:json_end]
            
            coaching_plan = json.loads(json_content)
            
            # Add metadata
            coaching_plan["created_at"] = datetime.utcnow()
            
            return coaching_plan
            
        except (json.JSONDecodeError, ValueError) as e:
            raise Exception(f"Failed to parse coaching plan response: {str(e)}")
    
    async def _get_player_context(
        self,
        player_id: str,
        db: Session
    ) -> Optional[PlayerContext]:
        """Get or create player context."""
        
        # Check cache first
        if player_id in self.player_contexts:
            return self.player_contexts[player_id]
        
        # Query database
        player_context = db.query(PlayerContext).filter(
            PlayerContext.player_id == player_id
        ).first()
        
        if not player_context:
            # Create new player context
            player_context = PlayerContextManager.create_new_player(player_id, "intermediate")
            db.add(player_context)
            db.commit()
        
        # Cache the context
        self.player_contexts[player_id] = player_context
        
        return player_context
    
    async def _save_scenario(
        self,
        scenario_data: Dict[str, Any],
        db: Session
    ) -> Scenario:
        """Save scenario to database."""
        
        scenario = Scenario(**scenario_data)
        db.add(scenario)
        db.commit()
        db.refresh(scenario)
        
        return scenario
    
    async def _save_evaluation(
        self,
        evaluation_data: Dict[str, Any],
        request: EvaluationRequest,
        db: Session
    ) -> Evaluation:
        """Save evaluation to database."""
        
        evaluation = Evaluation(
            evaluation_id=evaluation_data["evaluation_id"],
            scenario_id=request.scenario_id,
            player_id=request.player_id,
            player_action=request.player_action,
            player_amount=request.player_amount,
            time_taken=request.time_taken,
            correct=evaluation_data["correct"],
            optimal_action=evaluation_data["optimal_action"],
            ev_analysis=evaluation_data["ev_analysis"],
            mistake_analysis=evaluation_data.get("mistake_analysis"),
            coaching_feedback=evaluation_data["coaching_feedback"],
            performance_impact=evaluation_data["performance_impact"],
            key_concepts=evaluation_data["key_concepts"],
            difficulty_assessment=evaluation_data["difficulty_assessment"],
            follow_up_scenarios=evaluation_data.get("follow_up_scenarios")
        )
        
        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)
        
        return evaluation
    
    async def _update_player_context(
        self,
        player_id: str,
        evaluation_data: Dict[str, Any],
        db: Session
    ) -> None:
        """Update player context based on evaluation."""
        
        player_context = await self._get_player_context(player_id, db)
        
        if player_context:
            # Update using PlayerContextManager
            updated_context = PlayerContextManager.update_from_evaluation(
                player_context,
                evaluation_data
            )
            
            # Update counters
            updated_context.total_scenarios += 1
            if evaluation_data.get("correct", False):
                updated_context.correct_decisions += 1
            
            # Update cache
            self.player_contexts[player_id] = updated_context
            
            # Save to database
            db.commit()
    
    async def _get_recent_evaluations(
        self,
        player_id: str,
        db: Session,
        limit: int = 20
    ) -> List[Evaluation]:
        """Get recent evaluations for a player."""
        
        return db.query(Evaluation).filter(
            Evaluation.player_id == player_id
        ).order_by(Evaluation.created_at.desc()).limit(limit).all()
    
    async def _analyze_weaknesses(
        self,
        player_id: str,
        evaluations: List[Evaluation]
    ) -> Dict[str, Any]:
        """Analyze player weaknesses from recent evaluations."""
        
        if not evaluations:
            return {"message": "No recent evaluations to analyze"}
        
        # Build weakness analysis prompt
        player_decisions = []
        for eval in evaluations:
            player_decisions.append({
                "scenario_summary": f"MTT {eval.scenario.tournament_stage} stage",
                "player_action": eval.player_action,
                "optimal_action": eval.optimal_action.get("action", "unknown"),
                "ev_difference": eval.ev_analysis.get("ev_difference", 0),
                "leak_type": eval.mistake_analysis.get("leak_type", "none") if eval.mistake_analysis else "none"
            })
        
        prompt = build_weakness_analysis_prompt(
            player_decisions,
            {"player_id": player_id}
        )
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": COACHING_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Parse weakness analysis
            json_start = response.choices[0].message.content.find('{')
            json_end = response.choices[0].message.content.rfind('}') + 1
            json_content = response.choices[0].message.content[json_start:json_end]
            
            return json.loads(json_content)
            
        except Exception as e:
            return {"error": f"Failed to analyze weaknesses: {str(e)}"}
    
    def _calculate_progress_metrics(
        self,
        player_context: PlayerContext,
        evaluations: List[Evaluation]
    ) -> Dict[str, Any]:
        """Calculate progress metrics for a player."""
        
        if not evaluations:
            return {
                "overall_accuracy": 0.0,
                "improvement_rate": 0.0,
                "biggest_leaks": [],
                "strength_areas": [],
                "recommended_focus": []
            }
        
        # Calculate accuracy
        correct_count = sum(1 for eval in evaluations if eval.correct)
        overall_accuracy = correct_count / len(evaluations)
        
        # Get top weaknesses
        weakness_scores = []
        for category, weaknesses in player_context.weaknesses.items():
            for weakness, score in weaknesses.items():
                if score > 0:
                    weakness_scores.append({
                        "type": f"{category}.{weakness}",
                        "severity": score
                    })
        
        biggest_leaks = sorted(weakness_scores, key=lambda x: x["severity"], reverse=True)[:3]
        
        # Calculate improvement rate
        improvement_rate = player_context.improvement_rate
        
        return {
            "overall_accuracy": overall_accuracy,
            "improvement_rate": improvement_rate,
            "biggest_leaks": biggest_leaks,
            "strength_areas": player_context.strength_areas,
            "recommended_focus": player_context.focus_areas
        }
    
    def _scenario_to_dict(self, scenario: Scenario) -> Dict[str, Any]:
        """Convert scenario database object to dictionary."""
        
        return {
            "scenario_id": scenario.scenario_id,
            "tournament_stage": scenario.tournament_stage,
            "hero_position": scenario.hero_position,
            "hero_stack": scenario.hero_stack,
            "hero_cards": scenario.hero_cards,
            "villain_positions": scenario.villain_positions,
            "blinds": scenario.blinds,
            "ante": scenario.ante,
            "players_remaining": scenario.players_remaining,
            "action_history": scenario.action_history,
            "current_street": scenario.current_street,
            "board": scenario.board,
            "pot_size": scenario.pot_size,
            "to_call": scenario.to_call,
            "optimal_action": scenario.optimal_action
        }

# Create singleton instance
ai_coach_service = AICoachService()