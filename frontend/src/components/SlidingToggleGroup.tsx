import React, { useRef, useEffect } from 'react';
import { Box, Typography } from '@mui/material';

interface SlidingToggleGroupProps {
  value: string;
  onChange: (value: string) => void;
  options: { value: string; label: string }[];
}

export default function SlidingToggleGroup({ value, onChange, options }: SlidingToggleGroupProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [position, setPosition] = React.useState({ left: 0, width: 0 });

  useEffect(() => {
    if (!containerRef.current) return;

    const container = containerRef.current;
    const selectedIndex = options.findIndex((opt) => opt.value === value);
    const selectedChild = container.children[selectedIndex + 1] as HTMLElement; // +1 to skip the sliding background div

    if (selectedChild) {
      setPosition({
        left: selectedChild.offsetLeft,
        width: selectedChild.offsetWidth,
      });
    }

    // Recalculate on window resize and orientation change
    const handleResize = () => {
      if (!containerRef.current) return;
      const updatedContainer = containerRef.current;
      const updatedIndex = options.findIndex((opt) => opt.value === value);
      const updatedChild = updatedContainer.children[updatedIndex + 1] as HTMLElement;

      if (updatedChild) {
        setPosition({
          left: updatedChild.offsetLeft,
          width: updatedChild.offsetWidth,
        });
      }
    };

    window.addEventListener('resize', handleResize);
    window.addEventListener('orientationchange', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('orientationchange', handleResize);
    };
  }, [value, options]);

  return (
    <>
      <Box
        ref={containerRef}
        sx={{
          position: 'relative',
          display: 'inline-flex',
          bgcolor: 'background.paper',
          borderRadius: 2,
          p: 0.5,
          border: 1,
          borderColor: 'divider',
          gap: 0.5,
          width: { xs: '100%', sm: 'auto' },
        }}
      >
        {/* Sliding background */}
        <Box
          sx={{
            position: 'absolute',
            top: 4,
            left: position.left,
            width: position.width,
            height: 'calc(100% - 8px)',
            bgcolor: 'primary.main',
            borderRadius: 1.5,
            transition: 'all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1)',
            zIndex: 0,
          }}
        />

        {options.map((option, index) => {
          const isSelected = value === option.value;
          return (
            <Box
              key={option.value}
              onClick={() => onChange(option.value)}
              sx={{
                position: 'relative',
                zIndex: 1,
                flex: 1,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                px: { xs: 0.75, sm: 1.5 },
                py: 1,
                cursor: 'pointer',
                userSelect: 'none',
                transition: 'color 0.3s cubic-bezier(0.4, 0.0, 0.2, 1)',
                color: isSelected ? 'primary.contrastText' : 'text.primary',
                fontWeight: isSelected ? 600 : 400,
                fontSize: { xs: '0.65rem', sm: '0.75rem', md: '0.8rem' },
                whiteSpace: 'nowrap',
                borderRadius: 1.5,
                minWidth: 0,
              }}
            >
              {option.label}
            </Box>
          );
        })}
      </Box>
    </>
  );
}
