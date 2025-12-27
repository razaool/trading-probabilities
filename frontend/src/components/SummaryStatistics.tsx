import React from 'react';
import {
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import type { QueryResponse, SummaryStatistics } from '../types/api';

interface SummaryStatisticsProps {
  data: QueryResponse;
}

function formatPercentage(value: number): string {
  return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
}

function formatWinRate(value: number): string {
  return `${(value * 100).toFixed(1)}%`;
}

interface StatCardProps {
  title: string;
  value: string;
  subtitle?: string;
  positive?: boolean;
}

function StatCard({ title, value, subtitle, positive }: StatCardProps) {
  return (
    <Card>
      <CardContent>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          {title}
        </Typography>
        <Typography
          variant="h5"
          component="div"
          sx={{ color: positive !== undefined ? (positive ? '#2e7d32' : '#d32f2f') : 'inherit' }}
        >
          {value}
        </Typography>
        {subtitle && (
          <Typography variant="caption" color="text.secondary">
            {subtitle}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}

export default function SummaryStatistics({ data }: SummaryStatisticsProps) {
  return (
    <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Summary Statistics
      </Typography>

      {Object.entries(data.summary_statistics).map(([horizon, stats]: [string, SummaryStatistics]) => (
        <Box key={horizon} sx={{ mt: 3 }}>
          <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
            {data.ticker} +{horizon.toUpperCase()}
          </Typography>

          <Grid container spacing={2} sx={{ mb: 2 }}>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Average Return"
                value={formatPercentage(stats.mean)}
                subtitle={`${stats.count} occurrences`}
                positive={stats.mean >= 0}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Median Return"
                value={formatPercentage(stats.median)}
                positive={stats.median >= 0}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Win Rate"
                value={formatWinRate(stats.win_rate)}
                subtitle={stats.win_rate >= 0.5 ? 'Bullish' : 'Bearish'}
                positive={stats.win_rate >= 0.5}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Best / Worst"
                value={`${formatPercentage(stats.max)} / ${formatPercentage(stats.min)}`}
              />
            </Grid>
          </Grid>

          <TableContainer size="small">
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Metric</TableCell>
                  <TableCell align="right">Value</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                <TableRow>
                  <TableCell>Standard Deviation</TableCell>
                  <TableCell align="right">{formatPercentage(stats.std)}</TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>Count</TableCell>
                  <TableCell align="right">{stats.count}</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      ))}
    </Paper>
  );
}
