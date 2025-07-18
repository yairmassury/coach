import React from 'react';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  children: React.ReactNode;
  variant?: 'outline';
}

export const Badge = ({ children, className, ...props }: BadgeProps) => (
  <span className={`badge ${className}`} {...props}>{children}</span>
); 