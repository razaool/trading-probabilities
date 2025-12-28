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
  // Define the correct chronological order for timeframes
  const horizonOrder = ['1d', '1w', '1m', '1y'];
  const horizons = horizonOrder.filter(h => h in data.summary_statistics);

  const horizonLabels: Record<string, string> = {
    '1d': '+1D',
    '1w': '+1W',
    '1m': '+1M',
    '1y': '+1Y',
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Summary Statistics
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        {data.condition} - {data.total_occurrences} instances found
      </Typography>

      <TableContainer sx={{ mt: 2 }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Metric</TableCell>
              {horizons.map((horizon) => (
                <TableCell key={horizon} align="center">
                  <strong>{horizonLabels[horizon] || horizon.toUpperCase()}</strong>
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell><strong>Average Return</strong></TableCell>
              {horizons.map((horizon) => {
                const stats = data.summary_statistics[horizon];
                return (
                  <TableCell key={horizon} align="center">
                    <Box
                      sx={{
                        color: getColorForValue(stats.mean),
                        fontWeight: 'bold',
                      }}
                    >
                      {formatPercentage(stats.mean)}
                    </Box>
                  </TableCell>
                );
              })}
            </TableRow>

            <TableRow>
              <TableCell>Win Rate</TableCell>
              {horizons.map((horizon) => {
                const stats = data.summary_statistics[horizon];
                return (
                  <TableCell key={horizon} align="center">
                    <Box
                      sx={{
                        color: getColorForValue(stats.win_rate, true),
                        fontWeight: 'bold',
                      }}
                    >
                      {formatWinRate(stats.win_rate)}
                    </Box>
                  </TableCell>
                );
              })}
            </TableRow>

            <TableRow>
              <TableCell>Median Return</TableCell>
              {horizons.map((horizon) => {
                const stats = data.summary_statistics[horizon];
                return (
                  <TableCell key={horizon} align="center">
                    {formatPercentage(stats.median)}
                  </TableCell>
                );
              })}
            </TableRow>

            <TableRow>
              <TableCell>Best / Worst</TableCell>
              {horizons.map((horizon) => {
                const stats = data.summary_statistics[horizon];
                return (
                  <TableCell key={horizon} align="center" sx={{ fontSize: '0.85rem' }}>
                    {formatPercentage(stats.max)} / {formatPercentage(stats.min)}
                  </TableCell>
                );
              })}
            </TableRow>

            <TableRow>
              <TableCell>Std Deviation</TableCell>
              {horizons.map((horizon) => {
                const stats = data.summary_statistics[horizon];
                return (
                  <TableCell key={horizon} align="center">
                    {formatPercentage(stats.std)}
                  </TableCell>
                );
              })}
            </TableRow>

            <TableRow>
              <TableCell>Occurrences</TableCell>
              {horizons.map((horizon) => {
                const stats = data.summary_statistics[horizon];
                return (
                  <TableCell key={horizon} align="center">
                    {stats.count ?? 'N/A'}
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
