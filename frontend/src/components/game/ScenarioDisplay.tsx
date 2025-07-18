import React from 'react';
import { Scenario } from '@/types/game';

interface ScenarioDisplayProps {
  scenario: Scenario;
  onAction: (action: string, amount?: number) => void;
}

const ScenarioDisplay: React.FC<ScenarioDisplayProps> = ({ scenario, onAction }) => (
  <div onClick={() => onAction('fold')}>
    Scenario Display for scenario {scenario.id}
  </div>
);

export default ScenarioDisplay;