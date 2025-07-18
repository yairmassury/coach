import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Loader2, ArrowLeft, Settings } from 'lucide-react';
import ScenarioDisplay from '@/components/game/ScenarioDisplay';
import EvaluationFeedback from '@/components/ai-coach/EvaluationFeedback';
import { useAICoach } from '@/hooks/useAICoach';
import { Scenario, Evaluation } from '@/types/game';

const ScenarioTraining: React.FC = () => {
  const navigate = useNavigate();
  const { 
    generateScenario, 
    evaluateDecision, 
    loading, 
    error 
  } = useAICoach();
  
  const [currentScenario, setCurrentScenario] = useState<Scenario | null>(null);
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [sessionStats, setSessionStats] = useState({
    scenariosCompleted: 0,
    correctDecisions: 0,
    sessionStartTime: Date.now()
  });
  const [showEvaluation, setShowEvaluation] = useState(false);
  
  // Load initial scenario
  useEffect(() => {
    loadNextScenario();
  }, []);

  const loadNextScenario = async () => {
    try {
      setShowEvaluation(false);
      setEvaluation(null);
      
      const scenario = await generateScenario({
        tournament_stage: 'middle',
        stack_depth: 30,
        difficulty: 'intermediate',
        player_id: 'player1'
      });
      
      setCurrentScenario(scenario);
    } catch (error) {
      console.error('Error loading scenario:', error);
    }
  };

  const handleAction = async (action: string, amount?: number) => {
    if (!currentScenario) return;
    
    try {
      const startTime = Date.now();
      
      const evaluationResult = await evaluateDecision({
        scenario_id: currentScenario.id,
        action,
        player_id: 'player1',
        amount,
        time_taken: (Date.now() - startTime) / 1000
      });
      
      setEvaluation(evaluationResult);
      setShowEvaluation(true);
      
      // Update session stats
      setSessionStats(prev => ({
        ...prev,
        scenariosCompleted: prev.scenariosCompleted + 1,
        correctDecisions: prev.correctDecisions + (evaluationResult.correct ? 1 : 0)
      }));
      
    } catch (error) {
      console.error('Error evaluating decision:', error);
    }
  };

  const handleNextScenario = () => {
    loadNextScenario();
  };

  const handleEndSession = () => {
    navigate('/dashboard');
  };

  const getAccuracyRate = () => {
    if (sessionStats.scenariosCompleted === 0) return 0;
    return Math.round((sessionStats.correctDecisions / sessionStats.scenariosCompleted) * 100);
  };

  const getSessionDuration = () => {
    const durationMs = Date.now() - sessionStats.sessionStartTime;
    const minutes = Math.floor(durationMs / 60000);
    return minutes;
  };

  if (loading && !currentScenario) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading scenario...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle className="text-red-600">Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600 mb-4">{error}</p>
            <Button onClick={loadNextScenario} className="w-full">
              Try Again
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => navigate('/dashboard')}
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Dashboard
              </Button>
              <h1 className="text-xl font-semibold">MTT Training</h1>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Badge variant="outline">
                  {sessionStats.scenariosCompleted} scenarios
                </Badge>
                <Badge variant="outline">
                  {getAccuracyRate()}% accuracy
                </Badge>
                <Badge variant="outline">
                  {getSessionDuration()} min
                </Badge>
              </div>
              
              <Button variant="outline" size="sm">
                <Settings className="w-4 h-4 mr-2" />
                Settings
              </Button>
              
              <Button variant="outline" size="sm" onClick={handleEndSession}>
                End Session
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
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
          <div className="text-center">
            <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4" />
            <p className="text-gray-600">Loading scenario...</p>
          </div>
        )}
      </div>

      {/* Loading Overlay */}
      {loading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg">
            <div className="flex items-center space-x-3">
              <Loader2 className="w-6 h-6 animate-spin" />
              <span>Processing...</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ScenarioTraining;