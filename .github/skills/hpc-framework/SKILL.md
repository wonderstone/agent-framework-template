---
name: hpc-framework
description: 框架级 GPU 加速精华 — PyTorch CUDA Extension 自定义算子、Triton DSL kernel 编写与 autotune、JAX XLA shard_map 多 GPU 分片、GGML/llama.cpp CPU+GPU 混合推理、MLX Apple Silicon。用于在 ML 框架层面实现高性能自定义算子。
model: opus
---

# 框架级 GPU 加速 — 精华技能

## 框架选型决策树

```
需要框架级 GPU 加速？
├─ PyTorch 生态，需嵌入自定义 CUDA kernel
│   ├─ 快速开发 → PyTorch CUDA Extension (C++/CUDA + torch::Library)
│   ├─ 更简单 → Triton DSL (Python 写 kernel, @triton.autotune)
│   ├─ 极致优化(GEMM类) → CUTLASS + PyTorch binding
│   └─ vLLM 等推理框架集成 → Triton kernel（跨 NVIDIA/AMD）
│
├─ Google 生态 / TPU / 大规模分片
│   ├─ 首选 → JAX + XLA (shard_map, vmap, pmap→已废弃)
│   └─ 多 GPU 分片 → FSDP → Pipeline Parallel → Tensor Parallel (JAX)
│
├─ Apple Silicon 原生
│   ├─ 训练/推理 → MLX (Apple 官方, 统一内存零拷贝)
│   ├─ 极限性能 → RMLX (Rust, 2× MLX decode)
│   └─ 兼容 PyTorch API → PyTorch MPS (慢但兼容)
│
├─ CPU + GPU 混合推理 (LLM)
│   ├─ 最灵活 → GGML / llama.cpp (CPU + 多 GPU backend)
│   ├─ Metal/MPS → llama.cpp + Metal backend (Apple Silicon)
│   ├─ Vulkan → llama.cpp + Vulkan backend (跨平台)
│   ├─ CUDA → llama.cpp + CUDA backend
│   └─ ROCm → llama.cpp + HIP backend (AMD)
│
└─ 跨框架 → ONNX Runtime + TensorRT / OpenVINO / CoreML
```

## PyTorch CUDA Extension — 自定义算子

### 完整模板

```cpp
// my_ops.cu
#include <torch/extension.h>

// CUDA kernel
__global__ void my_kernel(const float* input, float* output, int N) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < N) output[idx] = input[idx] * 2.0f;
}

// Host wrapper
torch::Tensor my_op_cuda(torch::Tensor input) {
    auto output = torch::empty_like(input);
    int N = input.numel();
    const int threads = 256;
    const int blocks = (N + threads - 1) / threads;
    my_kernel<<<blocks, threads>>>(input.data_ptr<float>(), output.data_ptr<float>(), N);
    return output;
}

// PyTorch 注册
TORCH_LIBRARY(my_ops, m) {
    m.def("my_op(Tensor input) -> Tensor");
}
TORCH_LIBRARY_IMPL(my_ops, CUDA, m) {
    m.impl("my_op", my_op_cuda);
}
```

```python
# setup.py
from setuptools import setup
from torch.utils.cpp_extension import CUDAExtension, BuildExtension
setup(
    name='my_ops',
    ext_modules=[CUDAExtension('my_ops', ['my_ops.cu'])],
    cmdclass={'build_ext': BuildExtension}
)
```

### 关键技巧
- 用 `torch::empty_like` 而非手动分配显存
- `TORCH_LIBRARY` + `TORCH_LIBRARY_IMPL` 注册（新式 API，优于旧式 `PYBIND11_MODULE`）
- 多 GPU arch 编译：`TORCH_CUDA_ARCH_LIST="8.0;8.6;9.0" python setup.py install`
- 调试：`TORCH_SHOW_CPP_STACKTRACES=1` + `compute-sanitizer`

### HuggingFace kernel-builder 模式 (2026)
```bash
pip install git+https://github.com/huggingface/kernels.git
kernels skills add cuda-kernels --claude
```
Skill 覆盖：build.toml 配置、PyTorch binding、H100 compute capability 9.0、async copy、混精度模板。实测 Qwen3-8B RMSNorm 加速 2.47×。

## Triton DSL — Python 写 GPU Kernel

### 核心模式
```python
import triton
import triton.language as tl

@triton.jit
def vec_add_kernel(x_ptr, y_ptr, output_ptr, N,
                   BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(0)
    offsets = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
    mask = offsets < N
    x = tl.load(x_ptr + offsets, mask=mask)
    y = tl.load(y_ptr + offsets, mask=mask)
    tl.store(output_ptr + offsets, x + y, mask=mask)

# Autotune — Triton 杀手特性
@triton.autotune(
    configs=[
        triton.Config({'BLOCK_SIZE': 128}, num_warps=4),
        triton.Config({'BLOCK_SIZE': 256}, num_warps=4),
        triton.Config({'BLOCK_SIZE': 512}, num_warps=8),
    ],
    key=['N'],
)
@triton.jit
def my_kernel(...):
    ...
```

### NVIDIA vs AMD Triton 参数速查

