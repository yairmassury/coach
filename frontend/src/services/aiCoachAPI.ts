import { API_BASE_URL } from '@/config/constants';
import { Scenario, Evaluation, ProgressReport } from '@/types/game';

class AICoachAPI {
  async getScenario(request: any): Promise<Scenario> {
    const response = await fetch(`${API_BASE_URL}/games/scenario/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });
    if (!response.ok) throw new Error('Failed to get scenario');
    return response.json();
  }
  async evaluateDecision(decision: any): Promise<Evaluation> {
    const response = await fetch(`${API_BASE_URL}/games/scenario/evaluate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(decision),
    });
    if (!response.ok) throw new Error('Failed to evaluate decision');
    return response.json();
  }
  async getProgressReport(playerId: string = 'default'): Promise<ProgressReport> {
    const response = await fetch(`${API_BASE_URL}/ai/progress/${playerId}`);
    if (!response.ok) throw new Error('Failed to get progress report');
    return response.json();
  }
}

export const aiCoachAPI = new AICoachAPI();