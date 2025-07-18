"""
Prompt templates for evaluating player decisions in MTT scenarios.
"""

def build_evaluation_prompt(
    scenario_data: dict,
    player_action: str,
    player_context: dict = None,
    time_taken: float = None
) -> str:
    """
    Generate prompt for evaluating a player's decision.
    
    Args:
        scenario_data: The original scenario data
        player_action: The action taken by the player
        player_context: Player's weakness profile and history
        time_taken: Time taken to make decision (optional)
    """
    
    context_section = ""
    if player_context:
        context_section = f"""
        PLAYER CONTEXT:
        - Skill Level: {player_context.get('skill_level', 'unknown')}
        - Known Weaknesses: {player_context.get('weaknesses', {})}
        - Recent Performance: {player_context.get('recent_stats', {})}
        - Focus Areas: {player_context.get('focus_areas', [])}
        """
    
    time_section = ""
    if time_taken:
        time_section = f"""
        DECISION TIME: {time_taken:.1f} seconds
        - Fast decisions (<5s) may indicate snap calls/folds
        - Slow decisions (>30s) may indicate difficult spots or uncertainty
        """
    
    return f"""
    You are an expert MTT poker coach evaluating a player's decision.
    
    ORIGINAL SCENARIO:
    {format_scenario_for_evaluation(scenario_data)}
    
    PLAYER ACTION: {player_action}
    
    {context_section}
    {time_section}
    
    EVALUATION CRITERIA:
    1. Mathematical Correctness
       - Pot odds calculations
       - Expected value (EV) analysis
       - ICM considerations
       - Stack depth adjustments
    
    2. Strategic Soundness
       - Position awareness
       - Tournament stage appropriateness
       - Risk vs reward assessment
       - Future play implications
    
    3. Technical Execution
       - Bet sizing (if applicable)
       - Timing and decision speed
       - Range considerations
       - Opponent modeling
    
    4. Learning Opportunity
       - Identify specific leaks
       - Categorize mistake type
       - Suggest improvement areas
       - Provide actionable advice
    
    Return ONLY a valid JSON object with this EXACT structure:
    {{
        "evaluation_id": "unique_eval_id",
        "scenario_id": "{scenario_data.get('scenario_id', 'unknown')}",
        "player_action": "{player_action}",
        "correct": true,
        "optimal_action": {{
            "action": "call",
            "amount": 150,
            "reasoning": "Detailed explanation of optimal play"
        }},
        "ev_analysis": {{
            "player_action_ev": 2.45,
            "optimal_action_ev": 2.87,
            "ev_difference": -0.42,
            "ev_explanation": "Calculation breakdown"
        }},
        "mistake_analysis": {{
            "leak_type": "postflop.bet_sizing",
            "severity": 6,
            "category": "technical",
            "frequency": "occasional",
            "description": "Specific description of the mistake"
        }},
        "coaching_feedback": {{
            "immediate_feedback": "What happened in this hand",
            "concept_explanation": "Underlying poker concepts",
            "improvement_tip": "Specific actionable advice",
            "practice_suggestion": "How to work on this area"
        }},
        "performance_impact": {{
            "short_term": "Immediate consequences",
            "long_term": "Pattern implications",
            "tournament_impact": "How this affects tournament success"
        }},
        "key_concepts": ["ICM", "position", "bet_sizing", "pot_odds"],
        "difficulty_assessment": {{
            "scenario_difficulty": 7,
            "decision_difficulty": 6,
            "common_mistake": true,
            "skill_level_required": "intermediate"
        }},
        "follow_up_scenarios": [
            "Similar ICM spots with different stack sizes",
            "Same opponent type in different position"
        ]
    }}
    """

def format_scenario_for_evaluation(scenario_data: dict) -> str:
    """Format scenario data for evaluation prompt."""
    
    board_str = ""
    if scenario_data.get("board"):
        board_str = f"Board: {' '.join(scenario_data['board'])}"
    
    action_history = ""
    if scenario_data.get("action_history"):
        action_history = f"Action: {' → '.join(scenario_data['action_history'])}"
    
    return f"""
    Tournament Stage: {scenario_data.get('tournament_stage', 'unknown')}
    Position: {scenario_data.get('hero_position', 'unknown')}
    Stack: {scenario_data.get('hero_stack', 0)} chips ({scenario_data.get('hero_stack', 0) // scenario_data.get('blinds', {}).get('big', 100)} BB)
    Blinds: {scenario_data.get('blinds', {}).get('small', 50)}/{scenario_data.get('blinds', {}).get('big', 100)}
    Ante: {scenario_data.get('ante', 0)}
    Hero Cards: {' '.join(scenario_data.get('hero_cards', []))}
    {board_str}
    {action_history}
    Pot Size: {scenario_data.get('pot_size', 0)}
    To Call: {scenario_data.get('to_call', 0)}
    Players Remaining: {scenario_data.get('players_remaining', 'unknown')}
    """

