"""
Prompt templates for MTT scenario generation.
"""

def build_scenario_prompt(
    tournament_stage: str,
    stack_depth: int,
    player_weakness: str = None,
    difficulty: str = "intermediate",
    game_format: str = "MTT"
) -> str:
    """
    Generate prompt for creating realistic MTT poker scenarios.
    
    Args:
        tournament_stage: early, middle, bubble, itm, final_table
        stack_depth: Stack depth in big blinds
        player_weakness: Specific weakness to target (optional)
        difficulty: beginner, intermediate, advanced
        game_format: MTT, SNG, etc.
    """
    
    weakness_context = ""
    if player_weakness:
        weakness_context = f"""
        FOCUS AREA: Create a scenario that specifically tests "{player_weakness}".
        The scenario should expose this weakness and provide learning opportunities.
        """
    
    return f"""
    You are an expert MTT poker coach generating realistic training scenarios.
    
    Generate a specific MTT poker scenario with these parameters:
    - Tournament Stage: {tournament_stage}
    - Stack Depth: {stack_depth} BB
    - Difficulty Level: {difficulty}
    - Game Format: {game_format}
    
    {weakness_context}
    
    TOURNAMENT STAGE GUIDELINES:
    - Early: Deep stacks (50+ BB), focus on postflop play, building pots
    - Middle: Medium stacks (20-50 BB), antes in play, stealing becomes important
    - Bubble: High ICM pressure, tight play, survival mode
    - ITM: In the money, ladder considerations, risk vs reward
    - Final Table: Maximum ICM pressure, stack dynamics crucial
    
    STACK DEPTH CONSIDERATIONS:
    - Deep (50+ BB): Complex postflop decisions, implied odds, set mining
    - Medium (20-50 BB): Standard tournament play, position important
    - Short (10-20 BB): Push/fold considerations, all-in or fold decisions
    - Micro (<10 BB): Pure push/fold, Nash equilibrium ranges
    
    Return ONLY a valid JSON object with this EXACT structure:
    {{
        "scenario_id": "unique_scenario_id",
        "tournament_stage": "{tournament_stage}",
        "hero_position": "BTN|CO|MP|EP|SB|BB|UTG|UTG+1|UTG+2",
        "hero_stack": {stack_depth * 100},
        "hero_cards": ["As", "Kh"],
        "villain_positions": [{{"position": "CO", "stack": 2000, "player_type": "tight_aggressive"}}],
        "blinds": {{"small": 50, "big": 100}},
        "ante": 10,
        "players_remaining": 45,
        "total_players": 180,
        "prize_pool": 10000,
        "current_payouts": {{"9th": 500, "1st": 2500}},
        "action_history": ["UTG folds", "UTG+1 folds", "MP raises to 250", "CO folds"],
        "current_street": "preflop",
        "board": [],
        "pot_size": 425,
        "to_call": 150,
        "min_raise": 250,
        "max_raise": {stack_depth * 100},
        "valid_actions": ["fold", "call", "raise"],
        "scenario_description": "Detailed description of the situation and context",
        "key_concepts": ["position", "stack_depths", "ICM", "pot_odds"],
        "optimal_action": {{
            "action": "call",
            "amount": 150,
            "reasoning": "Detailed explanation of why this is optimal",
            "gto_frequency": 0.65
        }},
        "alternative_actions": [
            {{
                "action": "fold",
                "ev_difference": -1.2,
                "reasoning": "Why this is suboptimal"
            }},
            {{
                "action": "raise",
                "amount": 400,
                "ev_difference": -0.8,
                "reasoning": "Why this is suboptimal"
            }}
        ],
        "difficulty_factors": ["ICM pressure", "difficult opponent read", "close EV decision"],
        "learning_objectives": ["Understanding ICM", "Position awareness", "Stack depth adjustments"]
    }}
    """

def build_postflop_scenario_prompt(
    tournament_stage: str,
    stack_depth: int,
    street: str,
    player_weakness: str = None,
    difficulty: str = "intermediate"
) -> str:
    """Generate prompt for postflop scenarios."""
    
    weakness_context = ""
    if player_weakness:
        weakness_context = f"""
        FOCUS AREA: Create a scenario that specifically tests "{player_weakness}".
        """
    
    return f"""
    You are an expert MTT poker coach generating realistic postflop training scenarios.
    
    Generate a specific MTT postflop scenario:
    - Tournament Stage: {tournament_stage}
    - Stack Depth: {stack_depth} BB
    - Street: {street}
    - Difficulty: {difficulty}
    
    {weakness_context}
    
    POSTFLOP CONSIDERATIONS:
    - Flop: C-betting, board texture, range advantage
    - Turn: Barrel decisions, pot control, range polarization
    - River: Value betting, bluff catching, bet sizing
    
    The scenario should test postflop decision-making skills including:
    - Bet sizing
    - Bluff frequency
    - Value betting
    - Pot control
    - Range reading
    
    Return ONLY a valid JSON object with detailed postflop scenario structure.
    """

def build_bubble_scenario_prompt(
    players_remaining: int,
    paid_spots: int,
    stack_depth: int,
    difficulty: str = "intermediate"
) -> str:
    """Generate bubble-specific scenarios with ICM considerations."""
    
    return f"""
    You are an expert MTT poker coach generating realistic bubble scenarios.
    
    Generate a bubble scenario with maximum ICM pressure:
    - Players Remaining: {players_remaining}
    - Paid Spots: {paid_spots}
    - Stack Depth: {stack_depth} BB
    - Difficulty: {difficulty}
    
    BUBBLE DYNAMICS:
    - Short stacks desperate to survive
    - Medium stacks trying to pressure bubble
    - Big stacks can apply maximum pressure
    - ICM considerations paramount
    
    Focus on:
    - Risk vs reward calculations
    - ICM pressure dynamics
    - Bubble strategy adjustments
    - Survival considerations
    
    Return ONLY a valid JSON object emphasizing ICM decision-making.
    """

# Additional prompt templates for specific scenarios
COACHING_SYSTEM_PROMPT = """
You are an expert MTT poker coach with deep knowledge of:
- Game theory optimal (GTO) play
- Independent Chip Model (ICM) calculations
- Tournament dynamics and stages
- Player psychology and tendencies
- Bankroll management
- Risk assessment

Your role is to generate realistic, educational poker scenarios that help players improve their MTT skills.
Always provide detailed reasoning for optimal plays and explain the underlying concepts.
"""

EVALUATION_CONTEXT_PROMPT = """
When evaluating player decisions, consider:
1. Mathematical correctness (pot odds, implied odds, EV calculations)
2. Tournament context (ICM, stack sizes, stage of tournament)
3. Player tendencies and reads
4. Risk vs reward in tournament setting
5. Future play implications

Provide constructive feedback that helps the player understand both the immediate decision and the underlying concepts.
"""