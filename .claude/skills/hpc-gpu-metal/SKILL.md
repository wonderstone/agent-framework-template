---
name: hpc-gpu-metal
description: Apple GPU 高性能计算精华 — Metal Shading Language (MSL) kernel/Compute 编写、Metal Performance Shaders (MPS/MPSGraph)、MLX 框架、Apple Silicon (M1-M5) 统一内存优化、BNNS/ANE。用于 macOS/iOS 上的 GPU 加速、ML 推理训练、Metal compute kernel 开发与调优。
model: opus
---

# GPU Metal / Apple Silicon 高性能计算 — 精华技能

## 快速决策：技术选型

```
Apple Silicon 上做高性能计算？
├─ 深度学习训练/推理
│   ├─ 首选 → MLX（Apple 官方 ML 框架，统一内存零拷贝）
│   ├─ 需要最大模型覆盖 → PyTorch MPS（但比 MLX 慢 2-3×）
│   ├─ 需要极致性能 (LLM) → RMLX (Rust 重写, 2× MLX decode)
│   └─ 本地推理服务 → Ollama 0.19+ (内置 MLX backend)
│
├─ 自定义 GPU Compute Kernel
│   ├─ 最高层 → MPSGraph（自动 kernel fusion, 不需手写 MSL）
│   ├─ 中层 → MPS (预优化算子库: 矩阵乘/卷积/规约/排序等)
│   ├─ 底层 → Metal Shading Language (MSL C++14)
│   └─ 需与渲染结合 → Metal Compute + Render pipeline 共用资源
│
├─ 经典数值计算 (BLAS/LAPACK)
│   └─ Apple Accelerate (内置, 针对 Apple Silicon 优化, 无需额外安装)
│
└─ 混合精度推理 / 设备端 AI
    ├─ Core ML (部署) + ANE (Neural Engine, 最低功耗)
    └─ BNNS (Basic Neural Network Subroutines)
```

## Apple Silicon 架构核心认知

### 统一内存 (Unified Memory Architecture)
```
Intel/NVIDIA: CPU RAM ←(PCIe 复 制)→ GPU VRAM   (两 个 地 址 空 间)
Apple Silicon: CPU ←→ Unified Memory ←→ GPU      (同一物理内存)
```
- `MTLStorageModeShared` — CPU/GPU 零拷贝共享（默认首选）
- `MTLStorageModePrivate` — 仅 GPU 访问（更高带宽）
- `MTLResourceStorageModeMemoryless` — 片上 tile memory（不占 DRAM, 仅 TBDR 中间结果）

### M 系列 GPU 参数速查

| 芯片 | GPU 核心 | FP16 TFLOPS | 内存带宽 | 统一内存(max) |
|------|---------|-------------|---------|-------------|
| M1 | 7-8 | 2.6 | 68 GB/s | 16 GB |
| M2 | 8-10 | 3.6 | 100 GB/s | 24 GB |
| M3 | 10-18 | ~7 | 100-150 GB/s | 36 GB |
| M4 | 10-20 | ~9 | 120-180 GB/s | 64 GB |
| M2 Ultra | 60-76 | 27.2 | 800 GB/s | 192 GB |
| M3 Ultra | 60-80 | ~35 | 800-1000 GB/s | 256 GB |
| M5 (预估) | — | — | — | — |

### TBDR (Tile-Based Deferred Rendering) 关键影响
- Tile memory 是免费的（片上 SRAM），但容量有限
- 避免 tile memory spill → 优化 threadgroup 大小 + 中间结果复用
- `dispatchThreads` vs `dispatchThreadgroups`：前者让 GPU 决定分块（推荐），后者手动指定

## Metal Shading Language (MSL) 核心模板

### Compute Kernel 基本结构
```metal
#include <metal_stdlib>
using namespace metal;

kernel void my_kernel(
    device float* input  [[buffer(0)]],
    device float* output [[buffer(1)]],
    constant uint& N     [[buffer(2)]],
    uint gid             [[thread_position_in_grid]]
) {
    if (gid >= N) return;
    output[gid] = f(input[gid]);
}
```

### 2D 分块矩阵乘法模板
```metal
kernel void tiled_matmul(
    device const float* A [[buffer(0)]],
    device const float* B [[buffer(1)]],
    device float* C       [[buffer(2)]],
    constant uint& M [[buffer(3)]],
    constant uint& N [[buffer(4)]],
    constant uint& K [[buffer(5)]],
    threadgroup float* As [[threadgroup(0)]],
    threadgroup float* Bs [[threadgroup(1)]],
    uint2 gid [[threadgroup_position_in_grid]],
    uint2 tid [[thread_position_in_threadgroup]]
) {
    const uint TILE = 16;
    float sum = 0.0;
    for (uint k = 0; k < K; k += TILE) {
        // 协作加载 tile
        As[tid.y * TILE + tid.x] = A[(gid.y * TILE + tid.y) * K + (k + tid.x)];
        Bs[tid.y * TILE + tid.x] = B[(k + tid.y) * N + (gid.x * TILE + tid.x)];
        threadgroup_barrier(mem_flags::mem_threadgroup);
        // 计算 tile
        for (uint kk = 0; kk < TILE; kk++)
            sum += As[tid.y * TILE + kk] * Bs[kk * TILE + tid.x];
        threadgroup_barrier(mem_flags::mem_threadgroup);
    }
    uint row = gid.y * TILE + tid.y, col = gid.x * TILE + tid.x;
    if (row < M && col < N) C[row * N + col] = sum;
}
```

