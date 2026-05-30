# BIO-518: Humanity Preservation Threshold Analysis

## Model

$$H(\alpha) = \frac{1}{1 + e^{-k(\alpha_0 - \alpha)}}$$

- Threshold central: $\alpha_0 = 0.5$
- Slope: $k = 10.0$
- Humanity threshold: $H_{\text{critical}} = 0.7$

## Sensitivity

$$\frac{dH}{d\alpha} = k \cdot H \cdot (1 - H)$$

## Results

- Within threshold: 6 tasks
- Beyond threshold: 9 tasks

### Within Threshold Tasks

- BIO-507
- BIO-502
- BIO-505
- BIO-506
- BIO-504
- BIO-510

### Beyond Threshold Tasks

- BIO-511
- BIO-513
- BIO-520
- BIO-501
- BIO-503
- BIO-512
- BIO-508
- BIO-509
- BIO-516

## Graph Description

### Figure 1: Humanity Index Curve

Shows the sigmoid function H(α) with threshold line at H=0.7.
Green region: within threshold, Red region: beyond threshold.

### Figure 2: Sensitivity Analysis

Derivative dH/dα showing maximum sensitivity at α₀=0.5.

### Figure 3: Humanity Index by Task

Horizontal bar chart showing each task's humanity index.
Green bars: within threshold, Red bars: beyond threshold.

### Figure 4: Modification vs Humanity Index

Scatter plot with color gradient showing task distribution.
Color: green (high humanity) to red (low humanity).
