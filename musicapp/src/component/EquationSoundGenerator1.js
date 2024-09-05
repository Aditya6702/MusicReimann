import React, { useState, useEffect, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Button, Select, MenuItem, Card, CardHeader, CardContent, Typography, Slider } from '@mui/material';

const equations = ['Sine', 'Cosine', 'Tangent', 'Exponential', 'Logarithm', 'Square Root', 'Quadratic', 'Cubic'];

const EquationSoundGenerator = () => {
  const [selectedEquation, setSelectedEquation] = useState('Sine');
  const [data, setData] = useState([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [duration, setDuration] = useState(5);
  const audioContextRef = useRef();
  const oscillatorRef = useRef();
  const gainNodeRef = useRef();

  useEffect(() => {
    generateData();
  }, [selectedEquation, duration]);

  const generateData = () => {
    const n = 400;
    const minT = 0;
    const maxT = duration;
    const t = Array.from({ length: n }, (_, i) => minT + (i / (n - 1)) * (maxT - minT));

    let z;
    switch (selectedEquation) {
      case 'Sine':
        z = t.map(Math.sin);
        break;
      case 'Cosine':
        z = t.map(Math.cos);
        break;
      case 'Tangent':
        z = t.map(v => Math.min(Math.max(Math.tan(v), -100), 100));
        break;
      case 'Exponential':
        z = t.map(v => Math.min(Math.exp(v), 1e100));
        break;
      case 'Logarithm':
        z = t.map(v => Math.log(Math.abs(v) + 1));
        break;
      case 'Square Root':
        z = t.map(v => Math.sqrt(Math.abs(v)));
        break;
      case 'Quadratic':
        z = t.map(v => v ** 2);
        break;
      case 'Cubic':
        z = t.map(v => v ** 3);
        break;
      default:
        z = t.map(Math.sin);
    }

    const newData = t.map((value, index) => ({
      t: value,
      z: z[index],
    }));

    setData(newData);
  };

  const playSound = () => {
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
    }

    if (isPlaying) {
      oscillatorRef.current.stop();
      gainNodeRef.current.disconnect();
      setIsPlaying(false);
      return;
    }

    const audioContext = audioContextRef.current;
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator.type = 'sine';
    oscillator.frequency.setValueAtTime(440, audioContext.currentTime);
    gainNode.gain.setValueAtTime(0.5, audioContext.currentTime);

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    const now = audioContext.currentTime;
    data.forEach(({ t, z }) => {
      const time = now + t;
      const frequency = Math.abs(z) * 140 + 110; // Scale frequency between 110Hz and 990Hz
      oscillator.frequency.setValueAtTime(frequency, time);
    });

    oscillator.start();
    oscillator.stop(now + duration);

    oscillatorRef.current = oscillator;
    gainNodeRef.current = gainNode;

    setIsPlaying(true);

    oscillator.onended = () => {
      setIsPlaying(false);
    };
  };

  return (
    <Card sx={{ maxWidth: 800, margin: 'auto', mt: 4 }}>
      <CardHeader title="Equation Sound Generator" />
      <CardContent>
        <Select
          value={selectedEquation}
          onChange={(e) => setSelectedEquation(e.target.value)}
          fullWidth
          sx={{ mb: 2 }}
        >
          {equations.map((eq) => (
            <MenuItem key={eq} value={eq}>{eq}</MenuItem>
          ))}
        </Select>
        <Typography gutterBottom>Duration: {duration} seconds</Typography>
        <Slider
          value={duration}
          onChange={(_, newValue) => setDuration(newValue)}
          min={1}
          max={10}
          step={1}
          marks
          valueLabelDisplay="auto"
          sx={{ mb: 2 }}
        />
        <div style={{ height: 400, width: '100%' }}>
          <ResponsiveContainer>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="t" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="z" stroke="#8884d8" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <Button variant="contained" onClick={playSound} sx={{ mt: 2 }}>
          {isPlaying ? 'Stop Sound' : 'Play Sound'}
        </Button>
      </CardContent>
    </Card>
  );
};

export default EquationSoundGenerator;