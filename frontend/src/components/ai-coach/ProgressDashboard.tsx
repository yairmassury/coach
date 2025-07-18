import React from 'react';

const ProgressDashboard = ({ onStartSession }: { onStartSession: () => void }) => (
  <div onClick={onStartSession}>Progress Dashboard</div>
);

export default ProgressDashboard;