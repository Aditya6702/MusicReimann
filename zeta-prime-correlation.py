import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import mpmath
from scipy.io import wavfile
import io
import base64

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
    # Ensure frequency and duration are Python floats
    frequency = float(frequency)
    duration = float(duration)
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

def create_music_from_zeta(zeta_values, duration_scale=0.1, freq_min=220, freq_max=880):
    wave = np.array([])
    for z in zeta_values:
        # Convert mpmath mpf to Python float
        z_real = float(z.real)
        z_imag = float(z.imag)
        magnitude = abs(float(z))
        frequency = freq_min + (magnitude % (freq_max - freq_min))
        duration = duration_scale * (1 + (abs(z_imag) % 1))
        volume = 2048 + 2048 * (magnitude % 1)
        new_wave = get_sine_wave(frequency, duration, amplitude=volume)
        wave = np.concatenate((wave, new_wave))
    return wave

st.title("Riemann Zeta Function Explorer with Music")

st.sidebar.header("Parameters")
n_primes = st.sidebar.slider("Number of primes to generate", 10, 1000, 100)
max_t = st.sidebar.slider("Maximum t value for zeta function", 10, 100, 50)
s_value = st.sidebar.slider("Real part of s (usually 0.5 for critical line)", 0.1, 1.0, 0.5, 0.1)
duration_scale = st.sidebar.slider("Music duration scale", 0.01, 0.5, 0.1, 0.01)
sample_rate = st.sidebar.slider("Sample rate for music", 22050, 96000, 44100, 1000)

primes = generate_primes(n_primes)

t_values = np.linspace(0, max_t, 1000)
zeta_values = [riemann_zeta(s_value, t) for t in t_values]
zeta_values = [complex(z) for z in zeta_values]  # Ensure all values are complex numbers
zeta_abs_values = [abs(z) for z in zeta_values]

x_values = np.linspace(2, max(primes), 1000)
pi_x = [sum(1 for p in primes if p <= x) for x in x_values]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

ax1.plot(t_values, zeta_abs_values)
ax1.set_title(f"Absolute value of Riemann zeta function ζ({s_value} + it)")
ax1.set_xlabel("t")
ax1.set_ylabel("|ζ(s)|")

ax2.plot(x_values, pi_x)
ax2.scatter(primes, range(1, len(primes) + 1), color='red', s=20)
ax2.set_title("Prime-counting function π(x)")
ax2.set_xlabel("x")
ax2.set_ylabel("π(x)")

plt.tight_layout()
st.pyplot(fig)

st.header("Prime Number Data")
st.write(f"First 10 prime numbers: {primes[:10]}")
st.write(f"{n_primes}th prime number: {primes[-1]}")
st.write(f"π(100) = {sum(1 for p in primes if p <= 100)}")


st.header("Explanation")
st.write("""
This application demonstrates the connection between the Riemann zeta function, prime numbers, and music:

1. The top graph shows the absolute value of the Riemann zeta function along the line s = σ + it, where σ is the value you can adjust in the sidebar (typically 0.5 for the critical line).

2. The bottom graph shows the prime-counting function π(x), which counts the number of primes less than or equal to x. The red dots represent actual prime numbers.

3. The music generation is based on the complex values of the Riemann zeta function:
   - The frequency of each note is determined by the magnitude of zeta.
   - The duration of each note is influenced by the imaginary part of zeta.
   - The volume of each note is also based on the magnitude of zeta.

4. The resulting music is a unique auditory representation of the behavior of the Riemann zeta function. Listen for patterns and variations that might correspond to interesting features in the zeta function plot!

Adjust the parameters in the sidebar to explore different aspects of this relationship and generate different musical interpretations!
""")

st.sidebar.info("To run this app, save it as a .py file and run 'streamlit run your_file_name.py' in the terminal.")

