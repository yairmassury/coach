import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: 'ghost' | 'outline';
  size?: 'sm';
}

export const Button = ({ children, className, ...props }: ButtonProps) => (
  <button className={`button ${className}`} {...props}>{children}</button>
); 