import numpy as np
import matplotlib.pyplot as plt
import mpmath

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

# Generate prime numbers
n_primes = 100
primes = generate_primes(n_primes)

# Calculate zeta function values
s = 0.5  # Real part of s (critical line)
t_values = np.linspace(0, 50, 1000)  # Imaginary part of s
zeta_values = [abs(riemann_zeta(s, t)) for t in t_values]

# Calculate prime-counting function
x_values = np.linspace(2, max(primes), 1000)
pi_x = [sum(1 for p in primes if p <= x) for x in x_values]

# Plot results
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Plot Riemann zeta function
ax1.plot(t_values, zeta_values)
ax1.set_title(f"Absolute value of Riemann zeta function ζ({s} + it)")
ax1.set_xlabel("t")
ax1.set_ylabel("|ζ(s)|")

# Plot prime-counting function
ax2.plot(x_values, pi_x)
ax2.scatter(primes, range(1, len(primes) + 1), color='red', s=20)
ax2.set_title("Prime-counting function π(x)")
ax2.set_xlabel("x")
ax2.set_ylabel("π(x)")

plt.tight_layout()
plt.show()

# Print some interesting points
print(f"First 10 prime numbers: {primes[:10]}")
print(f"100th prime number: {primes[-1]}")
print(f"π(100) = {sum(1 for p in primes if p <= 100)}")
