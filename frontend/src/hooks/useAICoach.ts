import { useState, useCallback } from 'react';
import { AICoachAPI } from '@/services/aiCoachAPI';
import { Scenario, Evaluation, ProgressReport } from '@/types/game';

interface ScenarioRequest {
  tournament_stage: string;
  stack_depth: number;
  difficulty: string;
  player_id: string;
  focus_area?: string;
}

interface EvaluationRequest {
  scenario_id: string;
  action: string;
  player_id: string;
  amount?: number;
  time_taken?: number;
}

export const useAICoach = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentScenario, setCurrentScenario] = useState<Scenario | null>(null);
  const [currentEvaluation, setCurrentEvaluation] = useState<Evaluation | null>(null);

  const handleError = useCallback((err: any) => {
    console.error('AI Coach error:', err);
    setError(err.message || 'An unexpected error occurred');
  }, []);

  const generateScenario = useCallback(async (request: ScenarioRequest): Promise<Scenario> => {
    setLoading(true);
    setError(null);
    
    try {
      const scenario = await AICoachAPI.generateScenario(request);
      setCurrentScenario(scenario);
      return scenario;
    } catch (err) {
      handleError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [handleError]);

  const evaluateDecision = useCallback(async (request: EvaluationRequest): Promise<Evaluation> => {
    setLoading(true);
    setError(null);
    
    try {
      const evaluation = await AICoachAPI.evaluateDecision(request);
      setCurrentEvaluation(evaluation);
      return evaluation;
    } catch (err) {
      handleError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [handleError]);

  const getProgressReport = useCallback(async (playerId: string): Promise<ProgressReport> => {
    setLoading(true);
    setError(null);
    
    try {
      const report = await AICoachAPI.getProgressReport(playerId);
      return report;
    } catch (err) {
      handleError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [handleError]);

  const getCoachingPlan = useCallback(async (playerId: string, goals: string[] = []) => {
    setLoading(true);
    setError(null);
    
    try {
      const plan = await AICoachAPI.getCoachingPlan(playerId, goals);
      return plan;
    } catch (err) {
      handleError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [handleError]);

  const startSession = useCallback(async (playerId: string, goals: string[] = []) => {
    setLoading(true);
    setError(null);
    
    try {
      const session = await AICoachAPI.startSession(playerId, goals);
      return session;
    } catch (err) {
      handleError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [handleError]);

  const getWeaknessAnalysis = useCallback(async (playerId: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const analysis = await AICoachAPI.getWeaknessAnalysis(playerId);
      return analysis;
    } catch (err) {
      handleError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [handleError]);

  const getScenarioRecommendations = useCallback(async (playerId: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const recommendations = await AICoachAPI.getScenarioRecommendations(playerId);
      return recommendations;
    } catch (err) {
      handleError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [handleError]);

  const initializePlayer = useCallback(async (playerId: string, skillLevel: string = 'intermediate') => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await AICoachAPI.initializePlayer(playerId, skillLevel);
      return result;
    } catch (err) {
      handleError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [handleError]);

  const getAdaptiveDifficulty = useCallback(async (playerId: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const difficulty = await AICoachAPI.getAdaptiveDifficulty(playerId);
      return difficulty;
    } catch (err) {
      handleError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [handleError]);

  const getDetailedFeedback = useCallback(async (evaluationId: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const feedback = await AICoachAPI.getDetailedFeedback(evaluationId);
      return feedback;
    } catch (err) {
      handleError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [handleError]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const resetState = useCallback(() => {
    setCurrentScenario(null);
    setCurrentEvaluation(null);
    setError(null);
  }, []);

  return {
    // State
    loading,
    error,
    currentScenario,
    currentEvaluation,
    
    // Actions
    generateScenario,
    evaluateDecision,
    getProgressReport,
    getCoachingPlan,
    startSession,
    getWeaknessAnalysis,
    getScenarioRecommendations,
    initializePlayer,
    getAdaptiveDifficulty,
    getDetailedFeedback,
    
    // Utilities
    clearError,
    resetState,
  };
};

export default useAICoach;