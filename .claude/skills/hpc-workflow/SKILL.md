---
name: hpc-workflow
description: AI 辅助高性能优化工作流 — Profile→Analyze→Optimize→Verify 闭环、瓶颈自动分类 (Memory/Compute/Occupancy/Latency bound)、AI Agent 自动 kernel 优化策略、GPU 编程专家思维模型。用于指导 AI 或人工进行系统性的性能调优。
model: opus
---

# AI 辅助高性能优化工作流 — 元技能

## 核心思维模型：Roofline + 瓶颈分类

```
优化铁律：先 Profile → 分类瓶颈 → 针对性优化 → 重新验证
               ↑___________________________________________|
                              每次循环必须验证
```

### 瓶颈自动分类决策树

```
Roofline 分析 → 计算 Arithmetic Intensity (AI = FLOPs / Bytes)

AI 低 (≤10 FLOPs/byte) → Memory-bound
├── DRAM bandwidth far below peak → Uncoalesced access
│   → Fix: stride-1 access, SoA layout
├── L1/L2 cache miss rate high → Poor data reuse
│   → Fix: tiling, shared memory buffering
├── Shared memory bank conflict
│   → Fix: padding (+1), or change access stride
├── Frequent host↔device transfer
│   → Fix: pinned memory, async transfer, CUDA Streams
└── Many small kernel launches
    → Fix: kernel fusion, CUDA Graphs

AI 高 (≥100 FLOPs/byte) → Compute-bound
├── IPC far below peak → Warp divergence, instruction dependency
│   → Fix: predication, unroll, instruction reordering
├── Not using Tensor Core → Missing optimization opportunity
│   → Fix: CUTLASS/CuTe, wmma, Triton matmul
├── Large data type (double instead of float)
│   → Fix: fp32→fp16/bf16 where precision allows
└── Register spilling (check local memory traffic)
    → Fix: __launch_bounds__, limit register usage

Occupancy too low → Hiding latency capacity too small
├── Too many registers per thread → __launch_bounds__
├── Too much shared memory per block → reduce tile size
└── Block size too small/large → re-tune

"Long Scoreboard" stalls dominate → Almost always memory-bound
    (warps are waiting on memory, even if FLOPS look good)
```

## 标准优化循环 (各平台通用)

### Phase 1: 基准 & Profile

```bash
# CPU 版本
perf record -g ./my_app && perf report          # 找热函数
valgrind --tool=cachegrind ./my_app              # Cache miss 归因
likwid-perfctr -C 0 -g MEM_DP ./my_app          # 内存带宽

# GPU CUDA 版本
nsys profile --trace cuda,nvtx --stats true -o timeline ./my_app
nsys stats timeline.nsys-rep --report cuda_gpu_kern_sum  # Top 热 kernel
ncu --set full --kernel-name "hot_kernel" --csv -f report.csv ./my_app

# GPU Metal 版本
# Xcode → Product → GPU Frame Capture → Shader Profiler

# GPU ROCm 版本
rocprof --hip-trace -o profile.csv ./my_app
omniperf profile -n hot_kernel -- ./my_app

# PyTorch 版本
from torch.profiler import profile, ProfilerActivity
with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA]) as prof:
    model(x)
prof.export_chrome_trace("trace.json")
```

### Phase 2: 分析 & 分类

读 profile 结果，按以下顺序排查（按 ROI）：

1. **数据传输** — CPU↔GPU memcpy 时间占比 >10%？→ 减少传输、pinned memory、异步
2. **Kernel Launch Overhead** — 大量小 kernel（每个 <10μs）？→ 融合或 CUDA Graphs
3. **内存访问模式** — 带宽利用率 <60%？→ uncoalesced access、bank conflict
4. **计算效率** — IPC < 1.0？→ divergence、指令依赖、未用 Tensor Core
5. **Occupancy** — <50%？→ 寄存器/共享内存压力

### Phase 3: 定向优化

```python
# 伪代码：优化策略匹配表
OPTIMIZATION_STRATEGIES = {
    "DRAM_MEMORY_BOUND": [
        "1. Check memory coalescing (stride-1 access)",
        "2. Apply tiling to fit working set in L1/L2",
        "3. Buffer repeated reads in shared memory",
        "4. Use SoA instead of AoS layout",
        "5. Reduce data type size (fp64→fp32, fp32→fp16)"
    ],
    "L1_PRESSURE_BOUND": [
        "1. Reduce tile size to fit L1",
        "2. Check shared memory bank conflicts",
        "3. Use read-only cache (__ldg) for uniform reads"
    ],
    "LATENCY_BOUND": [
        "1. Increase occupancy (more warps to hide latency)",
        "2. Add instruction-level parallelism (ILP)",
        "3. Use async copy (cp.async) to overlap loads"
    ],
    "COMPUTE_BOUND": [
        "1. Use Tensor Core (CUTLASS/CuTe/wmma)",
        "2. Reduce data type (fp64→fp32→fp16→fp8)",
        "3. Fuse operations to reduce round-trips",
        "4. Eliminate warp divergence within critical path"
    ],
    "OCCUPANCY_BOUND": [
        "1. Limit register usage (--maxrregcount, __launch_bounds__)",
        "2. Reduce shared memory per block",
        "3. Adjust block size (not always bigger=better)"
    ],
    "HOST_OR_LAUNCH_BOUND": [
        "1. Use CUDA Graphs to eliminate launch overhead",
        "2. Batch small operations into single kernel",
        "3. Use persistent kernels for repeated small ops"
    ]
}
```

