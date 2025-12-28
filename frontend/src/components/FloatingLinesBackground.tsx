import React from 'react';

export default function FloatingLinesBackground() {
  return (
    <>
      <div className="floating-lines-background">
        <div className="line line-1"></div>
        <div className="line line-2"></div>
        <div className="line line-3"></div>
        <div className="line line-4"></div>
        <div className="line line-5"></div>
      </div>
      <style>{`
        .floating-lines-background {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          pointer-events: none;
          z-index: -1;
          overflow: hidden;
        }

        .line {
          position: absolute;
          width: 1px;
          height: 100%;
          background: linear-gradient(
            to bottom,
            transparent,
            rgba(100, 108, 255, 0.1),
            transparent
          );
          animation: float 20s ease-in-out infinite;
        }

        .line-1 {
          left: 10%;
          animation-delay: 0s;
        }

        .line-2 {
          left: 30%;
          animation-delay: -4s;
        }

        .line-3 {
          left: 50%;
          animation-delay: -8s;
        }

        .line-4 {
          left: 70%;
          animation-delay: -12s;
        }

        .line-5 {
          left: 90%;
          animation-delay: -16s;
        }

        @keyframes float {
          0%, 100% {
            transform: translateY(-100%);
            opacity: 0;
          }
          10% {
            opacity: 1;
          }
          90% {
            opacity: 1;
          }
          100% {
            transform: translateY(100%);
            opacity: 0;
          }
        }

        @media (prefers-color-scheme: light) {
          .line {
            background: linear-gradient(
              to bottom,
              transparent,
              rgba(100, 108, 255, 0.15),
              transparent
            );
          }
        }
      `}</style>
    </>
  );
}
