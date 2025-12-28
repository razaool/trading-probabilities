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
  { value: 'commodities', label: 'Commodities' },
];

const INDICATOR_OPTIONS = [
  { value: '^VIX', label: 'VIX', description: 'CBOE Volatility Index' },
  { value: '^VXN', label: 'VXN', description: 'Nasdaq-100 Volatility Index' },
  { value: 'PCR', label: 'PCR', description: 'Put/Call Ratio' },
];

const COMMODITY_OPTIONS = [
  { value: 'GLD', label: 'GLD', description: 'Gold (SPDR Gold Shares)' },
  { value: 'USO', label: 'USO', description: 'Oil (US Oil Fund)' },
  { value: 'SLV', label: 'SLV', description: 'Silver (iShares Silver Trust)' },
];

const DIRECTION_OPTIONS = [
  { value: 'increase', label: 'Price Increased (Rose)' },
  { value: 'decrease', label: 'Price Decreased (Dropped)' },
];

const INDICATOR_DIRECTION_OPTIONS = [
  { value: 'above', label: 'Exceeded (Above)' },
  { value: 'below', label: 'Dropped Below' },
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
  const [direction, setDirection] = useState<'increase' | 'decrease' | 'above' | 'below'>('increase');
  const [operator, setOperator] = useState<QueryRequest['operator']>('gte');
  const [timeHorizons, setTimeHorizons] = useState<QueryRequest['time_horizons']>(['1d', '1w', '1m', '1y']);
  const [assetType, setAssetType] = useState<'stocks' | 'indicators' | 'commodities'>('stocks');

  // Filter suggestions based on asset type
  const filteredSuggestions = suggestions.filter(suggestion => {
    const symbol = suggestion.ticker.toUpperCase();
    if (assetType === 'indicators') {
      // Show only PCR, VIX, VXN indicators
      return ['PCR', 'VIX', '^VIX', 'VXN', '^VXN', 'RVX'].includes(symbol);
    } else if (assetType === 'commodities') {
      // Show only commodities
      return ['GLD', 'USO', 'SLV'].includes(symbol);
    } else {
      // Hide indicators and commodities from stock/ETF view
      return !['PCR', 'VIX', '^VIX', 'VXN', '^VXN', 'RVX', 'GLD', 'USO', 'SLV'].includes(symbol);
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
    newAssetType: 'stocks' | 'indicators' | 'commodities' | null,
  ) => {
    if (newAssetType) {
      setAssetType(newAssetType);
      setTicker('');
      setSuggestions([]);
      // Reset direction to appropriate default for the asset type
      if (newAssetType === 'indicators') {
        setDirection('above');
      } else {
        setDirection('increase');
      }
    }
  };

  // Handle indicator button click
  const handleIndicatorSelect = (indicatorValue: string) => {
    setTicker(indicatorValue);
    // Force absolute threshold for indicators
    setConditionType('absolute_threshold');
    // Reset direction to 'above' for indicators
    setDirection('above');
  };

  // Handle commodity button click
  const handleCommoditySelect = (commodityValue: string) => {
    setTicker(commodityValue);
    // Don't force condition type for commodities - let user choose
  };

  // Handle condition type change - reset direction if switching to/from absolute threshold
  const handleConditionTypeChange = (newConditionType: QueryRequest['condition_type']) => {
    setConditionType(newConditionType);
    // If switching to absolute_threshold, reset direction to 'above'
    if (newConditionType === 'absolute_threshold' && direction === 'increase') {
      setDirection('above');
    }
    // If switching to percentage_change and direction is 'above', reset to 'increase'
    if (newConditionType === 'percentage_change' && direction === 'above') {
      setDirection('increase');
    }
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

    // For indicators, always use 'gte' (greater or equal) or 'lte' (less or equal)
    // based on the direction, since Match Type is not shown
    if (direction === 'above') {
      // Indicator exceeded threshold: use >=
      finalOperator = 'gte';
      finalThreshold = thresholdValue;
    } else if (direction === 'below') {
      // Indicator dropped below threshold: use <=
      finalOperator = 'lte';
      finalThreshold = thresholdValue;
    } else if (direction === 'increase') {
      // Price increased: use the operator from Match Type
      finalOperator = operator;
      finalThreshold = thresholdValue;
    } else {
      // direction === 'decrease' - Price decreased: invert operator and make threshold negative
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
          <ToggleButton value="commodities" aria-label="Commodities">
            Commodities
          </ToggleButton>
        </ToggleButtonGroup>
        <Typography variant="caption" display="block" color="text.secondary">
          {assetType === 'indicators'
            ? 'Volatility and sentiment indicators (VIX, VXN, PCR)'
            : assetType === 'commodities'
            ? 'Gold, oil, and silver commodities'
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
          </>
        ) : assetType === 'commodities' ? (
          <>
            <Typography variant="subtitle2" gutterBottom sx={{ mb: 1 }}>
              Select Commodity
            </Typography>
            <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
              {COMMODITY_OPTIONS.map((commodity) => (
                <Button
                  key={commodity.value}
                  variant={ticker === commodity.value ? "contained" : "outlined"}
                  onClick={() => handleCommoditySelect(commodity.value)}
                  sx={{
                    flex: 1,
                    py: 1.5,
                    textTransform: 'none',
                    flexDirection: 'column',
                    alignItems: 'flex-start',
                  }}
                >
                  <Typography variant="h6" component="span" fontWeight="bold">
                    {commodity.label}
                  </Typography>
                  <Typography variant="caption" component="span">
                    {commodity.description}
                  </Typography>
                </Button>
              ))}
            </Stack>
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
            onChange={(e) => handleConditionTypeChange(e.target.value as QueryRequest['condition_type'])}
            disabled={assetType === 'indicators'}
          >
            {CONDITION_TYPES.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
          {assetType === 'indicators' && (
            <Typography variant="caption" color="text.secondary">
              Indicators always use absolute threshold values
            </Typography>
          )}
        </FormControl>

        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <FormControl sx={{ flex: assetType === 'indicators' ? 1 : 1 }}>
            <InputLabel>
              {assetType === 'indicators' ? 'Condition' :
               conditionType === 'absolute_threshold' ? 'Price Level' : 'Direction'}
            </InputLabel>
            <Select
              value={direction}
              label={
                assetType === 'indicators' ? 'Condition' :
                conditionType === 'absolute_threshold' ? 'Price Level' : 'Direction'
              }
              onChange={(e) => setDirection(e.target.value as 'increase' | 'decrease' | 'above' | 'below')}
            >
              {(assetType === 'indicators' || conditionType === 'absolute_threshold'
                ? INDICATOR_DIRECTION_OPTIONS
                : DIRECTION_OPTIONS).map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {assetType !== 'indicators' && conditionType === 'percentage_change' && (
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
          )}

          <TextField
            sx={{ flex: assetType === 'indicators' ? 1 : 1 }}
            label={
              assetType === 'indicators' ? 'Threshold Value' :
              conditionType === 'absolute_threshold' ? 'Price Level ($)' : 'Percentage'
            }
            type="number"
            value={threshold}
            onChange={(e) => setThreshold(e.target.value)}
            placeholder={
              assetType === 'indicators' ? "e.g., 30, 1.0, 0.8" :
              conditionType === 'absolute_threshold' ? "e.g., 500, 1000, 150" : "e.g., 5, 10, 20"
            }
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
