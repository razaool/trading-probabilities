import React, { useState } from 'react';
import { Container, Box, CircularProgress, Alert, AlertTitle } from '@mui/material';
import QueryForm from '../components/QueryForm';
import ResultsTable from '../components/ResultsTable';
import SummaryStatistics from '../components/SummaryStatistics';
import PriceChart from '../components/PriceChart';
import GradientText from '../components/GradientText';
import GlassSurface from '../components/GlassSurface';
import FloatingLinesBackground from '../components/FloatingLinesBackground';
import { apiService } from '../services/api';
import type { QueryRequest, QueryResponse } from '../types/api';

export default function HomePage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<QueryResponse | null>(null);

  const handleQuery = async (query: QueryRequest) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await apiService.queryHistoricalPatterns(query);
      console.log('=== API Response Debug ===');
      console.log('Full response:', response);
      console.log('Total occurrences:', response.total_occurrences);
      console.log('Number of instances:', response.instances.length);
      console.log('First 3 instances:', response.instances.slice(0, 3));
      console.log('========================');
      setResults(response);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to query historical patterns';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <FloatingLinesBackground />
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          minHeight: '100vh',
          py: 4,
          px: 2,
        }}
      >
        <Box
          sx={{
            width: '100%',
            maxWidth: 1000,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            minWidth: { xs: 375, sm: 'auto' },
          }}
        >
          <Box sx={{ width: '100%', textAlign: 'center' }}>
            <Box sx={{ mb: 4 }}>
              <h1>
                <GradientText>Historical Pattern Analysis Tool</GradientText>
              </h1>
              <p style={{ color: 'text.secondary' }}>
                Query historical market data and analyze forward returns
              </p>
            </Box>

            <Box sx={{ maxWidth: 700, mx: 'auto', mb: 4 }}>
              <GlassSurface>
                <QueryForm onSubmit={handleQuery} loading={loading} />
              </GlassSurface>
            </Box>

            {loading && (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
                <CircularProgress />
              </Box>
            )}

            {error && (
              <Alert severity="error" sx={{ mt: 3, maxWidth: 700, mx: 'auto' }}>
                <AlertTitle>Error</AlertTitle>
                {error}
              </Alert>
            )}

            {results && !loading && (
              <Box sx={{ width: '100%' }}>
                <GlassSurface sx={{ mb: 2 }}>
                  <PriceChart
                    ticker={results.ticker}
                    occurrenceDates={results.instances.map(i => i.date)}
                  />
                </GlassSurface>
                <GlassSurface sx={{ mb: 2 }}>
                  <SummaryStatistics data={results} />
                </GlassSurface>
                <GlassSurface>
                  <ResultsTable data={results} />
                </GlassSurface>
              </Box>
            )}
          </Box>
        </Box>
      </Box>
    </>
  );
}
