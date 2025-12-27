import React, { useState } from 'react';
import {
  Box,
  Paper,
  TextField,
  Select,
  MenuItem,
  Button,
  Typography,
  FormControl,
  InputLabel,
  Checkbox,
  ListItemText,
} from '@mui/material';
import type { QueryRequest } from '../types/api';

interface QueryFormProps {
  onSubmit: (query: QueryRequest) => void;
  loading?: boolean;
}

const CONDITION_TYPES = [
  { value: 'percentage_change', label: 'Percentage Change' },
  { value: 'absolute_threshold', label: 'Absolute Threshold' },
];

const OPERATORS = [
  { value: 'gt', label: '>' },
  { value: 'lt', label: '<' },
  { value: 'gte', label: '>=' },
  { value: 'lte', label: '<=' },
  { value: 'eq', label: '=' },
];

const TIME_HORIZONS = [
  { value: '1d', label: '1 Day' },
  { value: '1w', label: '1 Week' },
  { value: '1m', label: '1 Month' },
  { value: '1y', label: '1 Year' },
];

export default function QueryForm({ onSubmit, loading }: QueryFormProps) {
  const [ticker, setTicker] = useState('');
  const [conditionType, setConditionType] = useState<QueryRequest['condition_type']>('percentage_change');
  const [threshold, setThreshold] = useState('');
  const [operator, setOperator] = useState<QueryRequest['operator']>('gt');
  const [timeHorizons, setTimeHorizons] = useState<QueryRequest['time_horizons']>(['1d', '1w', '1m', '1y']);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!ticker || !threshold) {
      return;
    }

    onSubmit({
      ticker: ticker.toUpperCase(),
      condition_type: conditionType,
      threshold: parseFloat(threshold),
      operator,
      time_horizons: timeHorizons,
    });
  };

  const handleTimeHorizonChange = (event: React.ChangeEvent<{ value: unknown }>) => {
    const value = event.target.value as string[];
    setTimeHorizons(typeof value === 'string' ? value.split(',') as QueryRequest['time_horizons'] : value as QueryRequest['time_horizons']);
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Query Historical Patterns
      </Typography>
      <Box component="form" onSubmit={handleSubmit}>
        <TextField
          fullWidth
          label="Ticker Symbol"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          placeholder="e.g., NVDA, VIX, SPY"
          sx={{ mb: 2 }}
          required
        />

        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel>Condition Type</InputLabel>
          <Select
            value={conditionType}
            label="Condition Type"
            onChange={(e) => setConditionType(e.target.value as QueryRequest['condition_type'])}
          >
            {CONDITION_TYPES.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <FormControl sx={{ flex: 1 }}>
            <InputLabel>Operator</InputLabel>
            <Select
              value={operator}
              label="Operator"
              onChange={(e) => setOperator(e.target.value as QueryRequest['operator'])}
            >
              {OPERATORS.map((op) => (
                <MenuItem key={op.value} value={op.value}>
                  {op.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <TextField
            sx={{ flex: 1 }}
            label="Threshold"
            type="number"
            value={threshold}
            onChange={(e) => setThreshold(e.target.value)}
            placeholder="e.g., 3, 30"
            required
          />
        </Box>

        <FormControl fullWidth sx={{ mb: 3 }}>
          <InputLabel>Time Horizons</InputLabel>
          <Select
            multiple
            value={timeHorizons}
            label="Time Horizons"
            onChange={handleTimeHorizonChange}
            renderValue={(selected) => selected.map((h) => TIME_HORIZONS.find(th => th.value === h)?.label).join(', ')}
          >
            {TIME_HORIZONS.map((horizon) => (
              <MenuItem key={horizon.value} value={horizon.value}>
                <Checkbox checked={timeHorizons.indexOf(horizon.value as '1d' | '1w' | '1m' | '1y') > -1} />
                <ListItemText primary={horizon.label} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Button
          fullWidth
          variant="contained"
          type="submit"
          disabled={loading}
          size="large"
        >
          {loading ? 'Analyzing...' : 'Query Historical Data'}
        </Button>
      </Box>
    </Paper>
  );
}
