export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const APP_CONFIG = {
  name: 'AI Poker Coach',
  version: '1.0.0',
  description: 'AI-powered MTT poker coaching application',
  author: 'Yair Massury',
} as const;

export const POKER_CONSTANTS = {
  POSITIONS: ['UTG', 'UTG+1', 'UTG+2', 'MP', 'CO', 'BTN', 'SB', 'BB'] as const,
  TOURNAMENT_STAGES: ['early', 'middle', 'bubble', 'itm', 'final_table'] as const,
  STREETS: ['preflop', 'flop', 'turn', 'river'] as const,
  ACTIONS: ['fold', 'call', 'raise', 'check', 'bet', 'all_in'] as const,
  SKILL_LEVELS: ['beginner', 'intermediate', 'advanced', 'expert'] as const,
  DIFFICULTY_LEVELS: ['easy', 'medium', 'hard', 'expert'] as const,
} as const;

export const UI_CONFIG = {
  TOAST_DURATION: 4000,
  LOADING_TIMEOUT: 30000,
  DEBOUNCE_DELAY: 300,
  ANIMATION_DURATION: 200,
} as const;

export const GAME_CONFIG = {
  MAX_SCENARIOS_PER_SESSION: 50,
  DEFAULT_STACK_DEPTH: 30,
  DEFAULT_DIFFICULTY: 'intermediate',
  DEFAULT_TOURNAMENT_STAGE: 'middle',
  SESSION_TIMEOUT: 3600000, // 1 hour in milliseconds
} as const;

export const COLORS = {
  PRIMARY: '#3B82F6',
  SECONDARY: '#6B7280',
  SUCCESS: '#10B981',
  WARNING: '#F59E0B',
  ERROR: '#EF4444',
  INFO: '#0EA5E9',
} as const;

export const BREAKPOINTS = {
  SM: 640,
  MD: 768,
  LG: 1024,
  XL: 1280,
  '2XL': 1536,
} as const;