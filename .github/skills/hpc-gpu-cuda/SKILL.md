---
name: hpc-gpu-cuda
description: GPU CUDA 高性能计算精华 — CUDA C/C++ kernel 编写与优化、CUTLASS/CuTe 模板库、cuBLAS/cuFFT/cuSPARSE/cuRAND、Nsight Systems/Compute 性能分析、TensorRT 推理优化。用于 NVIDIA GPU 上的高性能 kernel 开发、性能调优、CUDA→ROCm 移植。
model: opus
---

# GPU CUDA 高性能计算 — 精华技能

## 快速决策：技术选型

```
需要 GPU 高性能计算（NVIDIA 平台）？
├─ 标准数值运算（BLAS/FFT/稀疏）→ 直接用 cuBLAS/cuFFT/cuSPARSE/cuRAND（已达峰值 90%+）
├─ 自定义 kernel 开发
│   ├─ 快速原型、跨平台 → Triton DSL（Python 写 GPU kernel）
│   ├─ 极致性能、Tensor Core → CUTLASS/CuTe（NVIDIA 模板库）
│   ├─ 类 STL 并行算法 → Thrust（reduce/scan/sort）+ CUB（block/warp 级原语）
│   └─ 裸 CUDA C++ → 当上述都不满足时（需完全控制）
├─ 深度学习推理优化 → TensorRT（FP8/INT4 量化、kernel fusion）
├─ 多 GPU 通信 → NCCL（AllReduce 等集合通信）
└─ Python 用户 → CuPy（NumPy 兼容 API）、Numba CUDA、PyTorch CUDA Extension
```

## CUDA Kernel 优化 — 标准工作流

### 铁律：先 Profile，再优化，永远不要猜

```bash
# 第一步：系统级概览（找哪些 kernel 在吃时间）
nsys profile --trace cuda,nvtx --stats true -o timeline ./my_app

# 第二步：提取 GPU 时间 Top-N kernel
nsys stats timeline.nsys-rep --report cuda_gpu_kern_sum

# 第三步：针对热 kernel 深挖
ncu --kernel-name "hot_kernel" --launch-count 3 --set full -o analysis ./my_app

# 第四步：锁定 GPU 时钟（保证结果可复现）
sudo nvidia-smi -lgc 1200

# 第五步：根据 roofline 分类瓶颈
ncu --set full --section SpeedOfLight_RooflineChart ./my_app
```

### 瓶颈分类决策树

```
ncu Roofline 分析后：
│  Arithmetic Intensity = Total FLOPs ÷ Bytes Accessed
│
├─ 低 AI (≤10 FLOPs/byte) → Memory-bound
│   ├─ DRAM 带宽远低峰值 → uncoalesced 访问（最大最常见的问题）
│   │   → 修复：连续线程访问连续地址 (stride-1)，避免 stride-N
│   ├─ L1/L2 命中率低 → tiling 使数据复用留在 cache
│   └─ 共享内存 bank conflict → padding: __shared__ float smem[BLOCK][BLOCK+1]
│
├─ 高 AI (≥100 FLOPs/byte) → Compute-bound
│   ├─ IPC 低 → warp divergence、指令依赖、寄存器溢出
│   │   → 修复：统一 warp 内分支方向、使用 predication
│   ├─ 未用 Tensor Core → CUTLASS/CuTe 或 wmma API
│   └─ 数据类型过大 → 用 half/bf16 替代 float（Tensor Core 需要）
│
├─ 低 Occupancy → 隐藏延迟能力不足
│   ├─ 寄存器用量过高 → __launch_bounds__() 或 --maxrregcount
│   └─ 共享内存过大 → 减少 block 内共享内存，或降 block 大小
│
└─ Long Scoreboard  stalls → warps 在等内存（几乎总是 memory-bound）
```

### 关键优化技巧（按 ROI 排序）

1. **内存合并 (Coalescing)** — 通常是最大收益
   ```cuda
   // ✓ Good: stride-1 访问
   float val = data[threadIdx.x + blockIdx.x * blockDim.x];
   // ✗ Bad: strided 访问，浪费 85%+ 带宽
   float val = data[threadIdx.x * N + blockIdx.x];
   ```

2. **共享内存 + Bank Conflict 避免**
   ```cuda
   __shared__ float tile[BLOCK_SIZE][BLOCK_SIZE + 1]; // +1 padding 消除 conflict
   ```

3. **Occupancy 调优**
   ```cuda
   __launch_bounds__(256, 4)  // max 256 threads, min 4 blocks/SM
   __global__ void my_kernel(...) { ... }
   ```

4. **异步拷贝 (cp.async)** — Hopper (SM90+) 专属
   ```cuda
   // 用 TMA 或 cp.async 重叠 global→shared 传输与计算
   __pipeline_memcpy_async(&smem[0], &gmem[0], sizeof(float)*N);
   __pipeline_wait_prior(0);
   ```

5. **数据类型选择**
   - 默认用 `float`（平衡精度/性能）
   - Tensor Core 用 `half`/`__half2`（吞吐翻倍）
   - 避免 `double` 除非必需（带宽和寄存器均翻倍）

### 架构速查表

