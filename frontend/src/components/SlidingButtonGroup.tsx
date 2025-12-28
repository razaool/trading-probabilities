import React from 'react';
import { Box, Typography } from '@mui/material';

interface SlidingButtonGroupProps {
  value: string;
  onChange: (value: string) => void;
  options: { value: string; label: string; description?: string }[];
  orientation?: 'horizontal' | 'vertical';
}

export default function SlidingButtonGroup({
  value,
  onChange,
  options,
  orientation = 'horizontal'
}: SlidingButtonGroupProps) {
  const selectedIndex = options.findIndex((opt) => opt.value === value);

  if (orientation === 'vertical') {
    return (
      <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
        {options.map((option, index) => (
          <Box
            key={option.value}
            onClick={() => onChange(option.value)}
            sx={{
              position: 'relative',
              p: 2,
              borderRadius: 2,
              border: 1,
              borderColor: value === option.value ? 'primary.main' : 'divider',
              bgcolor: value === option.value ? 'primary.main' : 'background.paper',
              color: value === option.value ? 'primary.contrastText' : 'text.primary',
              cursor: 'pointer',
              transition: 'all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1)',
              textAlign: 'left',
              '&:hover': {
                borderColor: value === option.value ? 'primary.main' : 'primary.light',
                transform: value === option.value ? 'none' : 'translateX(4px)',
              },
            }}
          >
            <Typography variant="h6" fontWeight="bold" sx={{ mb: 0.5 }}>
              {option.label}
            </Typography>
            {option.description && (
              <Typography variant="caption" sx={{ opacity: value === option.value ? 0.9 : 0.7 }}>
                {option.description}
              </Typography>
            )}
          </Box>
        ))}
      </Box>
    );
  }

  // Horizontal layout
  return (
    <Box sx={{ display: 'flex', gap: 1.5, flexWrap: 'wrap' }}>
      {options.map((option, index) => (
        <Box
          key={option.value}
          onClick={() => onChange(option.value)}
          sx={{
            position: 'relative',
            flex: '1 1 calc(33.333% - 12px)',
            minWidth: 150,
            p: 2,
            borderRadius: 2,
            border: 1,
            borderColor: value === option.value ? 'primary.main' : 'divider',
            bgcolor: value === option.value ? 'primary.main' : 'background.paper',
            color: value === option.value ? 'primary.contrastText' : 'text.primary',
            cursor: 'pointer',
            transition: 'all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1)',
            textAlign: 'left',
            '&:hover': {
              borderColor: value === option.value ? 'primary.main' : 'primary.light',
              transform: value === option.value ? 'none' : 'translateY(-2px)',
              boxShadow: value === option.value ? 0 : 2,
            },
          }}
        >
          <Typography variant="h6" fontWeight="bold" sx={{ mb: 0.5 }}>
            {option.label}
          </Typography>
          {option.description && (
            <Typography variant="caption" sx={{ opacity: value === option.value ? 0.9 : 0.7 }}>
              {option.description}
            </Typography>
          )}
        </Box>
      ))}
    </Box>
  );
}
