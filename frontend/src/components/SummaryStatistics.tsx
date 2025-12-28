import React from 'react';
import {
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Box,
  Chip,
} from '@mui/material';
import type { QueryResponse, SummaryStatistics } from '../types/api';

interface SummaryStatisticsProps {
  data: QueryResponse;
}

function formatPercentage(value: number | null | undefined): string {
  if (value === null || value === undefined) {
    return 'N/A';
  }
  return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
}

function formatWinRate(value: number | null | undefined): string {
  if (value === null || value === undefined) {
    return 'N/A';
  }
  return `${(value * 100).toFixed(1)}%`;
}

function getColorForValue(value: number | null | undefined, isWinRate: boolean = false): string {
  if (value === null || value === undefined) return 'inherit';
  if (isWinRate) {
    return value >= 0.5 ? '#2e7d32' : '#d32f2f';
  }
  return value >= 0 ? '#2e7d32' : '#d32f2f';
}

export default function SummaryStatistics({ data }: SummaryStatisticsProps) {
  const horizonOrder = ['1d', '1w', '1m', '1y'];
  const horizons = horizonOrder.filter(h => h in data.summary_statistics);

  const horizonLabels: Record<string, string> = {
    '1d': '+1D',
    '1w': '+1W',
    '1m': '+1M',
    '1y': '+1Y',
  };

  return (
    <Paper
      elevation={0}
      sx={{
        p: { xs: 2, sm: 3 },
        mt: 2,
        background: 'rgba(255, 255, 255, 0.03)',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        borderRadius: 2,
        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: '0 8px 24px rgba(0, 0, 0, 0.15)',
        },
      }}
    >
      <Box sx={{ mb: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, fontSize: { xs: '1.1rem', sm: '1.25rem' } }}>
          Summary Statistics
        </Typography>
      </Box>
      <Typography variant="body2" color="text.secondary" gutterBottom sx={{ fontStyle: 'italic', fontSize: { xs: '0.75rem', sm: '0.875rem' } }}>
        {data.condition}
      </Typography>

      <TableContainer sx={{ mt: { xs: 2, sm: 3 }, overflowX: 'auto' }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell
                sx={{
                  borderBottom: '2px solid',
                  borderColor: 'divider',
                  fontWeight: 600,
                  color: 'text.primary',
                  fontSize: { xs: '0.7rem', sm: '0.875rem' },
                  padding: { xs: '6px 4px', sm: '16px' },
                }}
              >
                Metric
              </TableCell>
              {horizons.map((horizon) => (
                <TableCell
                  key={horizon}
                  align="center"
                  sx={{
                    borderBottom: '2px solid',
                    borderColor: 'divider',
                    fontWeight: 600,
                    color: 'text.primary',
                    fontSize: { xs: '0.7rem', sm: '0.875rem' },
                    padding: { xs: '6px 4px', sm: '16px' },
                  }}
                >
                  {horizonLabels[horizon] || horizon.toUpperCase()}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow
              sx={{
                transition: 'background-color 0.2s ease',
                '&:hover': {
                  bgcolor: 'rgba(0, 0, 0, 0.04)',
                },
              }}
            >
              <TableCell sx={{ fontWeight: 500, fontSize: { xs: '0.7rem', sm: '0.875rem' }, padding: { xs: '6px 4px', sm: '16px' } }}>Average Return</TableCell>
              {horizons.map((horizon) => {
                const stats = data.summary_statistics[horizon];
                return (
                  <TableCell key={horizon} align="center" sx={{ padding: { xs: '6px 4px', sm: '16px' } }}>
                    <Box
                      sx={{
                        color: getColorForValue(stats.mean),
                        fontWeight: 700,
                        fontSize: { xs: '0.8rem', sm: '1rem' },
                      }}
                    >
                      {formatPercentage(stats.mean)}
                    </Box>
                  </TableCell>
                );
              })}
            </TableRow>

            <TableRow
              sx={{
                transition: 'background-color 0.2s ease',
                '&:hover': {
                  bgcolor: 'rgba(0, 0, 0, 0.04)',
                },
              }}
            >
              <TableCell sx={{ fontWeight: 500, fontSize: { xs: '0.7rem', sm: '0.875rem' }, padding: { xs: '6px 4px', sm: '16px' } }}>Win Rate</TableCell>
              {horizons.map((horizon) => {
                const stats = data.summary_statistics[horizon];
                return (
                  <TableCell key={horizon} align="center" sx={{ padding: { xs: '6px 4px', sm: '16px' } }}>
                    <Box
                      sx={{
                        color: getColorForValue(stats.win_rate, true),
                        fontWeight: 700,
                        fontSize: { xs: '0.8rem', sm: '1rem' },
                      }}
                    >
                      {formatWinRate(stats.win_rate)}
                    </Box>
                  </TableCell>
                );
              })}
            </TableRow>

            <TableRow
              sx={{
                transition: 'background-color 0.2s ease',
                '&:hover': {
                  bgcolor: 'rgba(0, 0, 0, 0.04)',
                },
              }}
            >
              <TableCell sx={{ fontSize: { xs: '0.7rem', sm: '0.875rem' }, padding: { xs: '6px 4px', sm: '16px' } }}>Median Return</TableCell>
              {horizons.map((horizon) => {
                const stats = data.summary_statistics[horizon];
                return (
                  <TableCell key={horizon} align="center" sx={{ fontWeight: 500, fontSize: { xs: '0.75rem', sm: '0.875rem' }, padding: { xs: '6px 4px', sm: '16px' } }}>
                    {formatPercentage(stats.median)}
                  </TableCell>
                );
              })}
            </TableRow>

            <TableRow
              sx={{
                transition: 'background-color 0.2s ease',
                '&:hover': {
                  bgcolor: 'rgba(0, 0, 0, 0.04)',
                },
              }}
            >
              <TableCell sx={{ fontSize: { xs: '0.7rem', sm: '0.875rem' }, padding: { xs: '6px 4px', sm: '16px' } }}>Best / Worst</TableCell>
              {horizons.map((horizon) => {
                const stats = data.summary_statistics[horizon];
                return (
                  <TableCell key={horizon} align="center" sx={{ fontSize: { xs: '0.7rem', sm: '0.85rem' }, padding: { xs: '6px 4px', sm: '16px' } }}>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.25 }}>
                      <Box sx={{ color: '#2e7d32', fontWeight: 500, fontSize: { xs: '0.65rem', sm: '0.75rem' } }}>{formatPercentage(stats.max)}</Box>
                      <Box sx={{ color: '#d32f2f', fontWeight: 500, fontSize: { xs: '0.65rem', sm: '0.75rem' } }}>{formatPercentage(stats.min)}</Box>
                    </Box>
                  </TableCell>
                );
              })}
            </TableRow>

            <TableRow
              sx={{
                transition: 'background-color 0.2s ease',
                '&:hover': {
                  bgcolor: 'rgba(0, 0, 0, 0.04)',
                },
              }}
            >
              <TableCell sx={{ fontSize: { xs: '0.7rem', sm: '0.875rem' }, padding: { xs: '6px 4px', sm: '16px' } }}>Std Deviation</TableCell>
              {horizons.map((horizon) => {
                const stats = data.summary_statistics[horizon];
                return (
                  <TableCell key={horizon} align="center" sx={{ fontSize: { xs: '0.75rem', sm: '0.875rem' }, padding: { xs: '6px 4px', sm: '16px' } }}>
                    {formatPercentage(stats.std)}
                  </TableCell>
                );
              })}
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}