### Phase 4: 验证 & 记录
```bash
# 重新 profile 确认改进
# 记录：kernel 名称、瓶颈分类、优化策略、改进幅度
# 使用 git commit 记录每次变化
```

## AI Agent 自动化优化工具链 (2026)

### 已成熟可用

| 工具 | 平台 | 核心能力 | 实测效果 |
|------|------|---------|---------|
| **AKO4ALL** | CUDA/Triton | 全自动 profile→iterate→verify 循环 | 8.93× (A100, 41轮, 2h) |
| **cuda-optimization-skill** | CUDA/CUTLASS/Triton/CuTe | NCU 驱动多维分析 + 定向修改 | 简单 kernel 效果好 |
| **HuggingFace cuda-kernels** | PyTorch CUDA Ext | PyTorch 集成，kernel hub 分发 | Qwen3-8B: 2.47× |
| **AMD GEAK-Triton v2** | AMD ROCm Triton | AMD GPU auto-tune | TritonBench: 3.42× |
| **AMD Apex** | AMD ROCm | RL-driven, 12 kernel types, 19 models | 开源 MIT |
| **Forge MCP** | Multi-GPU | 32 并行 agent swarm | 据称 vs torch.compile: up to 14× |
| **FACT** | CUTLASS | Agentic CUTLASS transpilation | MiniGPT: 2.79× |
| **μCUTLASS** | CUTLASS | Compact DSL + SOL guidance | 59 KernelBench: 1.56× |

### 选用建议
```
需要 AI Agent 辅助优化？
├─ 通用 CUDA kernel → AKO4ALL (最完备, 开源)
├─ PyTorch 自定义算子 → HuggingFace cuda-kernels skill
├─ CUTLASS GEMM/Attention 变体 → FACT / μCUTLASS (论文级精度)
├─ AMD GPU → GEAK-Triton v2 或 Apex
├─ 多 GPU 竞争最优 → Forge MCP (商业, 但最强)
└─ 学习/教学 → cuda-optimization-skill (透明, 可读)
```

## 人类专家思维清单

AI Agent 毕竟是辅助，以下是人类专家在优化时需要做的判断：

1. **"够好就行了"** — 达到硬件峰值 80% 通常足够，剩余 20% 投入回报急剧下降
2. **"Profile 不对 = 白优化"** — 锁定 GPU 时钟、固定输入大小、重复 3 次取中位数
3. **"先算法，后微调"** — O(n²)→O(n log n) 的改变远大于调整 block size
4. **"减少数据移动 > 增加计算"** — 数据是瓶颈，计算是廉价的
5. **"Benchmark-gaming 要警惕"** — 一个 kernel 快但整体 pipeline 慢 = 无用
6. **"明白你优化的是什么架构"** — H100 vs A100 vs MI300X vs M2 Ultra 策略完全不同
7. **"保持可移植性意识"** — 太深入特定架构的优化可能在新一代上变慢

## GPU Kernel 优化 Checklist

- [ ] 已运行 ncuerocprof 获取 Roofline 数据
- [ ] 已分类瓶颈：Memory / Compute / Occupancy / Latency / Launch
- [ ] 内存访问已 coalesced（连续线程 = 连续地址）
- [ ] 共享内存无 bank conflict（或已 padding 解决）
- [ ] 数据布局是 SoA（不是 AoS）
- [ ] 使用了合适的精度（fp16 能用就尽量用）
- [ ] Tile 大小 fit cache hierarchy
- [ ] 如果 GEMM 类，已考虑 CUTLASS / Triton 而非手写
- [ ] 如果重复计算，已用 `__shared__` 缓存
- [ ] 异步数据传输已启用（Streams / cp.async / TMA）
- [ ] 小 kernel 已融合（或使用 CUDA Graphs）
- [ ] Occupancy 在合理范围（通常 50-75% 最佳, 不追求 100%）
- [ ] 已重新 profile 验证改进
- [ ] 结果已 git commit（含改进幅度）

## 精选参考

- [NVIDIA Roofline Analysis Guide](https://docs.nvidia.com/nsight-compute/ProfilingGuide/)
- [AKO4ALL](https://github.com/TongmingLAIC/AKO4ALL)
- [cuda-optimization-skill](https://github.com/gxinlong/cuda-optimization-skill)
- [Awesome-Kernel-Skills](https://zhuanlan.zhihu.com/p/2022319499546821151) — 18 模块系统化调优
- [FACT (Agentic CUTLASS Transpilation)](https://arxiv.org/abs/2604.26666)
- [μCUTLASS (Compact DSL + SOL Guidance)](https://arxiv.org/abs/2603.29010)
- [GEAK-Triton v2](https://rocm.blogs.amd.com/)
- [AMD Apex](https://github.com/amd/apex)
- [HuggingFace upskill](https://github.com/huggingface/upskill)