| 参数 | NVIDIA (H100) | AMD (MI300X) |
|------|--------------|--------------|
| num_warps | 4-8 (warp=32) | 2-4 (wavefront=64) |
| BLOCK_K (matmul) | 16 sweet spot | **32** sweet spot |
| arch | `sm_80`/`sm_90` | `gfx942`/`gfx908` |
| num_stages | 2-4 | 2-4 |
| 矩阵指令 | WMMA | MFMA |

### Triton 在 vLLM 中的实战
- 约 800 行 Triton 代码实现跨 NVIDIA/AMD/Intel 的 attention kernel
- H100 上达到 FlashAttention 3 的 100.7%
- MI300X 上获得 5.8× 加速
- 关键优化：Q Blocks + Parallel Tiled Softmax (3D kernel) + Persistent Kernels

## JAX XLA — 大规模分片训练

### pmap → shard_map 迁移（重要！）
```python
# 旧：pmap (已废弃)
@functools.partial(pmap, axis_name='batch')
def train_step(params, batch): ...

# 新：shard_map (推荐)
from jax.experimental.shard_map import shard_map
mesh = Mesh(devices, ('data', 'model'))
sharding = PartitionSpec('data', 'model')

@functools.partial(shard_map, mesh=mesh,
                   in_specs=(PartitionSpec('data', None),),
                   out_specs=PartitionSpec('data', None))
def my_function(x): ...
```

### 分片策略选择
| 策略 | 适用场景 | JAX 实现 |
|------|---------|---------|
| FSDP (全分片数据并行) | 大部分场景首选 | `jax.sharding.Mesh` |
| Tensor Parallel | 单层超 >7B | `shard_map` + collective |
| Pipeline Parallel | 层数多无法全放 | 手动 micro-batch |
| 3D 并行 | 超大模型 | TP+PP+DP 组合 |
| Expert Parallel (MoE) | Mixtral/DeepSeek | 按 expert 分片 |

### XLA 编译优化
```python
# 编译缓存（避免重复编译）
import jax
jax.config.update('jax_compilation_cache_dir', '/tmp/jax_cache')

# NVSHMEM 加速（NVIDIA GPU 间通信）
# export XLA_FLAGS="--xla_gpu_experimental_enable_nvshmem=true"
# 256K 序列长度加速 36%

# Shardy partitioner（自动分片优化器，JAX 25.10+ 默认启用）
```

## GGML / llama.cpp — CPU+GPU 混合推理

### Backend 选择
| Backend | 平台 | 适用 |
|---------|------|------|
| CPU (默认) | 全平台 | 无 GPU 时 fallback |
| CUDA | NVIDIA | 最佳 GPU 性能 |
| Metal | Apple Silicon | M1-M5 芯片 |
| Vulkan | 跨平台 GPU | AMD/Intel/手机 |
| ROCm/HIP | AMD | AMD GPU |
| SYCL | Intel GPU | Intel Arc/Data Center |

### 量化格式选择
| 格式 | 大小 | 质量 | 适用 |
|------|------|------|------|
| Q4_K_M | ~4.5 bpw | 很好 | 生产推荐 |
| Q5_K_M | ~5.5 bpw | 更好 | 质量优先 |
| Q2_K | ~2.5 bpw | 可接受 | 极小内存 |
| Q8_0 | ~8.5 bpw | 几乎无损 | 参考基线 |
| IQ4_NL | ~4.25 bpw | 好 | 低内存场景 |

### 关键编译选项
```bash
# Apple Silicon
cmake -B build -DGGML_METAL=ON

# NVIDIA
cmake -B build -DGGML_CUDA=ON

# Vulkan (跨平台)
cmake -B build -DGGML_VULKAN=ON

# 混合量化+GPU offload
./llama-cli -m model.gguf -ngl 99  # 99层GPU, 其余CPU
```

## 框架级性能调试

| 框架 | 工具 | 关键命令 |
|------|------|---------|
| PyTorch | torch.profiler | `prof.step()` 查 CUDA time, memory |
| PyTorch | NVIDIA Nsight | `nsys profile --trace cuda,nvtx python train.py` |
| Triton | `tl.static_assert` | kernel 内编译期检查 |
| JAX | `jax.profiler` | `with jax.profiler.trace(...)` |
| JAX | XLA HLO dump | `XLA_FLAGS="--xla_dump_to=./dump"` |
| GGML | `--verbose` | 打印 layer 时间分布 |

## 精选参考

- [PyTorch Custom C++/CUDA Extension](https://pytorch.org/tutorials/advanced/cpp_extension.html)
- [Triton Language Documentation](https://triton-lang.org/)
- [JAX shard_map Guide](https://docs.jax.dev/en/latest/notebooks/shard_map.html)
- [HuggingFace cuda-kernels Skill](https://github.com/huggingface/kernels)
- [AKO4ALL](https://github.com/TongmingLAIC/AKO4ALL)
- [GGML](https://github.com/ggml-org/ggml)
- [llama.cpp](https://github.com/ggml-org/llama.cpp)
- [MLX](https://github.com/ml-explore/mlx)
- [RMLX](https://github.com/robertelee78/mlx-native)
- [Awesome-Kernel-Skills (18 modules)](https://zhuanlan.zhihu.com/p/2022319499546821151)
- [TileLang Paper (ICLR 2026)](https://iclr.cc/virtual/2026/poster/10010186)
