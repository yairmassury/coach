import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
import ScenarioDisplay from '@/components/game/ScenarioDisplay';
import EvaluationFeedback from '@/components/ai-coach/EvaluationFeedback';
import { useAICoach } from '@/hooks/useAICoach';
import { Scenario, Evaluation } from '@/types/game';

const ScenarioTraining: React.FC = () => {
  const navigate = useNavigate();
  const { loading, error, getScenario, evaluateDecision } = useAICoach();
  const [currentScenario, setCurrentScenario] = useState<Scenario | null>(null);
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [showEvaluation, setShowEvaluation] = useState(false);

  const loadNextScenario = React.useCallback(async () => {
    setShowEvaluation(false);
    setEvaluation(null);
    const scenario = await getScenario({ tournament_stage: 'middle', stack_depth: 50 });
    if (scenario) {
      setCurrentScenario(scenario);
    }
  }, [getScenario]);

  useEffect(() => {
    loadNextScenario();
  }, [loadNextScenario]);

  const handleAction = async (action: string, amount?: number) => {
    if (!currentScenario) return;
    const result = await evaluateDecision({
      scenario_id: currentScenario.id,
      action,
      amount,
    });
    if (result) {
      setEvaluation(result);
      setShowEvaluation(true);
    }
  };

  const handleNextScenario = () => {
    loadNextScenario();
  };

  if (loading && !currentScenario) return <div>Loading scenario...</div>;

  if (error) {
    return (
      <div>
        <Card>
          <CardHeader>
            <CardTitle>Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p>{error}</p>
            <Button onClick={loadNextScenario}>Try Again</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div>
      <Button onClick={() => navigate('/dashboard')}>
        <ArrowLeft /> Back to Dashboard
      </Button>
      {showEvaluation && evaluation ? (
        <EvaluationFeedback
          evaluation={evaluation}
          onNextScenario={handleNextScenario}
        />
      ) : currentScenario ? (
        <ScenarioDisplay
          scenario={currentScenario}
          onAction={handleAction}
        />
      ) : (
        <div>No scenario loaded.</div>
      )}
    </div>
  );
};

export default ScenarioTraining;