def build_weakness_analysis_prompt(
    player_decisions: list,
    player_context: dict
) -> str:
    """Generate prompt for analyzing player weaknesses across multiple decisions."""
    
    return f"""
    You are an expert MTT poker coach analyzing player weaknesses.
    
    PLAYER CONTEXT:
    {player_context}
    
    RECENT DECISIONS:
    {format_decisions_for_analysis(player_decisions)}
    
    WEAKNESS ANALYSIS FRAMEWORK:
    
    1. PREFLOP LEAKS:
       - Opening ranges (too tight/loose)
       - 3-betting frequency
       - Blind defense
       - Limping tendencies
       - Stealing frequency
    
    2. POSTFLOP LEAKS:
       - C-betting patterns
       - Bet sizing issues
       - Bluff frequency
       - Value betting
       - Pot control
    
    3. TOURNAMENT SPECIFIC:
       - ICM awareness
       - Stack depth adjustments
       - Bubble play
       - Final table dynamics
       - Risk assessment
    
    4. MENTAL GAME:
       - Decision speed
       - Tilt control
       - Confidence levels
       - Learning consistency
    
    Return ONLY a valid JSON object with comprehensive weakness analysis.
    """

def format_decisions_for_analysis(decisions: list) -> str:
    """Format multiple decisions for weakness analysis."""
    
    formatted_decisions = []
    for i, decision in enumerate(decisions, 1):
        formatted_decisions.append(f"""
        Decision {i}:
        - Scenario: {decision.get('scenario_summary', 'unknown')}
        - Player Action: {decision.get('player_action', 'unknown')}
        - Optimal Action: {decision.get('optimal_action', 'unknown')}
        - EV Difference: {decision.get('ev_difference', 0)}
        - Leak Type: {decision.get('leak_type', 'none')}
        """)
    
    return "\n".join(formatted_decisions)

def build_coaching_plan_prompt(
    player_context: dict,
    weakness_analysis: dict,
    session_goals: list = None
) -> str:
    """Generate personalized coaching plan based on player weaknesses."""
    
    goals_section = ""
    if session_goals:
        goals_section = f"""
        SESSION GOALS:
        {[goal for goal in session_goals]}
        """
    
    return f"""
    You are an expert MTT poker coach creating a personalized improvement plan.
    
    PLAYER PROFILE:
    {player_context}
    
    WEAKNESS ANALYSIS:
    {weakness_analysis}
    
    {goals_section}
    
    COACHING PLAN FRAMEWORK:
    
    1. PRIORITY AREAS (Top 3 leaks to address)
       - Most impactful weaknesses
       - Easiest to fix vs hardest
       - Frequency of occurrence
    
    2. TARGETED EXERCISES
       - Specific scenario types
       - Repetition requirements
       - Difficulty progression
    
    3. CONCEPTUAL LEARNING
       - Theory to study
       - Mathematical concepts
       - Strategic principles
    
    4. PRACTICE STRUCTURE
       - Session length recommendations
       - Frequency of practice
       - Progress milestones
    
    5. TRACKING METRICS
       - KPIs to monitor
       - Success indicators
       - Improvement timeline
    
    Return ONLY a valid JSON object with detailed coaching plan.
    """

# Common evaluation patterns
LEAK_CATEGORIES = {
    "preflop": {
        "opening_too_tight": "Opening ranges too narrow for position/stack depth",
        "opening_too_loose": "Opening too many hands, especially in early position",
        "three_bet_frequency": "3-betting too often or too rarely",
        "blind_defense": "Poor blind defense strategy",
        "limping_strong": "Limping with strong hands instead of raising",
        "stealing_frequency": "Not stealing blinds enough in late position"
    },
    "postflop": {
        "cbet_frequency": "C-betting too often or too rarely",
        "bet_sizing": "Incorrect bet sizing for situation",
        "bluff_frequency": "Bluffing too often or too rarely",
        "value_betting": "Missing value bets or betting too thin",
        "pot_control": "Poor pot control with marginal hands",
        "fold_equity": "Not considering fold equity in bluffs"
    },
    "tournament": {
        "icm_awareness": "Not adjusting play for ICM considerations",
        "stack_depth": "Not adjusting to effective stack sizes",
        "bubble_play": "Poor bubble strategy",
        "final_table": "Incorrect final table dynamics",
        "risk_assessment": "Poor risk vs reward evaluation"
    }
}

COACHING_TIPS = {
    "beginner": {
        "focus": "Basic fundamentals and hand selection",
        "concepts": ["position", "pot odds", "basic ranges"],
        "complexity": "Simple scenarios with clear correct answers"
    },
    "intermediate": {
        "focus": "Tournament dynamics and advanced postflop play",
        "concepts": ["ICM", "range analysis", "bet sizing", "bubble play"],
        "complexity": "Mixed scenarios with multiple viable options"
    },
    "advanced": {
        "focus": "GTO concepts and exploitative adjustments",
        "concepts": ["solver analysis", "population tendencies", "game theory"],
        "complexity": "Complex scenarios with marginal decisions"
    }
}