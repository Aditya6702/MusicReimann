import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import mpmath
from scipy.io import wavfile
import io
import base64

# Set page config
st.set_page_config(page_title="Riemann Zeta Explorer & Music Generator", layout="wide")

# Custom CSS to make the app more attractive
st.markdown("""
<style>
    .stApp {
        background-color: #f0f0f5;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    h1, h2 {
        color: #1e3d59;
    }
    .stButton>button {
        background-color: #ff6e40;
        color: white;
    }
    .stSlider {
        color: #1e3d59;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(np.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def riemann_zeta(s, t):
    return mpmath.zeta(complex(s, t))

def get_sine_wave(frequency, duration, sample_rate=44100, amplitude=4096):
    frequency = float(frequency)
    duration = float(duration)
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

def create_music_from_zeta(zeta_values, duration_scale=0.1, freq_min=220, freq_max=880):
    wave = np.array([])
    for z in zeta_values:
        z_real = float(z.real)
        z_imag = float(z.imag)
        magnitude = abs(float(z))
        frequency = freq_min + (magnitude % (freq_max - freq_min))
        duration = duration_scale * (1 + (abs(z_imag) % 1))
        volume = 2048 + 2048 * (magnitude % 1)
        new_wave = get_sine_wave(frequency, duration, amplitude=volume)
        wave = np.concatenate((wave, new_wave))
    return wave

# Main app
st.title("🎵 Riemann Zeta Explorer & Music Generator 🧮")

# Sidebar
st.sidebar.header("Parameters")
n_primes = st.sidebar.slider("Number of primes to generate", 10, 1000, 100)
max_t = st.sidebar.slider("Maximum t value for zeta function", 10, 100, 50)
s_value = st.sidebar.slider("Real part of s (usually 0.5 for critical line)", 0.1, 1.0, 0.5, 0.1)
duration_scale = st.sidebar.slider("Music duration scale", 0.01, 0.5, 0.1, 0.01)
sample_rate = st.sidebar.slider("Sample rate for music", 22050, 96000, 44100, 1000)

# Generate data
primes = generate_primes(n_primes)
t_values = np.linspace(0, max_t, 1000)
zeta_values = [riemann_zeta(s_value, t) for t in t_values]
zeta_values = [complex(z) for z in zeta_values]
zeta_abs_values = [abs(z) for z in zeta_values]

x_values = np.linspace(2, max(primes), 1000)
pi_x = [sum(1 for p in primes if p <= x) for x in x_values]

# Create plots
col1, col2 = st.columns(2)

with col1:
    st.subheader("Riemann Zeta Function")
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.plot(t_values, zeta_abs_values, color='#ff6e40')
    ax1.set_title(f"Absolute value of ζ({s_value} + it)")
    ax1.set_xlabel("t")
    ax1.set_ylabel("|ζ(s)|")
    ax1.grid(True, alpha=0.3)
    st.pyplot(fig1)

with col2:
    st.subheader("Prime-counting Function")
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.plot(x_values, pi_x, color='#1e3d59')
    ax2.scatter(primes, range(1, len(primes) + 1), color='#ff6e40', s=20)
    ax2.set_title("Prime-counting function π(x)")
    ax2.set_xlabel("x")
    ax2.set_ylabel("π(x)")
    ax2.grid(True, alpha=0.3)
    st.pyplot(fig2)

# Generate music
if st.button("Generate Music"):
    st.subheader("🎶 Generated Music")
    wave = create_music_from_zeta(zeta_values, duration_scale, freq_min=220, freq_max=880)
    wave = np.int16(wave / np.max(np.abs(wave)) * 32767)
    
    # Save as WAV file
    buffer = io.BytesIO()
    wavfile.write(buffer, rate=sample_rate, data=wave)
    buffer.seek(0)
    
    # Create download link
    b64 = base64.b64encode(buffer.getvalue()).decode()
    href = f'<a href="data:audio/wav;base64,{b64}" download="zeta_music.wav">Download WAV</a>'
    st.markdown(href, unsafe_allow_html=True)
    
    # Display audio player
    st.audio(buffer, format='audio/wav')

# Prime number data
st.subheader("Prime Number Insights")
col3, col4, col5 = st.columns(3)
with col3:
    st.metric("First Prime", primes[0])
with col4:
    st.metric(f"{n_primes}th Prime", primes[-1])
with col5:
    st.metric("π(100)", sum(1 for p in primes if p <= 100))

# Explanation
st.subheader("📚 About This App")
st.write("""
This app explores the fascinating connection between the Riemann zeta function, prime numbers, and music:

1. **Riemann Zeta Function**: The graph shows the absolute value of ζ(s) along the line s = σ + it. The critical line (σ = 0.5) is of particular interest in the Riemann Hypothesis.

2. **Prime-counting Function**: π(x) counts the number of primes less than or equal to x. The red dots represent actual prime numbers.

3. **Music Generation**: We create a unique musical interpretation of the zeta function:
   - Frequency: Based on the magnitude of zeta
   - Duration: Influenced by the imaginary part of zeta
   - Volume: Also derived from the magnitude of zeta

Adjust the parameters in the sidebar to explore different aspects of this relationship and generate various musical interpretations. Listen for patterns in the music that might correspond to features in the zeta function plot!
""")

st.sidebar.info("Explore the connection between mathematics and music by adjusting the parameters and generating unique compositions!")