### MSL 性能关键点
- `half` vs `float`: M1-M2 的 half 吞吐是 float 的 2×（M3+ 趋同）
- `threadgroup_barrier` 开销不可忽视，MPSGraph 自动融合会隐藏很多 barrier
- 用 `function_constant` 做编译期分支，比运行时 `if` 快
- Triple buffering: 3 个缓冲区轮转，实现 CPU→GPU 流水线重叠

## MPS / MPSGraph

### MPS (预优化算子库)
```objc
// MPSMatrixMultiplication — 已达 Metal 峰值 ~90%
MPSMatrixMultiplication* mm = [[MPSMatrixMultiplication alloc] init...];
[mm encodeToCommandBuffer:cb leftMatrix:A rightMatrix:B resultMatrix:C];
```

### MPSGraph (自动融合图)
```objc
MPSGraph* graph = [[MPSGraph alloc] init];
MPSGraphTensor* x = [graph placeholderWithShape:@[@B,@C,@H,@W] dataType:MPSDataTypeFloat32];
MPSGraphTensor* conv = [graph convolution2DWithSource:x weights:w ...];
MPSGraphTensor* relu = [graph reLUWithTensor:conv name:nil];
// MPSGraph 自动将 Conv2D+ReLU 融合成一个 kernel dispatch!
```
实测：`Conv2D+ReLU` 融合 → M2 Ultra 上延迟从 1.83ms → 0.97ms（88.7% 提升）

### MPS 调试技巧
- Xcode GPU Frame Capture 可窥视 MPS 自动生成的 kernel
- 关注 3 类 stall: (1) register spill + bank conflict (2) 隐藏 barrier (3) 自动中间 buffer 导致的 L1 thrash
- stride=16 会触发 16-way bank conflict → 改为 17 可提升 124% occupancy

## MLX 框架

### 核心 API（类 NumPy/PyTorch 风格）
```python
import mlx.core as mx
a = mx.random.normal((1000, 1000))
b = mx.random.normal((1000, 1000))
c = a @ b                        # lazy: 只构建图
mx.eval(c)                       # 触发 Metal GPU 执行
c2 = mx.compile(lambda x,y: x@y)(a, b)  # JIT 编译（推荐）
```

### 关键优化技巧
- 懒执行 (lazy)：操作不立即执行，`mx.eval()` 或打印才触发
- `mx.compile` JIT：对重复执行的图显著加速（~2×）
- 零拷贝：MLX 数组直接操作统一内存，无 CPU↔GPU 传输
- 内存类型：`mx.float16` 在大模型推理中收益巨大

### RMLX (Rust 重写) — 性能突破
当 MLX 不够快时考虑：
- Decode: 7-dispatch fusion → 2.1× 比 MLX (`fused_rms_gemv` + `fused_swiglu_down`)
- Quant GEMM: Q4 提速 28%
- MoE Expert Parallelism: 30-178× 比 MLX
- Dist: Thunderbolt 5 RDMA, 零拷贝跨机, allreduce 6.6×

## 工具链速查

| 工具 | 用途 | 使用方式 |
|------|------|---------|
| Xcode GPU Frame Capture | 查看所有 Metal dispatch, shader profiler | Xcode → Product → GPU Frame Capture |
| Metal System Trace | 系统级 GPU 时间线 | Instruments → Metal System Trace |
| Metal Shader Validator | 编译期 shader 性能预估 | `xcrun metal -c kernel.metal` |
| `mlx.core.eval()` | 触发 MLX 执行 | 代码中 |
| Ollama 0.19+ | LLM 本地推理（MLX backend） | `ollama run qwen3` |

## 常见陷阱
1. **CPU↔GPU 复制** — 统一内存虽可零拷贝，但 `MTLStorageModeManaged` 在多 GPU 下仍可能复制
2. **MPS 兼容性** — 老 MPS 算子可能在 M1 上回退为 CPU（检查 `supportsInPlace`）
3. **Float16 精度** — M1-M2 的 half 吞吐高但范围有限（max 65504），溢出时自动回退 float 会慢很多
4. **Tile Memory 溢出** — 过大 threadgroup 导致片上内存溢出到 DRAM，性能断崖
5. **ANE 不可编程** — Neural Engine 只能通过 Core ML 间接使用

## 精选参考

- [Metal Shading Language Specification](https://developer.apple.com/metal/Metal-Shading-Language-Specification.pdf)
- [MPS Documentation](https://developer.apple.com/documentation/metalperformanceshaders)
- [MLX Documentation](https://ml-explore.github.io/mlx/)
- [RMLX](https://github.com/robertelee78/mlx-native) — Rust MLX, 2× decode
- [metal-kernel skill](https://github.com/pytorch/pytorch/tree/main/aten/src/ATen/native/mps) — PyTorch MPS kernel 参考
- [Metal Shader Expert](https://agentskills.so/skills/erichowens-some_claude_skills-metal-shader-expert) — 20+ 年经验 Metal 专家 skill
