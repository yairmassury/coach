import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export const Card = ({ children, className, ...props }: CardProps) => (
  <div className={`card ${className}`} {...props}>{children}</div>
);

export const CardContent = ({ children, className, ...props }: CardProps) => (
  <div className={`card-content ${className}`} {...props}>{children}</div>
);

export const CardHeader = ({ children, className, ...props }: CardProps) => (
  <div className={`card-header ${className}`} {...props}>{children}</div>
);

export const CardTitle = ({ children, className, ...props }: CardProps) => (
  <h2 className={`card-title ${className}`} {...props}>{children}</h2>
); 