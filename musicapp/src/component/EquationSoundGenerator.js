import React, { useState, useEffect, useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Button, Select, MenuItem, Card, CardHeader, CardContent, Typography, Slider, Container, Divider } from '@mui/material';

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

  const handleRedirect = () => {
    window.location.href = 'http://localhost:8501/'; // Replace with your desired URL
  };

  return (
    <Container maxWidth="md">
      <Card sx={{ marginTop: 4 }}>
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
          <Button variant="contained" onClick={handleRedirect} sx={{ mt: 2, ml: 2 }}>
            Zeta Function
          </Button>
        </CardContent>
      </Card>
      
      <Divider sx={{ my: 4 }} />

      <Card sx={{ marginTop: 4 }}>
        <CardHeader title="The Symphony of Mathematics" />
        <CardContent>
          <Typography variant="h6" gutterBottom>
            The Symphony of Mathematics: Transforming Mathematical Functions into Music
          </Typography>
          <Typography paragraph>
            Mathematics, often perceived as an abstract realm of numbers and formulas, finds a harmonious intersection with art through the transformation of mathematical functions into music. This innovative concept not only deepens our understanding of mathematical principles but also unveils new perspectives on how we perceive and appreciate both disciplines.
          </Typography>
          <Typography paragraph>
            <strong>Bridging the Abstract and the Artistic</strong>
          </Typography>
          <Typography paragraph>
            Mathematical functions, such as sine waves, exponential curves, and logarithmic spirals, are fundamental to the structure of our universe. When these functions are interpreted as musical elements, they create a unique symphony that bridges the abstract world of mathematics with the tangible experience of music.
          </Typography>
          <Typography paragraph>
            <strong>Sine Waves: The Musical Foundation</strong>
          </Typography>
          <Typography paragraph>
            Sine waves, characterized by their smooth periodic oscillations, are the building blocks of sound waves. In music, these waves correspond to pure tones. By mapping sine functions to musical notes, we can translate their continuous, predictable nature into harmonious melodies. This not only exemplifies the elegance of mathematical precision but also provides an auditory experience of its simplicity and beauty.
          </Typography>
          <Typography paragraph>
            <strong>Exponential and Logarithmic Functions: Dynamics and Growth</strong>
          </Typography>
          <Typography paragraph>
            Exponential and logarithmic functions describe processes of rapid growth or decay. In music, these functions can be used to create dynamic crescendos or gradual fades. For instance, an exponential function might control the intensity of a crescendo, gradually increasing the volume in a way that mirrors the natural escalation of excitement or emotion. Conversely, a logarithmic function might dictate the slow and steady decrease in volume, capturing the essence of a gentle, lingering finish.
          </Typography>
          <Typography paragraph>
            <strong>Quadratic and Cubic Functions: Rich Harmonic Structures</strong>
          </Typography>
          <Typography paragraph>
            Quadratic and cubic functions introduce more complex relationships, often resulting in intricate patterns and rich harmonic structures. These functions can be used to compose music with varying degrees of complexity and depth, reflecting the multifaceted nature of real-world phenomena. Their application in music composition can lead to evocative soundscapes that mirror the underlying mathematics of physical systems.
          </Typography>
          <Typography paragraph>
            <strong>Real-World Applications and Insights</strong>
          </Typography>
          <Typography paragraph>
            Transforming mathematical functions into music does more than just create interesting soundscapes; it offers tangible benefits and insights in various fields:
          </Typography>
          <Typography paragraph>
            <strong>Educational Tool:</strong> Integrating music with mathematical functions serves as an effective educational tool. By experiencing mathematical functions as musical compositions, students and enthusiasts can better grasp abstract concepts through auditory learning. This multisensory approach enhances comprehension and retention, making complex mathematical ideas more accessible and engaging.
          </Typography>
          <Typography paragraph>
            <strong>Scientific Visualization:</strong> In scientific research, converting data and functions into music provides an innovative way to visualize and interpret information. For instance, astrophysicists and biologists can use this method to uncover patterns and anomalies in their data that might be less obvious through traditional visualization techniques. Music becomes a powerful medium for data exploration and interpretation.
          </Typography>
          <Typography paragraph>
            <strong>A Harmonious Future:</strong> As we continue to explore the intersection of mathematics and music, we unlock new possibilities for understanding and appreciation. The symphony created by mathematical functions not only showcases the intrinsic beauty of mathematical relationships but also enriches our auditory experience. This harmonious blend of disciplines invites us to explore the profound connections between the abstract and the artistic, fostering a deeper appreciation for both mathematics and music.
          </Typography>
          <Typography paragraph>
            Embrace the rhythm of equations and let the melodies of functions inspire a new perspective on the world around us. Through this unique synthesis, we celebrate the beauty of mathematics in a way that resonates deeply with our senses and enriches our understanding of the universe.
          </Typography>
        </CardContent>
      </Card>
    </Container>
  );
};

export default EquationSoundGenerator;

