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
              borderColor: value === option.value ? '#646cff' : 'divider',
              background: value === option.value
                ? 'linear-gradient(90deg, #646cff 0%, #747bff 25%, #a855f7 50%, #747bff 75%, #646cff 100%)'
                : 'background.paper',
              color: value === option.value ? '#fff' : 'text.primary',
              cursor: 'pointer',
              transition: 'all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1)',
              textAlign: 'left',
              '&:hover': {
                borderColor: value === option.value ? '#646cff' : '#747bff',
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
    <Box sx={{ display: 'flex', gap: { xs: 0.75, sm: 1.5 }, flexWrap: 'wrap' }}>
      {options.map((option, index) => (
        <Box
          key={option.value}
          onClick={() => onChange(option.value)}
          sx={{
            position: 'relative',
            flex: { xs: '1 1 calc(50% - 6px)', sm: '1 1 calc(33.333% - 12px)' },
            minWidth: { xs: 80, sm: 150 },
            p: { xs: 1.5, sm: 2 },
            borderRadius: 2,
            border: 1,
            borderColor: value === option.value ? '#646cff' : 'divider',
            background: value === option.value
              ? 'linear-gradient(90deg, #646cff 0%, #747bff 25%, #a855f7 50%, #747bff 75%, #646cff 100%)'
              : 'background.paper',
            color: value === option.value ? '#fff' : 'text.primary',
            cursor: 'pointer',
            transition: 'all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1)',
            textAlign: 'left',
            '&:hover': {
              borderColor: value === option.value ? '#646cff' : '#747bff',
              transform: value === option.value ? 'none' : 'translateY(-2px)',
              boxShadow: value === option.value ? 0 : 2,
            },
          }}
        >
          <Typography variant="h6" fontWeight="bold" sx={{ mb: 0.5, fontSize: { xs: '1rem', sm: '1.25rem' } }}>
            {option.label}
          </Typography>
          {option.description && (
            <Typography variant="caption" sx={{ opacity: value === option.value ? 0.9 : 0.7, fontSize: { xs: '0.65rem', sm: '0.75rem' } }}>
              {option.description}
            </Typography>
          )}
        </Box>
      ))}
    </Box>
  );
}
