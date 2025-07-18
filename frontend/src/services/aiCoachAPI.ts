import { API_BASE_URL } from '@/config/constants';
import { Scenario, Evaluation, ProgressReport } from '@/types/game';

class AICoachAPIService {
  private baseURL: string;

  constructor() {
    this.baseURL = API_BASE_URL || 'http://localhost:8000/api';
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error(`API request failed: ${endpoint}`, error);
      throw error;
    }
  }

  async generateScenario(params: {
    tournament_stage: string;
    stack_depth: number;
    difficulty: string;
    player_id: string;
    focus_area?: string;
  }): Promise<Scenario> {
    const queryParams = new URLSearchParams({
      game_type: 'MTT',
      tournament_stage: params.tournament_stage,
      stack_depth: params.stack_depth.toString(),
      player_id: params.player_id,
      difficulty: params.difficulty,
      ...(params.focus_area && { focus_area: params.focus_area }),
    });

    return this.request<Scenario>(`/ai/scenario?${queryParams}`, {
      method: 'POST',
    });
  }

  async evaluateDecision(params: {
    scenario_id: string;
    action: string;
    player_id: string;
    amount?: number;
    time_taken?: number;
  }): Promise<Evaluation> {
    const queryParams = new URLSearchParams({
      scenario_id: params.scenario_id,
      action: params.action,
      player_id: params.player_id,
      ...(params.amount !== undefined && { amount: params.amount.toString() }),
      ...(params.time_taken !== undefined && { time_taken: params.time_taken.toString() }),
    });

    return this.request<Evaluation>(`/ai/evaluate?${queryParams}`, {
      method: 'POST',
    });
  }

  async getProgressReport(playerId: string): Promise<ProgressReport> {
    return this.request<ProgressReport>(`/ai/progress/${playerId}`);
  }

  async getCoachingPlan(playerId: string, sessionGoals: string[] = []): Promise<any> {
    const queryParams = new URLSearchParams();
    sessionGoals.forEach(goal => queryParams.append('session_goals', goal));

    return this.request<any>(`/ai/coaching-plan/${playerId}?${queryParams}`);
  }

  async startSession(playerId: string, sessionGoals: string[] = []): Promise<any> {
    return this.request<any>('/ai/coaching-session/start', {
      method: 'POST',
      body: JSON.stringify({
        player_id: playerId,
        session_goals: sessionGoals,
      }),
    });
  }

  async getWeaknessAnalysis(playerId: string): Promise<any> {
    return this.request<any>(`/ai/weakness-analysis/${playerId}`);
  }

  async getPlayerContext(playerId: string): Promise<any> {
    return this.request<any>(`/ai/player-context/${playerId}`);
  }

  async initializePlayer(playerId: string, skillLevel: string = 'intermediate'): Promise<any> {
    return this.request<any>(`/ai/player-context/${playerId}/initialize`, {
      method: 'POST',
      body: JSON.stringify({
        skill_level: skillLevel,
      }),
    });
  }

  async getScenarioRecommendations(playerId: string): Promise<any> {
    return this.request<any>(`/ai/scenario-recommendations/${playerId}`);
  }

  async getAdaptiveDifficulty(playerId: string): Promise<any> {
    return this.request<any>(`/games/difficulty/adaptive/${playerId}`);
  }

  async getDetailedFeedback(evaluationId: string): Promise<any> {
    return this.request<any>('/ai/feedback/detailed', {
      method: 'POST',
      body: JSON.stringify({
        evaluation_id: evaluationId,
      }),
    });
  }

  async getGlobalStats(): Promise<any> {
    return this.request<any>('/ai/stats/global');
  }

  async healthCheck(): Promise<any> {
    return this.request<any>('/ai/health');
  }

  // Game API endpoints (legacy compatibility)
  async getPlayerStats(playerId: string): Promise<any> {
    return this.request<any>(`/games/player/${playerId}/stats`);
  }

  async getPlayerScenarios(playerId: string, limit: number = 10, offset: number = 0): Promise<any> {
    return this.request<any>(`/games/player/${playerId}/scenarios?limit=${limit}&offset=${offset}`);
  }

  async getPlayerEvaluations(playerId: string, limit: number = 10, offset: number = 0): Promise<any> {
    return this.request<any>(`/games/player/${playerId}/evaluations?limit=${limit}&offset=${offset}`);
  }

  async startGameSession(playerId: string, sessionGoals: string[] = []): Promise<any> {
    return this.request<any>('/games/session/start', {
      method: 'POST',
      body: JSON.stringify({
        player_id: playerId,
        session_goals: sessionGoals,
      }),
    });
  }

  async getSessionSummary(playerId: string, sessionStart: string): Promise<any> {
    return this.request<any>('/games/session/summary', {
      method: 'POST',
      body: JSON.stringify({
        player_id: playerId,
        session_start: sessionStart,
      }),
    });
  }
}

export const AICoachAPI = new AICoachAPIService();
export default AICoachAPI;