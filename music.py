import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.io import wavfile
import mpmath
import os

#-- Create the list of musical notes
scale = [] 
for k in range(35, 65): 
    note = 440 * 2**((k-49)/12)
    if k % 12 != 0 and k % 12 != 2 and k % 12 != 5 and k % 12 != 7 and k % 12 != 10:
        scale.append(note) # add musical note (skip half tones)
n_notes = len(scale) # number of musical notes

#-- Generate the data
n = 400
sigma = 0.2
min_t = 200000
max_t = 500020

def create_data(f, nobs, min_t, max_t, sigma):
    z_real = []
    z_imag = []
    z_modulus = []
    incr_t = (max_t - min_t) / nobs
    for t in np.arange(min_t, max_t, incr_t):   
        if f == 'Zeta':
            z = mpmath.zeta(complex(sigma, t))
        elif f == 'Eta':
            z = mpmath.altzeta(complex(sigma, t))
        z_real.append(float(z.real))
        z_imag.append(float(z.imag))
        modulus = np.sqrt(z.real * z.real + z.imag * z.imag)
        z_modulus.append(float(modulus))
    return (z_real, z_imag, z_modulus)

(z_real, z_imag, z_modulus) = create_data('Eta', n, min_t, max_t, sigma) 

size = len(z_real) # should be identical to nobs
x = np.arange(size)

# frequency of each note     
y = z_real    
min_y = np.min(y)
max_y = np.max(y)
yf = 0.999 * n_notes * (y - min_y) / (max_y - min_y) 
 
# duration of each note
z = z_imag  
min_z = np.min(z)
max_z = np.max(z)
zf = 0.1 + 0.4 * (z - min_z) / (max_z - min_z) 

# volume of each note
v = z_modulus 
min_v = np.min(v)
max_v = np.max(v)
vf = 500 + 2000 * (1 - (v - min_v) / (max_v - min_v)) 

#-- plot data
mpl.rcParams['axes.linewidth'] = 0.3
fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=7)
ax.tick_params(axis='y', labelsize=7) 
plt.rcParams['axes.linewidth'] = 0.1
plt.plot(x, y, color='red', linewidth = 0.3)
plt.plot(x, z, color='blue', linewidth = 0.3)
plt.plot(x, v, color='green', linewidth = 0.3)
plt.legend(['frequency','duration','volume'], fontsize="7", 
    loc ="upper center", ncol=3)
plt.show()

#-- Turn the data into music
def get_sine_wave(frequency, duration, sample_rate=44100, amplitude=4096):
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

wave = []
for t in x: # loop over dataset observations, create one note per observation
    note = int(yf[t])
    duration = zf[t]
    frequency = scale[note]    
    volume = vf[t]  # 2048
    new_wave = get_sine_wave(frequency, duration=zf[t], amplitude=vf[t])
    wave = np.concatenate((wave, new_wave))

# Save the file and check for errors
try:
    wavfile.write('sound1.wav', rate=44100, data=wave.astype(np.int16))
    print("File written successfully to:", os.getcwd())
except Exception as e:
    print(f"Error writing file: {e}")
