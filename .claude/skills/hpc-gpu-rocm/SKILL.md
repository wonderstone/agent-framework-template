---
name: hpc-gpu-rocm
description: AMD GPU 高性能计算精华 — ROCm/HIP 编程、rocBLAS/rocFFT/rocRAND/rocSOLVER、CUDA→HIP 移植、rocprof/omniperf 性能分析、MI300X/MI250X 优化。用于 AMD Instinct/Radeon GPU 上的 kernel 开发、性能调优、跨平台 GPU 代码。
model: opus
---

# GPU ROCm / HIP 高性能计算 — 精华技能

## 快速决策：技术选型

```
AMD GPU 上做高性能计算？
├─ 标准数值库 → rocBLAS(GEMM) / rocFFT / rocSOLVER / rocRAND / rocSPARSE
├─ 自定义 kernel
│   ├─ 从 CUDA 移植 → HIP (hipify: 自动+手动) 或直接用 Claude Code 移植
│   ├─ 新开发、跨 NVIDIA/AMD → Triton DSL (硬件无关, Python 写 kernel)
│   └─ 新开发、仅 AMD → HIP C++ (与 CUDA 高度相似的 C++ 方言)
├─ AI 训练/推理
│   ├─ PyTorch ROCm → 标准 PyTorch 代码几乎零修改
│   ├─ vLLM → Triton attention backend (MI300X 上 5.8× vs baseline)
│   └─ JAX → jax-rocm 或 jax-triton
├─ 性能分析 → rocprof (timeline) + omniperf (kernel deep-dive)
└─ 容器化部署 → ROCm Docker (rocm/pytorch, rocm/vllm)
```

## HIP: CUDA 的 AMD 对应物

### CUDA → HIP 关键映射

| CUDA | HIP | 差异 |
|------|-----|------|
| `cudaMalloc` | `hipMalloc` | API 几乎完全相同 |
| `cudaMemcpy` | `hipMemcpy` | 同上 |
| `__global__` | `__global__` | 完全相同 |
| `__shared__` | `__shared__` | 完全相同 |
| `threadIdx.x` | `threadIdx.x` | 完全相同 |
| `cudaStream_t` | `hipStream_t` | `hipStreamCreate` |
| `cublasHandle_t` | `rocblas_handle` | rocBLAS 是 cuBLAS 的独立实现 |
| `nvtxRangePush` | `roctxRangePush` | ROCm 标注工具 |

### 移植策略

```bash
# 步骤1：自动转换 (hipify)
hipify-clang my_cuda.cu --cuda-install-toolchain
# 或
hipconvertinplace-perl.sh my_cuda_dir/

# 步骤2：手动检查
# - warp size: NVIDIA=32, AMD=32(RDNA)/64(CDNA)
# - 查看 hipify 生成的 .hip 文件中标记为 "TOCHECK" 的部分

# 步骤3：编译
hipcc -o my_app my_app.hip -lrocblas -lrocfft

# 步骤4：验证（结果与 CUDA 版本逐位对比）
```

### CUDA vs HIP (CDNA) 架构差异

| 概念 | NVIDIA (Hopper H100) | AMD (CDNA3 MI300X) |
|------|----------------------|---------------------|
| 线程束 | Warp = 32 threads | Wavefront = **64** threads |
| 每个 CU | 128 FP32 ALU | 64 FP32 ALU |
| 矩阵指令 | WMMA / MMA (f16,f32) | MFMA (f16,f32,bf16,i8) |
| L1 Cache | 256 KB/SM | 32 KB/CU → 共享 L2 |
| 共享内存 | 228 KB/SM | 64 KB/CU |
| HBM | 80 GB | 192 GB |
| 带宽 | 3.35 TB/s | 5.3 TB/s |
| 编程模型 | CUDA | HIP |

### Wavefront=64 的影响
```hip
// CUDA: num_warps=8 → 256 threads (8×32)
// AMD:  num_warps=8 → 512 threads (8×64)
// 所以 AMD 上 num_warps=4 ≈ NVIDIA 上 num_warps=8 的并行度
// 注意：divergence penalty 更严重（64 线程一起分支）
```

### MFMA (Matrix Fused Multiply-Add) 指令
```hip
// 类似 CUDA WMMA，但 wavefront=64
// BLOCK_K sweet spot: NVIDIA=16, AMD=32
// gfx942 (MI300X) 支持 fp16/bf16/fp32/i8 MFMA
```

