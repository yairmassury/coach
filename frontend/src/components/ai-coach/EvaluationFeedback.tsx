import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, XCircle, AlertCircle, TrendingUp } from 'lucide-react';
import { Evaluation } from '@/types/game';

interface EvaluationFeedbackProps {
  evaluation: Evaluation;
  onNextScenario: () => void;
}

const EvaluationFeedback: React.FC<EvaluationFeedbackProps> = ({ 
  evaluation, 
  onNextScenario 
}) => {
  const getStatusIcon = () => {
    if (evaluation.correct) {
      return <CheckCircle className="w-8 h-8 text-green-500" />;
    } else if (evaluation.severity >= 7) {
      return <XCircle className="w-8 h-8 text-red-500" />;
    } else {
      return <AlertCircle className="w-8 h-8 text-yellow-500" />;
    }
  };

  const getStatusColor = () => {
    if (evaluation.correct) return 'bg-green-50 border-green-200';
    if (evaluation.severity >= 7) return 'bg-red-50 border-red-200';
    return 'bg-yellow-50 border-yellow-200';
  };

  const getSeverityColor = (severity: number) => {
    if (severity >= 7) return 'destructive';
    if (severity >= 4) return 'secondary';
    return 'outline';
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-4">
      {/* Result Header */}
      <Card className={`mb-6 ${getStatusColor()}`}>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {getStatusIcon()}
              <div>
                <h2 className="text-2xl font-bold">
                  {evaluation.correct ? 'Correct Decision!' : 'Learning Opportunity'}
                </h2>
                <p className="text-lg text-gray-600">
                  Your Action: <span className="font-semibold">{evaluation.player_action}</span>
                </p>
              </div>
            </div>
            {!evaluation.correct && (
              <Badge variant={getSeverityColor(evaluation.severity)}>
                Severity: {evaluation.severity}/10
              </Badge>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Optimal Action */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Optimal Play</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold mb-2">Recommended Action</h3>
              <div className="flex items-center space-x-2">
                <Badge variant="outline" className="text-lg px-4 py-2">
                  {evaluation.optimal_action}
                </Badge>
                {evaluation.optimal_amount && (
                  <span className="text-lg">
                    {evaluation.optimal_amount.toLocaleString()} chips
                  </span>
                )}
              </div>
            </div>
            
            {evaluation.ev_difference !== 0 && (
              <div>
                <h3 className="font-semibold mb-2">Expected Value Difference</h3>
                <div className={`text-lg font-bold ${
                  evaluation.ev_difference > 0 ? 'text-green-600' : 'text-red-600'
                }`}>
                  {evaluation.ev_difference > 0 ? '+' : ''}{evaluation.ev_difference.toFixed(2)} BB
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Explanation */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold mb-2">Why This Matters</h3>
              <p className="text-gray-700">{evaluation.explanation}</p>
            </div>
            
            <div>
              <h3 className="font-semibold mb-2">Coaching Tip</h3>
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-blue-800">{evaluation.coaching_tip}</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Leak Analysis */}
      {evaluation.leak_identified && evaluation.leak_identified !== 'none' && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Leak Identified</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2">Pattern Detected</h3>
                <Badge variant="destructive">
                  {evaluation.leak_identified.replace('_', ' ').toUpperCase()}
                </Badge>
              </div>
              
              <div>
                <h3 className="font-semibold mb-2">How to Improve</h3>
                <div className="bg-red-50 p-4 rounded-lg">
                  <p className="text-red-800">
                    Focus on studying this area to plug this leak in your game.
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Key Concepts */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Key Concepts</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {evaluation.improvement_areas.map((concept, index) => (
              <Badge key={index} variant="outline">
                {concept}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Performance Impact */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="w-5 h-5" />
            <span>Performance Impact</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <h3 className="font-semibold mb-2">Short-term Impact</h3>
              <p className="text-sm text-gray-600">
                {evaluation.correct 
                  ? "This decision maximizes your expected value in this situation."
                  : "This decision costs you expected value in similar situations."
                }
              </p>
            </div>
            
            <div>
              <h3 className="font-semibold mb-2">Long-term Development</h3>
              <p className="text-sm text-gray-600">
                {evaluation.correct
                  ? "Keep practicing similar spots to maintain this strength."
                  : "Working on this area will significantly improve your overall game."
                }
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Action Button */}
      <div className="text-center">
        <button
          onClick={onNextScenario}
          className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg font-semibold"
        >
          Next Scenario
        </button>
      </div>
    </div>
  );
};

export default EvaluationFeedback;