import React, { useState, useEffect } from 'react';
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
  Autocomplete,
  Stack,
  ToggleButton,
  ToggleButtonGroup,
  Chip,
} from '@mui/material';
import type { QueryRequest, TickerSuggestion } from '../types/api';
import { apiService } from '../services/api';

interface QueryFormProps {
  onSubmit: (query: QueryRequest) => void;
  loading?: boolean;
}

const CONDITION_TYPES = [
  { value: 'percentage_change', label: 'Percentage Change' },
  { value: 'absolute_threshold', label: 'Absolute Threshold' },
];

const ASSET_TYPE_OPTIONS = [
  { value: 'stocks', label: 'Stocks & ETFs' },
  { value: 'indicators', label: 'Indicators' },
];

const INDICATOR_OPTIONS = [
  { value: '^VIX', label: 'VIX', description: 'CBOE Volatility Index' },
  { value: '^VXN', label: 'VXN', description: 'Nasdaq-100 Volatility Index' },
  { value: 'PCR', label: 'PCR', description: 'Put/Call Ratio' },
];

const DIRECTION_OPTIONS = [
  { value: 'increase', label: 'Price Increased (Rose)' },
  { value: 'decrease', label: 'Price Decreased (Dropped)' },
];

const OPERATOR_OPTIONS = [
  { value: 'gte', label: 'At Least (≥)' },  // Greater or equal - matches threshold AND beyond
  { value: 'eq', label: 'Exact Match (≈)' },  // Exact - matches within ±0.5%
  { value: 'gt', label: 'More Than (>)' },  // Greater than - matches beyond threshold only
];

const TIME_HORIZONS = [
  { value: '1d', label: '1 Day' },
  { value: '1w', label: '1 Week' },
  { value: '1m', label: '1 Month' },
  { value: '1y', label: '1 Year' },
];

