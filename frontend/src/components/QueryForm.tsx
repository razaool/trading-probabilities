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
import SlidingToggleGroup from './SlidingToggleGroup';
import SlidingButtonGroup from './SlidingButtonGroup';

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
  { value: 'sectors', label: 'Sector ETFs' },
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

const SECTOR_ETF_OPTIONS = [
  { value: 'XLF', label: 'XLF', description: 'Financial Select Sector SPDR' },
  { value: 'XLE', label: 'XLE', description: 'Energy Select Sector SPDR' },
  { value: 'XLK', label: 'XLK', description: 'Technology Select Sector SPDR' },
  { value: 'XLV', label: 'XLV', description: 'Health Care Select Sector SPDR' },
  { value: 'XLY', label: 'XLY', description: 'Consumer Discretionary Select Sector SPDR' },
  { value: 'XLP', label: 'XLP', description: 'Consumer Staples Select Sector SPDR' },
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
  const [assetType, setAssetType] = useState<'stocks' | 'indicators' | 'commodities' | 'sectors'>('stocks');

  // Filter suggestions based on asset type
  const filteredSuggestions = suggestions.filter(suggestion => {
    const symbol = suggestion.ticker.toUpperCase();
    if (assetType === 'indicators') {
      // Show only PCR, VIX, VXN indicators
      return ['PCR', 'VIX', '^VIX', 'VXN', '^VXN', 'RVX'].includes(symbol);
    } else if (assetType === 'commodities') {
      // Show only commodities
      return ['GLD', 'USO', 'SLV'].includes(symbol);
    } else if (assetType === 'sectors') {
      // Show only sector ETFs
      return ['XLF', 'XLE', 'XLK', 'XLV', 'XLY', 'XLP'].includes(symbol);
    } else {
      // Hide indicators, commodities, and sector ETFs from stock/ETF view
      return !['PCR', 'VIX', '^VIX', 'VXN', '^VXN', 'RVX', 'GLD', 'USO', 'SLV', 'XLF', 'XLE', 'XLK', 'XLV', 'XLY', 'XLP'].includes(symbol);
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
  const handleAssetTypeChange = (newAssetType: string) => {
    if (newAssetType && typeof newAssetType === 'string') {
      setAssetType(newAssetType as 'stocks' | 'indicators' | 'commodities' | 'sectors');
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

  // Handle sector ETF button click
  const handleSectorSelect = (sectorValue: string) => {
    setTicker(sectorValue);
    // Don't force condition type for sectors - let user choose
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
    <Box sx={{ p: { xs: 1.5, sm: 3 } }}>
      <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, mb: { xs: 2, sm: 3 } }}>
        Query Historical Patterns
      </Typography>

      <Box sx={{ mb: { xs: 2, sm: 3 } }}>
        <SlidingToggleGroup
          value={assetType}
          onChange={handleAssetTypeChange}
          options={ASSET_TYPE_OPTIONS}
        />
      </Box>

      <Box component="form" onSubmit={handleSubmit}>
        {assetType === 'indicators' ? (
          <>
            <Typography variant="subtitle2" gutterBottom sx={{ mb: 1 }}>
              Select Indicator
            </Typography>
            <Box sx={{ mb: { xs: 1.5, sm: 2 } }}>
              <SlidingButtonGroup
                value={ticker}
                onChange={handleIndicatorSelect}
                options={INDICATOR_OPTIONS}
              />
            </Box>
          </>
        ) : assetType === 'commodities' ? (
          <>
            <Typography variant="subtitle2" gutterBottom sx={{ mb: 1 }}>
              Select Commodity
            </Typography>
            <Box sx={{ mb: { xs: 1.5, sm: 2 } }}>
              <SlidingButtonGroup
                value={ticker}
                onChange={handleCommoditySelect}
                options={COMMODITY_OPTIONS}
              />
            </Box>
          </>
        ) : assetType === 'sectors' ? (
          <>
            <Typography variant="subtitle2" gutterBottom sx={{ mb: 1 }}>
              Select Sector ETF
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: { xs: 1, sm: 1.5 }, mb: { xs: 1.5, sm: 2 } }}>
              <SlidingButtonGroup
                value={ticker}
                onChange={handleSectorSelect}
                options={SECTOR_ETF_OPTIONS}
              />
            </Box>
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
                sx={{
                  mb: 2,
                  '& .MuiOutlinedInput-root': {
                    borderRadius: 2,
                    transition: 'all 0.2s ease',
                    '&.Mui-focused': {
                      '& .MuiOutlinedInput-notchedOutline': {
                        borderWidth: 2,
                      },
                    },
                  },
                }}
                required
              />
            )}
          />
        )}

        <FormControl fullWidth sx={{ mb: { xs: 1.5, sm: 2 } }}>
          <InputLabel>Condition Type</InputLabel>
          <Select
            value={conditionType}
            label="Condition Type"
            onChange={(e) => handleConditionTypeChange(e.target.value as QueryRequest['condition_type'])}
            disabled={assetType === 'indicators'}
            sx={{
              borderRadius: 2,
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                transition: 'all 0.2s ease',
                '&:hover': {
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderColor: 'primary.main',
                  },
                },
                '&.Mui-focused': {
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderWidth: 2,
                  },
                },
              },
            }}
          >
            {CONDITION_TYPES.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Box sx={{ display: 'flex', gap: { xs: 1, sm: 2 }, mb: { xs: 1.5, sm: 2 } }}>
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
              sx={{
                borderRadius: 2,
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2,
                  transition: 'all 0.2s ease',
                  '&:hover': {
                    '& .MuiOutlinedInput-notchedOutline': {
                      borderColor: 'primary.main',
                    },
                  },
                  '&.Mui-focused': {
                    '& .MuiOutlinedInput-notchedOutline': {
                      borderWidth: 2,
                    },
                  },
                },
              }}
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
                sx={{
                  borderRadius: 2,
                  '& .MuiOutlinedInput-root': {
                    borderRadius: 2,
                    transition: 'all 0.2s ease',
                    '&:hover': {
                      '& .MuiOutlinedInput-notchedOutline': {
                        borderColor: 'primary.main',
                      },
                    },
                    '&.Mui-focused': {
                      '& .MuiOutlinedInput-notchedOutline': {
                        borderWidth: 2,
                      },
                    },
                  },
                }}
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
            sx={{
              flex: assetType === 'indicators' ? 1 : 1,
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                transition: 'all 0.2s ease',
                '&.Mui-focused': {
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderWidth: 2,
                  },
                },
              },
            }}
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

        <FormControl fullWidth sx={{ mb: { xs: 2, sm: 3 } }}>
          <InputLabel>Time Horizons</InputLabel>
          <Select
            multiple
            value={timeHorizons}
            label="Time Horizons"
            onChange={handleTimeHorizonChange}
            renderValue={(selected) => selected.map((h) => TIME_HORIZONS.find(th => th.value === h)?.label).join(', ')}
            sx={{
              borderRadius: 2,
              '& .MuiOutlinedInput-root': {
                borderRadius: 2,
                transition: 'all 0.2s ease',
                '&:hover': {
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderColor: 'primary.main',
                  },
                },
                '&.Mui-focused': {
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderWidth: 2,
                  },
                },
              },
            }}
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
          sx={{
            borderRadius: 2,
            py: 1.5,
            fontWeight: 600,
            textTransform: 'none',
            fontSize: '1rem',
            transition: 'all 0.2s ease',
            background: 'linear-gradient(90deg, #646cff 0%, #747bff 25%, #a855f7 50%, #747bff 75%, #646cff 100%)',
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 8px 24px rgba(100, 108, 255, 0.3)',
              background: 'linear-gradient(90deg, #646cff 0%, #747bff 25%, #a855f7 50%, #747bff 75%, #646cff 100%)',
            },
            '&:active': {
              transform: 'translateY(0)',
            },
          }}
        >
          {loading ? 'Analyzing...' : 'Query Historical Data'}
        </Button>
      </Box>
    </Box>
  );
}
