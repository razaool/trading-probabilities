import React from 'react';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material';
import type { QueryResponse } from '../types/api';

interface ResultsTableProps {
  data: QueryResponse;
}

function formatPercentage(value: number | null | undefined): string {
  if (value === null || value === undefined) return 'N/A';
  return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
}

function formatCellColor(value: number | null | undefined): React.CSSProperties {
  if (value === null || value === undefined) return {};
  return {
    color: value >= 0 ? '#2e7d32' : '#d32f2f',
    fontWeight: 'bold',
  };
}

export default function ResultsTable({ data }: ResultsTableProps) {
  const timeHorizons = Object.keys(data.summary_statistics);

  return (
    <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Historical Occurrences
      </Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        {data.condition} - {data.total_occurrences} instances found
      </Typography>

      <TableContainer sx={{ mt: 2 }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Date</TableCell>
              {timeHorizons.map((horizon) => (
                <TableCell key={horizon} align="right">
                  {data.ticker} +{horizon.toUpperCase()}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {data.instances.map((instance, index) => (
              <TableRow key={index} hover>
                <TableCell component="th" scope="row">
                  {instance.date}
                </TableCell>
                {timeHorizons.map((horizon) => (
                  <TableCell key={horizon} align="right" style={formatCellColor(instance.forward_returns[horizon])}>
                    {formatPercentage(instance.forward_returns[horizon])}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}