## 性能分析工具链

```bash
# rocprof — 系统级 timeline（类似 Nsight Systems）
rocprof --hip-trace --roctx-trace -o profile.csv ./my_app

# omniperf — kernel 级深度分析（类似 Nsight Compute）
omniperf profile -n my_kernel -- ./my_app
omniperf analyze -p workloads/my_kernel/mi300x/

# rocgdb — 调试
rocgdb ./my_app
(rocgdb) break my_kernel
(rocgdb) info agents  # 列出 GPU

# ROCm Profiler API (代码中嵌入)
#include <roctracer/roctx.h>
roctxRangePush("my_stage");
/* ... */
roctxRangePop();
```

### 关键性能指标
- **Memcpy bandwidth**: MI300X 峰值 5.3 TB/s HBM
- **MFMA 利用率**: 检查 MFMA 指令占比（FP32 计算通常不是瓶颈）
- **L2 Cache 命中率**: MI300X 共享 L2 架构，需特别注意多 CU 间的 cache thrash
- **Wavefront occupancy**: 64-wide wavefront，divergence 代价比 NVIDIA 更大

## AMD 最新策略：AI Agent 驱动优化 (2026)

AMD 在 2026 年明确拥抱 "Agentic GPU Programming"：

| 工具/项目 | 说明 |
|-----------|------|
| **AMD Apex** | 开源 RL 训练环境，Claude Code/Codex 在真实 AMD GPU 上优化 kernel，12 种 kernel 类型 |
| **GEAK-Triton v2** | AMD 官方 Triton kernel 优化 agent，TritonBench 上平均 3.42× 加速 |
| **GEAK HIP** | HIP kernel 自动化优化 agent |
| **GEAK-OpenEvolve** | 基于 Quality-Diversity 进化搜索的 kernel 优化 |
| **Claude Code CUDA→ROCm 移植** | 社区已验证：零手写代码 30 分钟完成 (lc0 象棋引擎) |

### AMD Apex 架构
```
13 Domain Skills (加载到 Claude Code):
├── Triton Optimization
├── HIP Tuning
├── Architecture Guidance (CDNA3 gfx942, CDNA4)
├── Kernel RAG (检索已知优化模式)
├── Fusion Advisor (kernel 融合建议)
├── Magpie Evaluation (性能评估)
└── 5 MCP Servers (源码检索, kernel RAG, GPU信息, 融合顾问, 评估)
```

## Triton on AMD ROCm

### 编译目标
```python
# NVIDIA: 
#   triton.compile(..., arch="sm_80")
# AMD:
#   triton.compile(..., arch="gfx942")  # MI300X
#   triton.compile(..., arch="gfx908")  # MI100
#   triton.compile(..., arch="gfx1100") # RDNA3 (RX 7900)
```

### AMD Triton 特殊参数
```python
@triton.autotune(
    configs=[
        triton.Config({'BLOCK_M': 128, 'BLOCK_N': 256, 'BLOCK_K': 32,   # ← K=32 sweet spot
                       'num_warps': 4, 'num_stages': 4}),                 # ← num_warps=4 ≈ CUDA num_warps=8
    ],
    key=['M', 'N', 'K'],
)
@triton.jit
def my_kernel(...):
    ...
```

## 与 NVIDIA 对比速查

| 维度 | NVIDIA 优势 | AMD 优势 |
|------|------------|----------|
| 生态成熟度 | 更好（CUDA 17+年） | 追赶中 |
| 内存容量 | 最多 141 GB (H200) | **192 GB** (MI300X) |
| 内存带宽 | 4.8 TB/s (H200) | **5.3 TB/s** (MI300X) |
| 性价比 | — | 通常更低 |
| 软件兼容 | PyTorch 最稳 | PyTorch ROCm 已成熟 |
| AI Agent 工具 | AKO4ALL, cuda-optimization-skill | Apex, GEAK 系列 |

## 精选参考

- [ROCm Documentation](https://rocm.docs.amd.com/)
- [HIP Programming Guide](https://rocm.docs.amd.com/projects/HIP/en/latest/)
- [AMD Apex](https://github.com/amd/apex) — Agentic kernel optimization
- [GEAK-Triton v2](https://rocm.blogs.amd.com/) — AMD Triton 优化 agent
- [HLRS AMD GPU Training](https://www.hlrs.de/training/2026/gpu-amd)
- [Triton AMD Backend](https://github.com/triton-lang/triton)
