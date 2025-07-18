import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Play, BarChart3, Brain } from 'lucide-react';
import ProgressDashboard from '@/components/ai-coach/ProgressDashboard';
import { useAICoach } from '@/hooks/useAICoach';
import { ProgressReport } from '@/types/game';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { loading, error, getProgressReport } = useAICoach();
  const [progress, setProgress] = useState<ProgressReport | null>(null);

  const loadProgressReport = React.useCallback(async () => {
    const report = await getProgressReport('default');  // Replace with actual player ID
    if (report) {
      setProgress(report);
    }
  }, [getProgressReport]);

  useEffect(() => {
    loadProgressReport();
  }, [loadProgressReport]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!progress) return <div>No progress report available.</div>;

  return (
    <div>
      <h1>Dashboard</h1>
      <ProgressDashboard onStartSession={() => navigate('/training')} />
      <Button onClick={() => navigate('/training')}>
        <Play /> Start Training
      </Button>
      <Button onClick={() => navigate('/analysis')}>
        <BarChart3 /> View Analysis
      </Button>
      <Card>
        <CardHeader>
          <CardTitle>
            <Brain /> Skill Level
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p>{progress.overall_skill}%</p>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;