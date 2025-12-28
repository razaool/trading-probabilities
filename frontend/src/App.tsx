import React, { useState, useMemo } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider, CssBaseline, IconButton, Box } from '@mui/material';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import GitHubIcon from '@mui/icons-material/GitHub';
import HomePage from './pages/HomePage';
import { createLightTheme, createDarkTheme } from './theme';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  const [mode, setMode] = useState<'dark' | 'light'>('dark');

  const theme = useMemo(() => {
    return mode === 'dark' ? createDarkTheme() : createLightTheme();
  }, [mode]);

  const toggleColorMode = () => {
    setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
  };

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box
          sx={{
            position: 'fixed',
            top: 16,
            right: 16,
            zIndex: 9999,
            display: 'flex',
            gap: 1,
            transform: 'translateZ(0)',
            willChange: 'transform',
          }}
        >
          <IconButton
            href="https://github.com/razaool/trading-probabilities"
            target="_blank"
            rel="noopener noreferrer"
            color="inherit"
            sx={{
              bgcolor: 'background.paper',
              boxShadow: 3,
              '&:hover': {
                bgcolor: 'background.default',
              },
            }}
          >
            <GitHubIcon />
          </IconButton>
          <IconButton
            onClick={toggleColorMode}
            color="inherit"
            sx={{
              bgcolor: 'background.paper',
              boxShadow: 3,
              '&:hover': {
                bgcolor: 'background.default',
              },
            }}
          >
            {mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
          </IconButton>
        </Box>
        <Router>
          <Routes>
            <Route path="/" element={<HomePage />} />
          </Routes>
        </Router>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
