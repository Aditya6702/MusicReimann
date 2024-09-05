import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from scipy.io import wavfile
import mpmath

def show_app1():
    st.title("Musical Note Generator")

    # Create the list of musical notes
    scale = [] 
    for k in range(35, 65): 
        note = 440 * 2 ** ((k - 49) / 12)
        # Only include notes that are not half tones
        if k % 12 not in [0, 2, 5, 7, 10]:
            scale.append(note)
    n_notes = len(scale)  # Number of musical notes

    # Generate the data
    def create_data(f, nobs, min_t, max_t, sigma):
        z_real = []
        z_imag = []
        z_modulus = []
        incr_t = (max_t - min_t) / nobs
        for t in np.linspace(min_t, max_t, nobs):   
            if f == 'Zeta':
                z = mpmath.zeta(complex(sigma, t))
            elif f == 'Eta':
                z = mpmath.altzeta(complex(sigma, t))
            z_real.append(float(z.real))
            z_imag.append(float(z.imag))
            modulus = np.sqrt(z.real ** 2 + z.imag ** 2)
            z_modulus.append(float(modulus))
        return z_real, z_imag, z_modulus

    # UI components
    n = st.slider('Number of Observations', min_value=100, max_value=1000, value=300)
    sigma = st.slider('Sigma', min_value=0.1, max_value=5.0, value=0.5)
    min_t = st.slider('Minimum Time', min_value=0, max_value=1000, value=0)
    max_t = st.slider('Maximum Time', min_value=0, max_value=1000, value=1000)

    data_function = st.selectbox('Select function', ['Eta', 'Zeta'])

    if st.button('Generate Data'):
        z_real, z_imag, z_modulus = create_data(data_function, n, min_t, max_t, sigma)

        # Plot data
        size = len(z_real)
        x = np.arange(size)

        y = z_real    
        min_y = np.min(y)
        max_y = np.max(y)
        yf = 0.999 * (y - min_y) / (max_y - min_y) * (n_notes - 1)

        z = z_imag  
        min_z = np.min(z)
        max_z = np.max(z)
        zf = 0.1 + 0.4 * (z - min_z) / (max_z - min_z)

        v = z_modulus 
        min_v = np.min(v)
        max_v = np.max(v)
        vf = 500 + 2000 * (1 - (v - min_v) / (max_v - min_v))

        # Plot
        fig, ax = plt.subplots()
        ax.tick_params(axis='x', labelsize=7)
        ax.tick_params(axis='y', labelsize=7) 
        ax.plot(x, y, color='red', linewidth=0.3, label='Frequency')
        ax.plot(x, z, color='blue', linewidth=0.3, label='Duration')
        ax.plot(x, v, color='green', linewidth=0.3, label='Volume')
        ax.legend(fontsize="7", loc="upper center", ncol=3)
        st.pyplot(fig)

        # Generate the audio
        def get_sine_wave(frequency, duration, sample_rate=44100, amplitude=4096):
            t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
            wave = amplitude * np.sin(2 * np.pi * frequency * t)
            return wave

        wave = np.array([])
        for t in x:
            note = int(yf[t])
            duration = zf[t]
            frequency = scale[note] if note < n_notes else scale[-1]  # Handle out of range notes
            volume = vf[t]
            new_wave = get_sine_wave(frequency, duration, amplitude=volume)
            wave = np.concatenate((wave, new_wave))

        # Normalize and save the audio
        wave = np.int16(wave / np.max(np.abs(wave)) * 32767)
        wavfile.write('sound.wav', rate=44100, data=wave)
        st.audio('sound.wav', format='audio/wav')

    
if __name__ == "__main__":
    show_app1()
