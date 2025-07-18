import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Play, 
  BarChart3, 
  Settings, 
  BookOpen, 
  Target,
  Brain,
  TrendingUp,
  Calendar,
  Award
} from 'lucide-react';
import ProgressDashboard from '@/components/ai-coach/ProgressDashboard';
import { useAICoach } from '@/hooks/useAICoach';
import { ProgressReport } from '@/types/game';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { getProgressReport, loading } = useAICoach();
  const [progressReport, setProgressReport] = useState<ProgressReport | null>(null);
  const [selectedDifficulty, setSelectedDifficulty] = useState('intermediate');
  const [sessionGoals, setSessionGoals] = useState<string[]>([]);

  useEffect(() => {
    loadProgressReport();
  }, []);

  const loadProgressReport = async () => {
    try {
      const report = await getProgressReport('player1');
      setProgressReport(report);
    } catch (error) {
      console.error('Error loading progress report:', error);
    }
  };

  const handleStartSession = () => {
    navigate('/training');
  };

  const handleStartCustomSession = () => {
    navigate('/training', { 
      state: { 
        difficulty: selectedDifficulty,
        goals: sessionGoals 
      } 
    });
  };

  const toggleSessionGoal = (goal: string) => {
    setSessionGoals(prev => 
      prev.includes(goal) 
        ? prev.filter(g => g !== goal)
        : [...prev, goal]
    );
  };

  const availableGoals = [
    'Improve preflop ranges',
    'Practice postflop bet sizing',
    'Master ICM decisions',
    'Work on bubble play',
    'Strengthen final table strategy',
    'Improve bluff frequency',
    'Better pot odds calculation'
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <Brain className="w-8 h-8 text-blue-600" />
              <h1 className="text-2xl font-bold">AI Poker Coach</h1>
            </div>
            
            <div className="flex items-center space-x-4">
              <Button variant="outline" size="sm">
                <Settings className="w-4 h-4 mr-2" />
                Settings
              </Button>
              
              <Button variant="outline" size="sm">
                <BookOpen className="w-4 h-4 mr-2" />
                Study Guide
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Quick Actions */}
          <div className="lg:col-span-1">
            <Card className="mb-6">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Play className="w-5 h-5" />
                  <span>Quick Start</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Button onClick={handleStartSession} className="w-full" size="lg">
                  Start Training Session
                </Button>
                
                <div className="space-y-2">
                  <label className="text-sm font-medium">Difficulty</label>
                  <select 
                    value={selectedDifficulty}
                    onChange={(e) => setSelectedDifficulty(e.target.value)}
                    className="w-full p-2 border rounded-md"
                  >
                    <option value="beginner">Beginner</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </select>
                </div>
                
                <Button 
                  onClick={handleStartCustomSession} 
                  variant="outline" 
                  className="w-full"
                >
                  Custom Session
                </Button>
              </CardContent>
            </Card>

            {/* Session Goals */}
            <Card className="mb-6">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Target className="w-5 h-5" />
                  <span>Session Goals</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {availableGoals.map((goal) => (
                    <div key={goal} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        id={goal}
                        checked={sessionGoals.includes(goal)}
                        onChange={() => toggleSessionGoal(goal)}
                        className="w-4 h-4 text-blue-600 rounded"
                      />
                      <label htmlFor={goal} className="text-sm">
                        {goal}
                      </label>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Recent Activity */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Calendar className="w-5 h-5" />
                  <span>Recent Activity</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Last session</span>
                    <Badge variant="outline">2 hours ago</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Scenarios completed</span>
                    <Badge variant="outline">15</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Accuracy</span>
                    <Badge variant="outline">78%</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Progress Dashboard */}
          <div className="lg:col-span-2">
            {progressReport ? (
              <ProgressDashboard
                progress={progressReport}
                onStartSession={handleStartSession}
              />
            ) : (
              <Card>
                <CardContent className="p-8">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading your progress...</p>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>

        {/* Additional Features */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="w-5 h-5" />
                <span>Analytics</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-4">
                Deep dive into your performance metrics and identify patterns.
              </p>
              <Button variant="outline" className="w-full">
                View Analytics
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="w-5 h-5" />
                <span>Coaching Plan</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-4">
                Get personalized coaching recommendations based on your play.
              </p>
              <Button variant="outline" className="w-full">
                Get Coaching Plan
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Award className="w-5 h-5" />
                <span>Achievements</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-4">
                Track your milestones and unlock new challenges.
              </p>
              <Button variant="outline" className="w-full">
                View Achievements
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;