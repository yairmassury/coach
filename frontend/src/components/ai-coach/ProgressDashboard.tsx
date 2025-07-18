import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  TrendingUp, 
  Target, 
  Brain, 
  BarChart3, 
  Award,
  Calendar
} from 'lucide-react';
import { ProgressReport } from '@/types/game';

interface ProgressDashboardProps {
  progress: ProgressReport;
  onStartSession: () => void;
}

const ProgressDashboard: React.FC<ProgressDashboardProps> = ({ 
  progress, 
  onStartSession 
}) => {
  const getSkillLevelColor = (skill: number) => {
    if (skill >= 80) return 'text-green-600';
    if (skill >= 60) return 'text-blue-600';
    if (skill >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getSkillLevelText = (skill: number) => {
    if (skill >= 80) return 'Advanced';
    if (skill >= 60) return 'Intermediate';
    if (skill >= 40) return 'Developing';
    return 'Beginner';
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-4">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Your Poker Progress</h1>
        <p className="text-gray-600">
          Track your improvement and identify areas for growth
        </p>
      </div>

      {/* Overall Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Overall Skill</CardTitle>
            <Brain className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className={`text-2xl font-bold ${getSkillLevelColor(progress.overall_skill)}`}>
              {progress.overall_skill.toFixed(1)}%
            </div>
            <p className="text-xs text-muted-foreground">
              {getSkillLevelText(progress.overall_skill)}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Improvement Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              +{(progress.improvement_rate * 100).toFixed(1)}%
            </div>
            <p className="text-xs text-muted-foreground">
              per session
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Scenarios</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {progress.stats.total_hands}
            </div>
            <p className="text-xs text-muted-foreground">
              {progress.stats.win_rate.toFixed(1)}% accuracy
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Accuracy Trend */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="w-5 h-5" />
            <span>Accuracy Trend</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <span className="text-sm font-medium">Recent Performance:</span>
              <Progress 
                value={progress.stats.win_rate} 
                className="flex-1"
              />
              <span className="text-sm text-gray-600">
                {progress.stats.win_rate.toFixed(1)}%
              </span>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              {progress.stats.accuracy_trend.slice(-4).map((accuracy, index) => (
                <div key={index} className="text-center">
                  <div className="font-semibold">{(accuracy * 100).toFixed(1)}%</div>
                  <div className="text-gray-500">Session {index + 1}</div>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Biggest Leaks */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Target className="w-5 h-5" />
            <span>Areas for Improvement</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {progress.biggest_leaks.map((leak, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-red-50 rounded-lg">
                <div>
                  <h3 className="font-semibold">
                    {leak.type.replace('_', ' ').replace('.', ' - ')}
                  </h3>
                  <p className="text-sm text-gray-600">
                    Impact: {leak.severity}/10
                  </p>
                </div>
                <Badge variant="destructive">
                  Priority #{index + 1}
                </Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Recommended Focus */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Award className="w-5 h-5" />
            <span>Recommended Focus</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="bg-blue-50 p-4 rounded-lg">
              <h3 className="font-semibold mb-2">Next Priority</h3>
              <p className="text-blue-800">
                Focus on improving your {progress.recommended_focus[0]} skills
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {progress.recommended_focus.slice(1).map((focus, index) => (
                <div key={index} className="p-3 border rounded-lg">
                  <h4 className="font-medium">{focus}</h4>
                  <p className="text-sm text-gray-600">
                    Practice scenarios targeting this area
                  </p>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Session Stats */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Calendar className="w-5 h-5" />
            <span>Session Statistics</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">
                {progress.stats.total_hands}
              </div>
              <div className="text-sm text-gray-600">Total Scenarios</div>
            </div>
            
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">
                {Math.round(progress.stats.total_hands * (progress.stats.win_rate / 100))}
              </div>
              <div className="text-sm text-gray-600">Correct Decisions</div>
            </div>
            
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">
                {Math.round(progress.stats.total_hands / 20)}
              </div>
              <div className="text-sm text-gray-600">Sessions Completed</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4">
        <button
          onClick={onStartSession}
          className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg font-semibold"
        >
          Start Practice Session
        </button>
        
        <button
          className="px-8 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 text-lg font-semibold"
        >
          View Detailed Analysis
        </button>
      </div>
    </div>
  );
};

export default ProgressDashboard;