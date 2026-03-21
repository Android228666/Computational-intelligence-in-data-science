# Buffon's Needle Experiment - Pi Estimation 🧶

This project implements a **Monte Carlo simulation** of the classic Buffon's Needle problem to estimate the value of $\pi$.

## 📝 Project Overview

The experiment involves dropping a needle of length $L$ onto a floor with parallel lines separated by a distance $D$. By calculating the ratio of needles that cross a line to the total number of tosses, we can approximate the value of $\pi$.

### Mathematical Formula
The probability $P$ of a hit is given by:
$$P = \frac{2L}{\pi D}$$

From this, we derive the estimation for $\pi$:
$$\pi \approx \frac{2 \cdot L \cdot N}{D \cdot hits}$$

## 🚀 Features
- **Simulation Engine:** Efficient vectorized calculations using `numpy`.
- **Visualization:** A 2D plot showing hits (blue) and misses (red).
- **Convergence Analysis:** Boxplots showing how the estimation improves as the number of tosses ($N$) increases.

## 📊 Results Visualization

Open image in "Monte Carlo project" named "Simulation results"

## 🛠️ Requirements
To run this script, you need Python 3 and the following libraries:
```bash
pip install numpy matplotlib
