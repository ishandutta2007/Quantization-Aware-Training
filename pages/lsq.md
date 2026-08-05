# The Adaptive Scaling Era (Learned Step-Size Quantization / LSQ)

## Overview

Learned Step-Size Quantization (LSQ) introduced the quantization step-size interval directly as a learnable parameter optimized during backpropagation, rather than relying on rigid, pre-calculated clipping thresholds.

## Significance

This unlocked stable, ultra-low bit-width architectures (down to INT4 and INT2 combinations) by enabling the model to dynamically reshape its numerical boundaries alongside weight evolution.

## Diagram

```mermaid
flowchart TD
    Input[FP32 Weights / Activations] --> Scale[Apply Learnable Scale s]
    Scale --> Quantize[Quantize & Clip]
    Quantize --> Dequantize[Dequantize with s]
    Dequantize --> Output[Fake-Quantized Value]
    Loss -.->|Gradient updates s dynamically| Scale
```
