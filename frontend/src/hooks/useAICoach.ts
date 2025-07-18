import { useState, useCallback } from 'react';
import { aiCoachAPI } from '@/services/aiCoachAPI';
import { Scenario, Evaluation, ProgressReport } from '@/types/game';

interface ScenarioRequest {
  tournament_stage: string;
  stack_depth: number;
}

export const useAICoach = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getScenario = useCallback(async (request: ScenarioRequest): Promise<Scenario | null> => {
    setLoading(true);
    setError(null);
    try {
      const scenario = await aiCoachAPI.getScenario(request);
      return scenario as Scenario;
    } catch (err: any) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const evaluateDecision = useCallback(async (decision: any): Promise<Evaluation | null> => {
    setLoading(true);
    setError(null);
    try {
      const evaluation = await aiCoachAPI.evaluateDecision(decision);
      return evaluation as Evaluation;
    } catch (err: any) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const getProgressReport = useCallback(async (playerId?: string): Promise<ProgressReport | null> => {
    setLoading(true);
    setError(null);
    try {
      const report = await aiCoachAPI.getProgressReport(playerId);
      return report as ProgressReport;
    } catch (err: any) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    loading,
    error,
    getScenario,
    evaluateDecision,
    getProgressReport,
  };
};