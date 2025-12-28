import React, { useEffect, useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  CircularProgress,
  Chip,
  useTheme,
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { apiService } from '../services/api';

interface PriceDataPoint {
  date: string;
  close: number;
}

interface PriceChartProps {
  ticker: string;
  occurrenceDates: string[];
}

export default function PriceChart({ ticker }: PriceChartProps) {
  const theme = useTheme();
  const [priceData, setPriceData] = useState<PriceDataPoint[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPrices = async () => {
      try {
        setLoading(true);
        const response = await apiService.getHistoricalPrices(ticker);

        // Just show last 2 years of data
        const twoYearsData = response.prices.slice(-504); // ~252 trading days per year * 2

        // Transform to simpler format
        const chartData = twoYearsData.map(price => ({
          date: price.date,
          close: price.close,
        }));

        setPriceData(chartData);
        setError(null);
      } catch (err) {
        console.error('Error fetching price data:', err);
        setError('Failed to load price data');
      } finally {
        setLoading(false);
      }
    };

    fetchPrices();
  }, [ticker]);

  // Format currency
  const formatPrice = (value: number) => {
    return `$${value.toFixed(2)}`;
  };

  // Format date for tooltip
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  // Custom tooltip
  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <Box
          sx={{
            bgcolor: 'background.paper',
            p: 1.5,
            borderRadius: 1,
            border: 1,
            borderColor: 'divider',
            boxShadow: 3,
          }}
        >
          <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
            {formatDate(payload[0].payload.date)}
          </Typography>
          <Typography variant="body2" sx={{ color: '#646cff', fontSize: '0.85rem' }}>
            Close: {formatPrice(payload[0].value)}
          </Typography>
        </Box>
      );
    }
    return null;
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 8 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ textAlign: 'center', py: 4 }}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  // Calculate min and max for Y axis
  const allPrices = priceData.map(d => d.close);
  const minY = Math.min(...allPrices) * 0.98;
  const maxY = Math.max(...allPrices) * 1.02;

  // Get theme-aware colors
  const axisColor = theme.palette.mode === 'dark' ? 'rgba(255, 255, 255, 0.7)' : 'rgba(0, 0, 0, 0.7)';
  const gridColor = theme.palette.mode === 'dark' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';
  const axisStroke = theme.palette.mode === 'dark' ? 'rgba(255, 255, 255, 0.3)' : 'rgba(0, 0, 0, 0.3)';

  return (
    <Paper
      elevation={0}
      sx={{
        p: 2,
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
      <Box sx={{ mb: 1 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, fontSize: '1.1rem' }}>
          Price History: {ticker}
        </Typography>
      </Box>

      <ResponsiveContainer width="100%" height={350}>
        <LineChart
          data={priceData}
          margin={{
            top: 10,
            right: 20,
            left: 10,
            bottom: 10,
          }}
        >
          <CartesianGrid
            strokeDasharray="3 3"
            stroke={gridColor}
            vertical={false}
          />
          <XAxis
            dataKey="date"
            tick={{ fill: axisColor, fontSize: 11 }}
            stroke={axisStroke}
            tickFormatter={(dateStr) => {
              const date = new Date(dateStr);
              return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
            }}
            angle={-45}
            textAnchor="end"
            height={30}
            interval="preserveStartEnd"
          />
          <YAxis
            domain={[minY, maxY]}
            tick={{ fill: axisColor, fontSize: 11 }}
            stroke={axisStroke}
            tickFormatter={formatPrice}
            width={60}
          />
          <Tooltip content={<CustomTooltip />} />
          <Line
            type="monotone"
            dataKey="close"
            stroke="#646cff"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 6, fill: '#646cff', stroke: '#fff', strokeWidth: 2 }}
            name="Close Price"
          />
        </LineChart>
      </ResponsiveContainer>

      <Box>
        <Typography variant="caption" color="text.secondary" sx={{ fontStyle: 'italic' }}>
          Historical price data for the last 2 years
        </Typography>
      </Box>
    </Paper>
  );
}
