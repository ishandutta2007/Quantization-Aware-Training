# Weight-Only Quantization vs. Joint Weight-Activation QAT

## Overview

Weight-Only QAT focuses exclusively on compressing stationary static parameter states (e.g., INT4 weights) while retaining dynamic FP16 calculations. 

Joint Weight-Activation QAT targets high-throughput contexts by quantizing both parameters and moving runtime activations (e.g., INT8/INT8). This requires meticulous balancing due to unpredictable runtime outliers.

## Diagram

```mermaid
flowchart TD
    subgraph Weight-Only
        W1[INT4 Weights] --> MatMul1[FP16 MatMul]
        A1[FP16 Activations] --> MatMul1
    end
    subgraph Joint QAT
        W2[INT8 Weights] --> MatMul2[INT8 MatMul]
        A2[INT8 Activations] --> MatMul2
    end
```
