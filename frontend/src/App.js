import React, { useState } from 'react';
import {
  Container, Typography, Button, Paper, Alert, Stack
} from '@mui/material';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';

function App() {
  const [file, setFile] = useState(null);
  const [startTime, setStartTime] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please upload a CSV file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    if (startTime) {
      // Convert to "YYYY-MM-DD HH:MM:SS"
      const formatted = startTime.toISOString().slice(0, 19).replace('T', ' ');
      formData.append('start_time', formatted);
    }

    try {
      const response = await fetch('http://localhost:5000/delineation', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (data.error) {
        setError(data.error);
        setResult(null);
        return;
      }
      setResult(data);
      setError('');
    } catch (err) {
      setError('Failed to fetch results.');
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Container maxWidth="sm" sx={{ mt: 5 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" gutterBottom>
            Delineation reader
          </Typography>

          <form onSubmit={handleSubmit}>
            <Stack spacing={2}>
              <Button variant="contained" component="label">
                Upload CSV File
                <input
                  type="file"
                  accept=".csv"
                  hidden
                  onChange={(e) => setFile(e.target.files[0])}
                />
              </Button>

              {file && (
                <Typography variant="body2" color="textSecondary">
                  Selected file: {file.name}
                </Typography>
              )}

              <DateTimePicker
                label="Recording Start Time"
                value={startTime}
                onChange={(newValue) => setStartTime(newValue)}
                renderInput={(params) => <params.TextField {...params} />}
              />

              <Button variant="contained" type="submit">
                Submit
              </Button>
            </Stack>
          </form>

          {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}

          {result && (
            <Paper elevation={1} sx={{ mt: 4, p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Results
              </Typography>
              <Stack spacing={1}>
                  <Typography><strong>Mean HR:</strong> {result.mean_hr} bpm</Typography>
                  <Typography>
                    <strong>Min HR:</strong> {result.min_hr} bpm at{" "}
                    {result.min_time ? result.min_time : `${result.min_time_ms} ms`}
                  </Typography>

                  <Typography>
                    <strong>Max HR:</strong> {result.max_hr} bpm at{" "}
                    {result.max_time ? result.max_time : `${result.max_time_ms} ms`}
                  </Typography>
                  
                {"warning" in result && (
                  <Alert severity="warning">{result.warning}</Alert>
                )}
              </Stack>
            </Paper>
          )}


        </Paper>
      </Container>
    </LocalizationProvider>
  );
}

export default App;