export default function QueryForm({ onSubmit, loading }: QueryFormProps) {
  const [ticker, setTicker] = useState('');
  const [suggestions, setSuggestions] = useState<TickerSuggestion[]>([]);
  const [conditionType, setConditionType] = useState<QueryRequest['condition_type']>('percentage_change');
  const [threshold, setThreshold] = useState('');
  const [direction, setDirection] = useState<'increase' | 'decrease'>('increase');
  const [operator, setOperator] = useState<QueryRequest['operator']>('gte');
  const [timeHorizons, setTimeHorizons] = useState<QueryRequest['time_horizons']>(['1d', '1w', '1m', '1y']);
  const [assetType, setAssetType] = useState<'stocks' | 'indicators'>('stocks');

  // Filter suggestions based on asset type
  const filteredSuggestions = suggestions.filter(suggestion => {
    const symbol = suggestion.ticker.toUpperCase();
    if (assetType === 'indicators') {
      // Show only PCR, VIX, VXN indicators
      return ['PCR', 'VIX', '^VIX', 'VXN', '^VXN', 'RVX'].includes(symbol);
    } else {
      // Hide indicators from stock/ETF view
      return !['PCR', 'VIX', '^VIX', 'VXN', '^VXN', 'RVX'].includes(symbol);
    }
  });

  // Fetch suggestions when ticker changes
  useEffect(() => {
    if (ticker.length >= 1) {
      const debounceTimer = setTimeout(async () => {
        try {
          const results = await apiService.getTickerSuggestions(ticker);
          setSuggestions(results);
        } catch (error) {
          console.error('Error fetching suggestions:', error);
        }
      }, 300);

      return () => clearTimeout(debounceTimer);
    } else {
      setSuggestions([]);
    }
  }, [ticker]);

  // Reset ticker when switching asset types
  const handleAssetTypeChange = (
    event: React.MouseEvent<HTMLElement>,
    newAssetType: 'stocks' | 'indicators' | null,
  ) => {
    if (newAssetType) {
      setAssetType(newAssetType);
      setTicker('');
      setSuggestions([]);
    }
  };

  // Handle indicator button click
  const handleIndicatorSelect = (indicatorValue: string) => {
    setTicker(indicatorValue);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!ticker || !threshold) {
      return;
    }

    const thresholdValue = parseFloat(threshold);

    // Convert direction to operator and apply sign
    let finalOperator: QueryRequest['operator'];
    let finalThreshold: number;

    if (direction === 'increase') {
      // Price increased
      finalOperator = operator;
      finalThreshold = thresholdValue;
    } else {
      // Price decreased: invert operator and make threshold negative
      if (operator === 'gt') {
        finalOperator = 'lt'; // Decrease "more than" = less than negative
      } else if (operator === 'gte') {
        finalOperator = 'lte'; // Decrease "at least" = less than or equal negative
      } else {
        finalOperator = 'eq'; // Exact match stays the same
      }
      finalThreshold = -thresholdValue; // Convert positive input to negative
    }

    onSubmit({
      ticker: ticker.toUpperCase(),
      condition_type: conditionType,
      threshold: finalThreshold,
      operator: finalOperator,
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

      <Box sx={{ mb: 3 }}>
        <ToggleButtonGroup
          value={assetType}
          exclusive
          onChange={handleAssetTypeChange}
          aria-label="Asset Type"
          sx={{ mb: 1 }}
        >
          <ToggleButton value="stocks" aria-label="Stocks & ETFs">
            Stocks & ETFs
          </ToggleButton>
          <ToggleButton value="indicators" aria-label="Indicators">
            Indicators
          </ToggleButton>
        </ToggleButtonGroup>
        <Typography variant="caption" display="block" color="text.secondary">
          {assetType === 'indicators'
            ? 'Volatility and sentiment indicators (VIX, VXN, PCR)'
            : 'Individual stocks, ETFs, and market indices'}
        </Typography>
      </Box>

      <Box component="form" onSubmit={handleSubmit}>
        {assetType === 'indicators' ? (
          <>
            <Typography variant="subtitle2" gutterBottom sx={{ mb: 1 }}>
              Select Indicator
            </Typography>
            <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
              {INDICATOR_OPTIONS.map((indicator) => (
                <Button
                  key={indicator.value}
                  variant={ticker === indicator.value ? "contained" : "outlined"}
                  onClick={() => handleIndicatorSelect(indicator.value)}
                  sx={{
                    flex: 1,
                    py: 1.5,
                    textTransform: 'none',
                    flexDirection: 'column',
                    alignItems: 'flex-start',
                  }}
                >
                  <Typography variant="h6" component="span" fontWeight="bold">
                    {indicator.label}
                  </Typography>
                  <Typography variant="caption" component="span">
                    {indicator.description}
                  </Typography>
                </Button>
              ))}
            </Stack>
            {ticker && (
              <Box sx={{ mb: 2 }}>
                <Chip
                  label={`Selected: ${ticker}`}
                  onDelete={() => setTicker('')}
                  color="primary"
                />
              </Box>
            )}
          </>
        ) : (
          <Autocomplete
            freeSolo
            options={filteredSuggestions}
            getOptionLabel={(option) => {
              if (typeof option === 'string') return option;
              return option.ticker;
            }}
            value={ticker}
            onChange={(event, newValue) => {
              if (typeof newValue === 'string') {
                setTicker(newValue);
              } else if (newValue) {
                setTicker(newValue.ticker);
              } else {
                setTicker('');
              }
            }}
            onInputChange={(event, newInputValue) => {
              setTicker(newInputValue);
            }}
            renderOption={(props, option) => (
              <Box component="li" {...props} sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                <Typography variant="body1" fontWeight="bold">
                  {option.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {option.ticker}
                </Typography>
              </Box>
            )}
            slotProps={{
              paper: {
                sx: {
                  width: 'fit-content',
                  minWidth: '100%',
                }
              }
            }}
            renderInput={(params) => (
              <TextField
                {...params}
                fullWidth
                label="Ticker Symbol"
                placeholder="e.g., NVDA, AVGO, SPY"
                sx={{ mb: 2 }}
                required
              />
            )}
          />
        )}

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
            <InputLabel>Direction</InputLabel>
            <Select
              value={direction}
              label="Direction"
              onChange={(e) => setDirection(e.target.value as 'increase' | 'decrease')}
            >
              {DIRECTION_OPTIONS.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl sx={{ flex: 1 }}>
            <InputLabel>Match Type</InputLabel>
            <Select
              value={operator}
              label="Match Type"
              onChange={(e) => setOperator(e.target.value as QueryRequest['operator'])}
            >
              {OPERATOR_OPTIONS.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <TextField
            sx={{ flex: 1 }}
            label="Percentage"
            type="number"
            value={threshold}
            onChange={(e) => setThreshold(e.target.value)}
            placeholder="e.g., 5, 10, 20"
            helperText="Enter a positive number (e.g., 5 for 5%)"
            inputProps={{ step: "any", min: 0 }}
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
