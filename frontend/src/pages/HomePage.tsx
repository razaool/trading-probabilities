import React, { useState } from 'react';
import { Container, Box, CircularProgress, Alert, AlertTitle } from '@mui/material';
import QueryForm from '../components/QueryForm';
import ResultsTable from '../components/ResultsTable';
import SummaryStatistics from '../components/SummaryStatistics';
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
      setResults(response);
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to query historical patterns';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ my: 4 }}>
        <Box sx={{ mb: 4, textAlign: 'center' }}>
          <h1>Historical Pattern Analysis Tool</h1>
          <p style={{ color: '#666' }}>
            Query historical market data and analyze forward returns
          </p>
        </Box>

        <Box sx={{ maxWidth: 600, mx: 'auto' }}>
          <QueryForm onSubmit={handleQuery} loading={loading} />
        </Box>

        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
            <CircularProgress />
          </Box>
        )}

        {error && (
          <Alert severity="error" sx={{ mt: 3 }}>
            <AlertTitle>Error</AlertTitle>
            {error}
          </Alert>
        )}

        {results && !loading && (
          <>
            <SummaryStatistics data={results} />
            <ResultsTable data={results} />
          </>
        )}
      </Box>
    </Container>
  );
}
