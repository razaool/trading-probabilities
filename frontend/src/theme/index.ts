import { createTheme } from '@mui/material/styles';

export const createLightTheme = () =>
  createTheme({
    palette: {
      mode: 'light',
      primary: {
        main: '#1976d2',
      },
      secondary: {
        main: '#dc004e',
      },
      background: {
        default: '#f5f5f5',
        paper: '#ffffff',
      },
    },
    typography: {
      fontFamily: [
        '-apple-system',
        'BlinkMacSystemFont',
        '"Segoe UI"',
        'Roboto',
        '"Helvetica Neue"',
        'Arial',
        'sans-serif',
      ].join(','),
    },
    components: {
      MuiContainer: {
        styleOverrides: {
          root: {
            paddingTop: '2rem',
            paddingBottom: '2rem',
          },
        },
      },
    },
  });

export const createDarkTheme = () =>
  createTheme({
    palette: {
      mode: 'dark',
      primary: {
        main: '#90caf9',
      },
      secondary: {
        main: '#f48fb1',
      },
      background: {
        default: '#121212',
        paper: '#1e1e1e',
      },
    },
    typography: {
      fontFamily: [
        '-apple-system',
        'BlinkMacSystemFont',
        '"Segoe UI"',
        'Roboto',
        '"Helvetica Neue"',
        'Arial',
        'sans-serif',
      ].join(','),
    },
    components: {
      MuiContainer: {
        styleOverrides: {
          root: {
            paddingTop: '2rem',
            paddingBottom: '2rem',
          },
        },
      },
    },
  });

export default createDarkTheme();
