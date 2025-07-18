import React from 'react';

interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value: number;
}

export const Progress = ({ value, className, ...props }: ProgressProps) => (
  <div className={`progress-bar ${className}`} {...props}>
    <div style={{ width: `${value}%` }} className="progress" />
  </div>
); 