export interface Scenario {
  id: string;
  tournament_stage: string;
  hero_position: string;
  hero_cards: string[];
  hero_stack: number;
  villain_positions: VillainPosition[];
  blinds: {
    small: number;
    big: number;
  };
  ante: number;
  players_remaining: number;
  total_players: number;
  prize_pool: number;
  current_payouts?: { [key: string]: number };
  action_history: string[];
  current_street: string;
  board: string[];
  pot_size: number;
  to_call: number;
  min_raise: number;
  max_raise: number;
  valid_actions: string[];
  scenario_description: string;
  key_concepts: string[];
  optimal_action: OptimalAction;
  alternative_actions: AlternativeAction[];
  difficulty_factors: string[];
  learning_objectives: string[];
  difficulty_level: string;
  created_at: string;
}

export interface VillainPosition {
  position: string;
  stack: number;
  player_type: string;
  vpip?: number;
  pfr?: number;
  aggression?: number;
  tendency?: string;
  notes?: string;
}

export interface OptimalAction {
  action: string;
  amount?: number;
  reasoning: string;
  gto_frequency?: number;
  ev_estimate?: number;
  risk_assessment?: string;
}

export interface AlternativeAction {
  action: string;
  amount?: number;
  ev_difference: number;
  reasoning: string;
  frequency?: number;
}

export interface Evaluation {
  evaluation_id: string;
  scenario_id: string;
  player_action: string;
  correct: boolean;
  optimal_action: string;
  optimal_amount?: number;
  ev_difference: number;
  leak_identified?: string;
  explanation: string;
  coaching_tip: string;
  improvement_areas: string[];
  severity: number;
  created_at: string;
}

export interface ProgressReport {
  overall_skill: number;
  improvement_rate: number;
  biggest_leaks: Array<{
    type: string;
    severity: number;
  }>;
  recommended_focus: string[];
  stats: {
    total_hands: number;
    win_rate: number;
    accuracy_trend: number[];
  };
}

export interface PlayerContext {
  player_id: string;
  skill_level: string;
  total_scenarios: number;
  total_sessions: number;
  accuracy_trend: number[];
  weaknesses: { [category: string]: { [weakness: string]: number } };
  focus_areas: string[];
  preferred_difficulty: string;
  improvement_rate: number;
  last_session?: string;
}

export interface CoachingPlan {
  current_focus: string;
  exercises: Array<{
    type: string;
    description: string;
    target_hands?: number;
  }>;
  concepts_to_study: string[];
  estimated_sessions: number;
}

export interface WeaknessAnalysis {
  analysis: { [category: string]: any };
  recommendations: string[];
  priority_areas: string[];
}

export interface SessionSummary {
  session_duration: number;
  scenarios_completed: number;
  correct_decisions: number;
  accuracy_rate: number;
  concepts_practiced: string[];
  leaks_identified: string[];
  session_start: string;
  session_end: string;
}

export interface AdaptiveDifficulty {
  recommended_difficulty: string;
  reasoning: string;
  recent_accuracy: number;
  total_evaluations: number;
}

export interface DetailedFeedback {
  evaluation_id: string;
  immediate_feedback: string;
  concept_explanation: string;
  improvement_tip: string;
  practice_suggestion: string;
  performance_impact: { [key: string]: any };
  key_concepts: string[];
  difficulty_assessment: { [key: string]: any };
  follow_up_scenarios?: string[];
}

export interface ScenarioRecommendation {
  focus_weakness?: string;
  difficulty_level: string;
  scenario_types: string[];
  session_goals: string[];
}

export interface GlobalStats {
  total_evaluations: number;
  total_players: number;
  recent_evaluations: number;
  avg_accuracy: number;
  popular_concepts: string[];
}

export interface PlayerStats {
  total_scenarios: number;
  correct_decisions: number;
  accuracy_rate: number;
  avg_decision_time: number;
}

export interface GameSession {
  session_id: string;
  player_id: string;
  coaching_plan: CoachingPlan;
  recommendations: ScenarioRecommendation;
  started_at: string;
}

// Enums for better type safety
export enum TournamentStage {
  EARLY = 'early',
  MIDDLE = 'middle',
  BUBBLE = 'bubble',
  ITM = 'itm',
  FINAL_TABLE = 'final_table',
}

export enum Position {
  UTG = 'UTG',
  UTG_1 = 'UTG+1',
  UTG_2 = 'UTG+2',
  MP = 'MP',
  CO = 'CO',
  BTN = 'BTN',
  SB = 'SB',
  BB = 'BB',
}

export enum Street {
  PREFLOP = 'preflop',
  FLOP = 'flop',
  TURN = 'turn',
  RIVER = 'river',
}

export enum Action {
  FOLD = 'fold',
  CALL = 'call',
  RAISE = 'raise',
  CHECK = 'check',
  BET = 'bet',
  ALL_IN = 'all_in',
}

export enum SkillLevel {
  BEGINNER = 'beginner',
  INTERMEDIATE = 'intermediate',
  ADVANCED = 'advanced',
  EXPERT = 'expert',
}

export enum Difficulty {
  EASY = 'easy',
  MEDIUM = 'medium',
  HARD = 'hard',
  EXPERT = 'expert',
}

// Request/Response types for API
export interface ScenarioRequest {
  tournament_stage: TournamentStage;
  stack_depth: number;
  game_format: string;
  difficulty: string;
  player_id: string;
  focus_area?: string;
  scenario_type?: string;
}

export interface EvaluationRequest {
  scenario_id: string;
  player_id: string;
  player_action: string;
  player_amount?: number;
  time_taken?: number;
  player_context?: any;
}

export interface SessionStartRequest {
  player_id: string;
  session_goals: string[];
}

export interface SessionSummaryRequest {
  player_id: string;
  session_start: string;
}