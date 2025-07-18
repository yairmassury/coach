import React from 'react';
import { Evaluation } from '@/types/game';

interface EvaluationFeedbackProps {
  evaluation: Evaluation;
  onNextScenario: () => void;
}

const EvaluationFeedback: React.FC<EvaluationFeedbackProps> = ({ evaluation, onNextScenario }) => (
  <div onClick={onNextScenario}>
    Evaluation Feedback for scenario {evaluation.id}
  </div>
);

export default EvaluationFeedback;