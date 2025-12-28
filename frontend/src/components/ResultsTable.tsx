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
  Chip,
  TablePagination,
} from '@mui/material';
import type { QueryResponse } from '../types/api';

interface ResultsTableProps {
  data: QueryResponse;
}

function formatPercentage(value: number | null | undefined): string {
  if (value === null || value === undefined) return 'N/A';
  return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
}

export default function ResultsTable({ data }: ResultsTableProps) {
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(25);

  const timeHorizons = Object.keys(data.summary_statistics);
  const horizonOrder = ['1d', '1w', '1m', '1y'].filter(h => h in data.summary_statistics);

  const handleChangePage = (event: React.MouseEvent<HTMLButtonElement> | null, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const paginatedInstances = data.instances.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  return (
    <Paper
      elevation={0}
      sx={{
        p: { xs: 2, sm: 3 },
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
      <Box sx={{ mb: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 600, fontSize: { xs: '1.1rem', sm: '1.25rem' } }}>
          Historical Occurrences
        </Typography>
      </Box>

      <TableContainer sx={{ overflowX: 'auto' }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell
                sx={{
                  borderBottom: '2px solid',
                  borderColor: 'divider',
                  fontWeight: 600,
                  fontSize: { xs: '0.7rem', sm: '0.875rem' },
                  padding: { xs: '6px 4px', sm: '16px' },
                }}
              >
                Date
              </TableCell>
              {horizonOrder.map((horizon) => (
                <TableCell
                  key={horizon}
                  align="right"
                  sx={{
                    borderBottom: '2px solid',
                    borderColor: 'divider',
                    fontWeight: 600,
                    fontSize: { xs: '0.7rem', sm: '0.875rem' },
                    padding: { xs: '6px 4px', sm: '16px' },
                  }}
                >
                  {horizon.toUpperCase()}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {paginatedInstances.map((instance, index) => (
              <TableRow
                key={index}
                sx={{
                  transition: 'all 0.2s ease',
                  '&:hover': {
                    bgcolor: 'rgba(0, 0, 0, 0.04)',
                    transform: 'scale(1.01)',
                  },
                }}
              >
                <TableCell
                  component="th"
                  scope="row"
                  sx={{
                    fontWeight: 500,
                    borderBottom: '1px solid',
                    borderColor: 'divider',
                    fontSize: { xs: '0.7rem', sm: '0.875rem' },
                    padding: { xs: '6px 4px', sm: '16px' },
                  }}
                >
                  {instance.date}
                </TableCell>
                {horizonOrder.map((horizon) => {
                  const value = instance.forward_returns[horizon];
                  const isPositive = value !== null && value !== undefined && value >= 0;
                  return (
                    <TableCell
                      key={horizon}
                      align="right"
                      sx={{
                        fontWeight: 600,
                        color: isPositive ? '#2e7d32' : '#d32f2f',
                        borderBottom: '1px solid',
                        borderColor: 'divider',
                        fontSize: { xs: '0.7rem', sm: '0.875rem' },
                        padding: { xs: '6px 4px', sm: '16px' },
                      }}
                    >
                      {formatPercentage(value)}
                    </TableCell>
                  );
                })}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <TablePagination
        rowsPerPageOptions={[10, 25, 50, 100]}
        component="div"
        count={data.instances.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
        sx={{
          '.MuiTablePagination-root': {
            fontSize: { xs: '0.75rem', sm: '0.875rem' },
          },
          '.MuiTablePagination-select': {
            paddingTop: 1,
            paddingBottom: 1,
            fontSize: { xs: '0.75rem', sm: '0.875rem' },
          },
          '.MuiTablePagination-selectLabel, .MuiTablePagination-displayedRows': {
            fontSize: { xs: '0.75rem', sm: '0.875rem' },
          },
          '.MuiTablePagination-selectLabel': {
            margin: 0,
          },
          '.MuiTablePagination-displayedRows': {
            margin: 0,
          },
          '.MuiTablePagination-actions': {
            marginLeft: { xs: 0, sm: 0 },
          },
          '.MuiTablePagination-spacer': {
            flex: 1,
          },
        }}
      />
    </Paper>
  );
}