| 架构 | SM | Max Threads/SM | Shared Mem/SM | Tensor Core | 关键特性 |
|------|----|----|------|-------------|------|
| Ampere (A100, SM80) | 108 | 2048 | 164 KB | 3rd gen | BF16, TF32 |
| Hopper (H100, SM90) | 132 | 2048 | 228 KB | 4th gen | FP8, TMA, DPX |
| Ada (L40S, SM89) | — | 1536 | 100 KB | 4th gen | FP8 |
| Blackwell (B200, SM100) | — | 2048 | 256 KB | 5th gen | FP4, MXFP8 |

## CUTLASS / CuTe — Tensor Core 编程的工业标准

### 何时用 CUTLASS vs 手写 CUDA
- **用 CUTLASS**: GEMM/Conv/Attention 变体，需要 Tensor Core，对性能要求 ≥ cuBLAS 80%
- **用手写 CUDA**: 简单 element-wise、reduction、无矩阵乘法模式

### CuTe DSL 核心概念（CUTLASS 4.3+）
```cpp
// CuTe DSL 关键抽象
auto tiled_mma = make_tiled_mma(SM80_16x8x8_F32F16F16F32_TN{});
auto thr_copy = make_tiled_copy(Copy_Atom<UniversalCopy<uint128_t>, float>{});
// Threadblock shape, stages, epilogue, schedule 都是编译期参数
```

### μCUTLASS (2026 新范式)
- 紧凑 DSL，AI Agent 更易 in-context 学习
- Speed-of-Light (SOL) 引导：用理论上界约束/验证优化过程
- 实测比底层 CUDA 更易被 Agent 生成，同时保持 1.27×–1.56× speedup

## cuBLAS / cuFFT / cuSPARSE / Thrust

| 库 | 用途 | 关键 API |
|----|------|---------|
| **cuBLAS** | 稠密矩阵乘/向量 | `cublasGemmEx`, `cublasLtMatmul` |
| **cuFFT** | 快速傅里叶变换 | `cufftExecC2C`, `cufftPlanMany` |
| **cuSPARSE** | 稀疏矩阵运算 | SpMM, SpMV, SpGEMM |
| **Thrust** | 并行算法(STL风格) | `thrust::sort`, `thrust::reduce`, `thrust::scan` |
| **CUB** | Block/Warp级原语 | `cub::BlockReduce`, `cub::BlockScan` |

### 关键经验
- cuBLAS GEMM 已达理论峰值 90%+，自定义 GEMM kernel 很难超越
- 复杂算子组合优于逐个调用（避免 round-trip 开销）
- cuBLAS + CUDA Streams 实现多流并行

## Nsight 工具链速查

```bash
# Nsight Systems — 系统级时间线
nsys profile --trace cuda,nvtx,osrt --stats true -o timeline ./app

# Nsight Compute — 单 kernel 深挖
ncu --set full --kernel-name "kname" --launch-count 3 --csv -f report.csv ./app

# NVTX 标注（在代码中标记关键阶段）
#include <nvtx3/nvToolsExt.h>
nvtxRangePushA("forward_pass"); /* 代码 */ nvtxRangePop();

# cuda-gdb — 调试
cuda-gdb ./app
(cuda-gdb) set cuda break_on_launch application
(cuda-gdb) info cuda kernels

# compute-sanitizer — 内存错误检测
compute-sanitizer --tool memcheck ./app
compute-sanitizer --tool racecheck ./app
```

## TensorRT 推理优化速查

```python
# 核心流程：ONNX → TensorRT Engine → Inference
import tensorrt as trt
builder = trt.Builder(logger)
network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
# 关键优化：FP16/INT8 量化、layer fusion、kernel auto-tuning
config.set_flag(trt.BuilderFlag.FP16)
config.set_flag(trt.BuilderFlag.INT8)
```

## AI Agent 辅助优化工作流 (2026)

成熟的开源工具链可实现闭环优化：
1. **[AKO4ALL](https://github.com/TongmingLAIC/AKO4ALL)** — agent 读 kernel → NCU profile → 改写 → 验证，支持 CUDA/Triton，实测 8.93× 加速
2. **[cuda-optimization-skill](https://github.com/gxinlong/cuda-optimization-skill)** — 生成→编译→验证→NCU分析→优化 全流程
3. **[HuggingFace cuda-kernels](https://github.com/huggingface/kernels)** — PyTorch CUDA Extension 专用 skill，Qwen3-8B 上 2.47× 加速
4. **[Forge MCP](https://www.npmjs.com/package/@rightnow/forge-mcp-server)** — 32 并行 agent swarm 竞争生成最优 kernel

## 精选参考

- [CUDA C++ Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/)
- [CUTLASS Documentation](https://docs.nvidia.com/cutlass/)
- [Nsight Compute Documentation](https://docs.nvidia.com/nsight-compute/)
- [NVIDIA/skills](https://github.com/NVIDIA/skills) — NVIDIA 官方 Agent Skills
- [AKO4ALL](https://github.com/TongmingLAIC/AKO4ALL) — Agentic Kernel Optimization
- [FACT Paper](https://arxiv.org/abs/2604.26666) — Agentic CUTLASS Transpilation
- [μCUTLASS Paper](https://arxiv.org/abs/2603.29010) — Compact DSL + SOL Guidance
