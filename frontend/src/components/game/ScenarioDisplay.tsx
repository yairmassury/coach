import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Scenario } from '@/types/game';

interface ScenarioDisplayProps {
  scenario: Scenario;
  onAction: (action: string, amount?: number) => void;
}

const ScenarioDisplay: React.FC<ScenarioDisplayProps> = ({ scenario, onAction }) => {
  return (
    <div className="w-full max-w-4xl mx-auto p-4">
      {/* Tournament Info */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-4">
          <div>
            <Badge variant="outline" className="mb-2">
              {scenario.tournament_stage.toUpperCase()}
            </Badge>
            <h2 className="text-2xl font-bold">MTT Scenario</h2>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-600">
              {scenario.players_remaining} players remaining
            </p>
            <p className="text-sm text-gray-600">
              Blinds: {scenario.blinds.small}/{scenario.blinds.big}
              {scenario.ante > 0 && ` (${scenario.ante})`}
            </p>
          </div>
        </div>
      </div>

      {/* Poker Table */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Table Situation</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Board and Pot */}
            <div>
              <div className="mb-4">
                <h3 className="font-semibold mb-2">Board</h3>
                <div className="flex space-x-2">
                  {scenario.board.length > 0 ? (
                    scenario.board.map((card, index) => (
                      <div
                        key={index}
                        className="w-12 h-16 bg-white border-2 border-gray-300 rounded-lg flex items-center justify-center text-sm font-bold"
                      >
                        {card}
                      </div>
                    ))
                  ) : (
                    <div className="text-gray-500">Preflop</div>
                  )}
                </div>
              </div>
              <div className="mb-4">
                <h3 className="font-semibold mb-2">Pot Size</h3>
                <div className="text-2xl font-bold text-green-600">
                  {scenario.pot_size.toLocaleString()} chips
                </div>
              </div>
            </div>

            {/* Hero Info */}
            <div>
              <div className="mb-4">
                <h3 className="font-semibold mb-2">Your Position</h3>
                <Badge variant="secondary">{scenario.hero_position}</Badge>
              </div>
              <div className="mb-4">
                <h3 className="font-semibold mb-2">Your Cards</h3>
                <div className="flex space-x-2">
                  {scenario.hero_cards.map((card, index) => (
                    <div
                      key={index}
                      className="w-12 h-16 bg-blue-100 border-2 border-blue-300 rounded-lg flex items-center justify-center text-sm font-bold"
                    >
                      {card}
                    </div>
                  ))}
                </div>
              </div>
              <div className="mb-4">
                <h3 className="font-semibold mb-2">Your Stack</h3>
                <div className="text-xl font-bold">
                  {scenario.hero_stack.toLocaleString()} chips
                </div>
                <div className="text-sm text-gray-600">
                  ({Math.floor(scenario.hero_stack / scenario.blinds.big)} BB)
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Action History */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Action History</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {scenario.action_history.map((action, index) => (
              <div key={index} className="text-sm">
                {action}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Villains */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Opponents</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {scenario.villain_positions.map((villain, index) => (
              <div key={index} className="border rounded-lg p-3">
                <div className="font-semibold">{villain.position}</div>
                <div className="text-sm text-gray-600">
                  Stack: {villain.stack.toLocaleString()} chips
                </div>
                <div className="text-sm text-gray-600">
                  Type: {villain.player_type}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Action Required */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Action Required</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="mb-4">
            <p className="text-lg">{scenario.scenario_description}</p>
          </div>
          
          {scenario.to_call > 0 && (
            <div className="mb-4">
              <p className="text-lg font-semibold">
                To Call: {scenario.to_call.toLocaleString()} chips
              </p>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex space-x-4">
            {scenario.valid_actions.map((action) => (
              <button
                key={action}
                onClick={() => onAction(action)}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {action.toUpperCase()}
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Learning Objectives */}
      <Card>
        <CardHeader>
          <CardTitle>Learning Objectives</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {scenario.learning_objectives.map((objective, index) => (
              <div key={index} className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span className="text-sm">{objective}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ScenarioDisplay;