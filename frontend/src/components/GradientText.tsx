import React from 'react';

interface GradientTextProps {
  children: React.ReactNode;
  className?: string;
}

export default function GradientText({ children, className }: GradientTextProps) {
  return (
    <>
      <span className={`shimmer-text ${className || ''}`}>{children}</span>
      <style>{`
        .shimmer-text {
          background: linear-gradient(
            90deg,
            #646cff 0%,
            #747bff 25%,
            #a855f7 50%,
            #747bff 75%,
            #646cff 100%
          );
          background-size: 200% auto;
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          animation: shimmer 3s linear infinite;
          display: inline-block;
        }

        @keyframes shimmer {
          0% {
            background-position: -200% center;
          }
          100% {
            background-position: 200% center;
          }
        }
      `}</style>
    </>
  );
}
