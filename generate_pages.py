import os

pages_dir = "pages"
if not os.path.exists(pages_dir):
    os.makedirs(pages_dir)

pages = {
    "post_training_truncation.md": {
        "title": "The Post-Training Truncation Era",
        "content": "## Overview\n\nIn the early days of neural network deployment, Post-Training Quantization (PTQ) was the dominant method for compression. Models were trained natively using high-precision FP32 or FP16. After training concluded, a separate offline process mapped continuous floating-point values into localized integer formats.\n\n## Limitations\n\nThis approach created massive mathematical rounding drops and severe accuracy degradation in memory-starved architectures. It failed to account for out-of-distribution outlier activations, rendering ultra-low bit-width deployments non-viable.\n\n## Diagram\n\n```mermaid\nflowchart TD\n    A[FP32 Model Trained] --> B[Offline Quantization]\n    B --> C[Truncation / Rounding]\n    C --> D[INT8 Model]\n    D --> E[Accuracy Drop & Outlier Loss]\n```\n"
    },
    "ste_qat.md": {
        "title": "The Simulated Noise Revolution (Straight-Through Estimator QAT)",
        "content": "## Overview\n\nQuantization-Aware Training (QAT) using the Straight-Through Estimator (STE) revolutionized model compression by injecting fake quantization nodes during the forward pass. This allowed the model to experience low-precision rounding errors natively while accumulating parameter adjustments.\n\n## Significance\n\nIt solved the zero-gradient paradox of discrete step-functions by bypassing non-differentiable rounding operators during the backward pass using a Straight-Through Estimator (STE), bridging the gap between hardware constraints and gradient descent.\n\n## Diagram\n\n```mermaid\nflowchart LR\n    Forward[Forward Pass: Fake Quantization] --> Loss[Loss Calculation]\n    Loss --> Backward[Backward Pass: STE Bypass]\n    Backward --> Update[Weight Update in FP32]\n    Update --> Forward\n```\n"
    },
    "lsq.md": {
        "title": "The Adaptive Scaling Era (Learned Step-Size Quantization / LSQ)",
        "content": "## Overview\n\nLearned Step-Size Quantization (LSQ) introduced the quantization step-size interval directly as a learnable parameter optimized during backpropagation, rather than relying on rigid, pre-calculated clipping thresholds.\n\n## Significance\n\nThis unlocked stable, ultra-low bit-width architectures (down to INT4 and INT2 combinations) by enabling the model to dynamically reshape its numerical boundaries alongside weight evolution.\n\n## Diagram\n\n```mermaid\nflowchart TD\n    Input[FP32 Weights / Activations] --> Scale[Apply Learnable Scale s]\n    Scale --> Quantize[Quantize & Clip]\n    Quantize --> Dequantize[Dequantize with s]\n    Dequantize --> Output[Fake-Quantized Value]\n    Loss --> UpdateS[Gradient updates s dynamically]\n```\n"
    },
    "uniform_asymmetric_quantization.md": {
        "title": "The Uniform Asymmetric Quantization Operator",
        "content": "## Overview\n\nThe Uniform Asymmetric Quantization Operator maps a real floating-point value into an integer range using a scale factor and an integer zero-point offset. This allows for representing asymmetric distributions (e.g., ReLU activations) more effectively than symmetric quantization.\n\n## Mathematics\n\nThe transformation is defined as:\n\n$$q = \\text{clamp}\\left( \\left\\lfloor \\frac{r}{S} \\right\\rceil + Z, q_{\\min}, q_{\\max} \\right)$$\n\nWhere $S$ is the scale and $Z$ is the zero-point.\n\n## Diagram\n\n```mermaid\nflowchart TD\n    R[Real Value r] --> Div[Divide by Scale S]\n    Div --> Round[Round to Nearest Integer]\n    Round --> AddZ[Add Zero Point Z]\n    AddZ --> Clamp[Clamp to Range]\n    Clamp --> Q[Quantized Value q]\n```\n"
    },
    "ste.md": {
        "title": "The Straight-Through Estimator (STE)",
        "content": "## Overview\n\nThe standard rounding operator is a step function with a derivative of zero almost everywhere, which would cause backpropagation to completely stall. The Straight-Through Estimator (STE) is a technique that replaces the non-differentiable gradient with an identity mapping matrix during the backward pass.\n\n## Mechanism\n\nThis forces the high-precision floating-point master weights to absorb fine-grained gradient updates while the forward pass evaluates strictly simulated low-precision outcomes.\n\n## Diagram\n\n```mermaid\nflowchart LR\n    subgraph Forward Pass\n        X --> Round[Rounding Operation] --> Y\n    end\n    subgraph Backward Pass\n        dY --> Identity[Identity Mapping STE] --> dX\n    end\n```\n"
    },
    "weight_only_vs_joint.md": {
        "title": "Weight-Only Quantization vs. Joint Weight-Activation QAT",
        "content": "## Overview\n\nWeight-Only QAT focuses exclusively on compressing stationary static parameter states (e.g., INT4 weights) while retaining dynamic FP16 calculations. \n\nJoint Weight-Activation QAT targets high-throughput contexts by quantizing both parameters and moving runtime activations (e.g., INT8/INT8). This requires meticulous balancing due to unpredictable runtime outliers.\n\n## Diagram\n\n```mermaid\nflowchart TD\n    subgraph Weight-Only\n        W1[INT4 Weights] --> MatMul1[FP16 MatMul]\n        A1[FP16 Activations] --> MatMul1\n    end\n    subgraph Joint QAT\n        W2[INT8 Weights] --> MatMul2[INT8 MatMul]\n        A2[INT8 Activations] --> MatMul2\n    end\n```\n"
    },
    "non_uniform_qat.md": {
        "title": "Non-Uniform & Outlier-Aware QAT",
        "content": "## Overview\n\nModern foundation architectures exhibit massive activation spikes in isolated channels. Modern QAT variants mathematically isolate these critical outlier tokens into protected high-precision islands (FP16), while forcing the remaining 99% of standard background distribution channels into dense low-precision blocks.\n\n## Approach\n\nTechniques like NormalFloat and Outlier-Protected Tuning ensure that the model retains performance by not overly penalizing the few essential features that drive model predictions.\n\n## Diagram\n\n```mermaid\npie title Token Distribution Allocation\n    \"Low-Precision Dense Blocks (INT4/INT8)\" : 99\n    \"High-Precision Islands (FP16 Outliers)\" : 1\n```\n"
    },
    "weight_instability_loop.md": {
        "title": "The Float-Integer Master Weight Instability Loop",
        "content": "## Overview\n\nBecause gradient updates are incredibly fine-grained, modifying floating-point master weights by fractions may not alter their discrete quantized equivalent in the forward pass. This creates stuck gradients and oscillating loss patterns during deep fine-tuning.\n\n## Mitigation\n\nImplementing **Stochastic Rounding** or utilizing progressive learning rate warm-up schedules coupled with weight decay regularization gently smooths out parameter jumps and stabilizes the training process.\n\n## Diagram\n\n```mermaid\nflowchart LR\n    Stuck[Stuck Gradients] --> Detect[Detect Oscillation]\n    Detect --> SR[Apply Stochastic Rounding]\n    Detect --> LR[Apply LR Warm-up / Decay]\n    SR --> Stable[Stabilized Convergence]\n    LR --> Stable\n```\n"
    },
    "hardware_kernel_divergence.md": {
        "title": "The Hardware Kernel Generation Divergence",
        "content": "## Overview\n\nSimulating quantization in framework tools like PyTorch or TensorFlow does not automatically translate into real-world inference speedups. If target hardware lacks explicit Tensor Core support for mixed operations (e.g., INT4 matrix math multiplication), the network will suffer execution delays.\n\n## Mitigation\n\nDeploying custom compilation backends like **TensorRT**, **ONNX Runtime**, or **Apache TVM**. These compile the trained fake-quantization operators into highly optimized, native structural INT8 integer execution layers.\n\n## Diagram\n\n```mermaid\nflowchart TD\n    PyTorch[Simulated QAT in PyTorch] --> Export[Export to ONNX]\n    Export --> Compiler[Compiler: TensorRT / TVM]\n    Compiler --> Optimize[Operator Fusion & INT8 Mapping]\n    Optimize --> Hardware[Hardware Execution on NPUs/GPUs]\n```\n"
    },
    "edge_cv.md": {
        "title": "Ultra-Low Latency Mobile and Edge Computer Vision",
        "content": "## Overview\n\nQAT powers real-world processing engines on autonomous robotics and smart mobile platforms. For models like MobileNet and YOLO, QAT allows dense image object tracking matrices to compile directly onto low-power Edge TPUs and NPU chips without breaking safety thresholds.\n\n## Application\n\nBy leveraging INT8/INT4 precision, these models achieve real-time latency and massive energy savings, enabling untethered operation.\n\n## Diagram\n\n```mermaid\nflowchart LR\n    Cam[Camera Feed] --> QAT_Model[INT8 YOLO Model]\n    QAT_Model --> NPU[Edge NPU Execution]\n    NPU --> BBox[Bounding Box Output]\n```\n"
    },
    "llm_qat.md": {
        "title": "On-Device Foundation Language Modeling",
        "content": "## Overview\n\nQAT drives localized on-device agent execution. Applying specialized QAT to compact 1B–8B parameter networks compresses massive VRAM demands down into consumer-tier mobile hardware storage budgets.\n\n## Application\n\nThis enables powerful Edge Assistants that run privately and autonomously without relying on cloud APIs, transforming modern smartphones into AI hubs.\n\n## Diagram\n\n```mermaid\nflowchart TD\n    LLM[8B Parameter Model] --> QAT[LLM-QAT Compression]\n    QAT --> Device[Smartphone 8GB RAM]\n    Device --> Inference[Local Text Generation]\n```\n"
    },
    "fp8_inference.md": {
        "title": "High-Throughput Data Center Serving",
        "content": "## Overview\n\nQAT minimizes cloud operating overhead across distributed serving grids. Enterprise networks leverage FP8-focused QAT frameworks to double generation throughput boundaries while keeping visual or textual fidelity identical to baseline cluster states.\n\n## Application\n\nLarge-scale clusters (like H100s) utilize FP8 precision natively to maximize token generation per watt, pushing the frontier of Data Center serving economics.\n\n## Diagram\n\n```mermaid\nflowchart LR\n    Req[User Requests] --> LB[Load Balancer]\n    LB --> Node1[FP8 Inference Node 1]\n    LB --> Node2[FP8 Inference Node 2]\n    Node1 --> Resp[High Throughput Output]\n    Node2 --> Resp\n```\n"
    }
}

for filename, data in pages.items():
    filepath = os.path.join(pages_dir, filename)
    with open(filepath, 'w') as f:
        f.write(f"# {data['title']}\\n\\n{data['content']}")

print("Successfully created 12 markdown pages in pages/ directory.")
