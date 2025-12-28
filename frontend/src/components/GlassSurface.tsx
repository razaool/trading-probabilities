import React from 'react';
import { Box } from '@mui/material';

interface GlassSurfaceProps {
  children: React.ReactNode;
  sx?: any;
}

export default function GlassSurface({ children, sx }: GlassSurfaceProps) {
  return (
    <>
      <Box
        sx={{
          background: 'rgba(255, 255, 255, 0.05)',
          backdropFilter: 'blur(10px)',
          WebkitBackdropFilter: 'blur(10px)',
          borderRadius: 2,
          border: '1px solid rgba(255, 255, 255, 0.1)',
          ...sx,
        }}
      >
        {children}
      </Box>
      <style>{`
        @media (prefers-color-scheme: light) {
          .glass-surface {
            background: rgba(255, 255, 255, 0.7) !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
          }
        }
      `}</style>
    </>
  );
}
