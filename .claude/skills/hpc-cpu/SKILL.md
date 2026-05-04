---
name: hpc-cpu
description: CPU 高性能计算精华 — SIMD 向量化 (SSE/AVX/NEON/SVE)、多线程并行 (OpenMP/TBB)、数值线性代数 (BLAS/LAPACK/Eigen/MKL)、Cache/Memory 优化。用于 C/C++/Fortran/Python 性能关键代码的编写、审查、优化。
model: opus
---

# CPU 高性能计算 — 精华技能

## 快速决策：技术选型

```
性能瓶颈在哪？
├─ 数值线性代数（大矩阵乘法/分解）
│   ├─ 仅小矩阵(≤4x4) + 几何 → 纯 Eigen（固定大小类型，表达式模板零开销）
│   ├─ 开源 → Eigen + OpenBLAS（EIGEN_USE_BLAS + EIGEN_USE_LAPACKE）
│   ├─ Intel CPU 极致性能 → Eigen + MKL（EIGEN_USE_MKL_ALL）
│   ├─ macOS → Eigen + Apple Accelerate
│   └─ 需 GPU → cuBLAS/cuSOLVER，或 Eigen(fixed-size only on CUDA)
│
├─ 循环/数据并行
│   ├─ 简单 for 循环、遗留代码(C/Fortran) → OpenMP (#pragma omp parallel for)
│   ├─ 现代 C++17+、不规则负载、嵌套并行 → oneTBB (parallel_for, work-stealing)
│   ├─ Python → Numba @jit(nopython=True, parallel=True) 或 joblib
│   └─ Rust → rayon (parallel iterators)
│
├─ SIMD 向量化
│   ├─ x86 Intel/AMD → SSE4.2(128b) / AVX2(256b) / AVX-512(512b)
│   ├─ ARM (Apple M, 鲲鹏) → NEON(128b) / SVE(可变宽度)
│   ├─ 跨平台 → SIMDe（api兼容）或 SSE2NEON（仅SSE→NEON）
│   └─ 关键技巧：SoA 数据布局、64B cache-line 对齐、消除 false sharing
│
└─ 多线程架构设计
    ├─ 数据并行（均匀数据 → OpenMP static schedule）
    ├─ 任务并行（不规则 DAG → TBB flow::graph）
    └─ 流水线并行（多阶段 → TBB parallel_pipeline）
```

## SIMD 向量化 — 核心要点

### 数据布局是第一位的
- **SoA (Struct of Arrays)** 布局使编译器能生成连续 SIMD 加载，比 AoS 提升 60%+ 利用率
- **64-byte 对齐**：`alignas(64)` 或 `posix_memalign`，配合 `__builtin_assume_aligned(ptr, 64)`
- **消除 False Sharing**：多线程写入相邻变量时用 padding 隔开到不同 cache line

### x86 → ARM 移植速查表
| x86 (AVX2) | ARM (NEON) |
|---|---|
| `__m256` | `float32x4_t` (NEON 128b 用两个串起来) |
| `_mm256_load_ps` | `vld1q_f32` |
| `_mm256_fmadd_ps` | `vfmaq_f32` |
| `_mm256_store_ps` | `vst1q_f32` |

- 全功能等价库：[SIMDe](https://github.com/simd-everywhere/simde) (支持 SSE→NEON/AVX→SVE)
- 轻量 SSE→NEON：[SSE2NEON](https://github.com/DLTcollab/sse2neon)

### 编译器标志
```bash
# x86: 让编译器自动向量化
-O3 -march=native -mtune=native -ftree-vectorize

# ARM (Apple Silicon): 
-O3 -mcpu=apple-m1 -mtune=native

# 诊断：哪些循环被向量化了
-fopt-info-vec-all   # GCC
-Rpass=vector         # Clang
```

## 多线程并行 (OpenMP / TBB)

### OpenMP 最佳实践
```c
// 简单循环并行化（static schedule 适合均匀负载）
#pragma omp parallel for schedule(static) num_threads(N)
for (int i = 0; i < N; i++) { ... }

// 带 reduction
#pragma omp parallel for reduction(+:sum)
for (int i = 0; i < N; i++) sum += a[i];

// 嵌套并行（谨慎！容易 oversubscribe）
omp_set_nested(1);
#pragma omp parallel for num_threads(4)
for (...) {
    #pragma omp parallel for num_threads(2)
    for (...) { ... }
}
```
- 线程数 ≤ 物理核心数，避免 oversubscription
- `OMP_PROC_BIND=close` + `OMP_PLACES=cores` 绑定核心
- 与外部 BLAS 混用时：设 `OMP_NUM_THREADS` 和 `OPENBLAS_NUM_THREADS` 协调，避免 M×N 线程爆炸

### TBB 最佳实践
```cpp
// 适合不规则负载 — work-stealing 自动负载均衡
tbb::parallel_for(tbb::blocked_range<int>(0, N),
    [&](const tbb::blocked_range<int>& r) {
        for (int i = r.begin(); i != r.end(); i++) { ... }
    });

// 可组合 — 安全嵌套并行
tbb::task_group g;
g.run([&]{ do_work_a(); });
g.run([&]{ do_work_b(); });
g.wait();
```

### OpenMP vs TBB 选择
| 场景 | 选 |
|------|-----|
| 遗留 C/Fortran、简单 for 加速 | OpenMP |
| C++17+ 新项目、不规则负载 | TBB |
| 需要嵌套并行、与外部库共存 | TBB（work-stealing 更安全）|
| 单文件快速原型 | OpenMP（几行 pragma） |

## 数值线性代数 (BLAS / LAPACK / Eigen / MKL)

### 后端选择优先级
1. **Intel MKL** — x86 最强（AVX-512 优化），商业但有免费社区版
2. **OpenBLAS** — 开源最强，支持多架构，多线程
3. **BLIS** — 现代开源框架，AMD 官方推荐
4. **Apple Accelerate** — macOS/iOS 内置
5. **Netlib BLAS** — 参考实现（仅用于验证，勿用于生产）

### Eigen 核心技巧
- 固定大小矩阵用模板参数：`Eigen::Matrix4f`（编译期优化 + 无堆分配）
- 利用表达式模板：`mat = a * b + c * d` 是单次向量化循环，不是两次乘法+一次加法
- 大矩阵通过宏挂载后端：
```cpp
#define EIGEN_USE_MKL_ALL       // MKL 全替换
#define EIGEN_USE_BLAS           // 仅 BLAS 替换
#define EIGEN_USE_LAPACKE        // 仅 LAPACK 替换
```
- 编译器标志：`-O3 -DNDEBUG -march=native -mtune=native`

### 多线程配置（避免与应用程序争抢）
```bash
export MKL_NUM_THREADS=4       # MKL
export OPENBLAS_NUM_THREADS=4  # OpenBLAS
export OMP_NUM_THREADS=4       # OpenMP 通用
```

## Cache / Memory 优化

### 优化层级与收益
| 层级 | 典型收益 | 方法 |
|------|---------|------|
| 算法降复杂度 | 10×–1000× | O(n³)→O(n²) 算法替换 |
| 数据结构 | 2×–10× | SoA, 紧凑结构, 小类型 |
| 内存分配 | 2×–5× | pool, arena, stack alloc |
| Cache 友好 | 1.5×–3× | tiling, prefetch, 对齐 |
| SIMD | 2×–8× | 向量化 + 正确数据布局 |

### 关键技巧
- **Tiling (分块)**：使工作集 fit L1/L2 cache，对大矩阵操作收益巨大
- **Prefetch**：`__builtin_prefetch(&data[i+64], 0, 3)` 隐藏 30-50% 内存延迟；但在带宽饱和时禁用
- **Cache-line 对齐**：`alignas(64)` 避免 false sharing
- **NUMA 感知**：`numactl --cpunodebind=0 --membind=0 ./app`，或 `libnuma` API

## 性能分析工具链

| 工具 | 用途 | 关键命令 |
|------|------|---------|
| `perf` | CPU PMU 采样 | `perf record -g ./app && perf report` |
| `valgrind --tool=cachegrind` | Cache miss 分析 | `valgrind --tool=cachegrind ./app` |
| Intel Advisor | 向量化诊断 + Roofline | GUI |
| `likwid-perfctr` | 微架构计数器 | `likwid-perfctr -C 0 -g MEM_DP ./app` |
| `numastat` | NUMA 命中率 | `numastat -p <pid>` |

## 精选参考

- [Intel Intrinsics Guide](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html) — x86 SIMD 指令速查
- [Eigen MKL 集成](https://eigen.tuxfamily.org/dox/TopicUsingIntelMKL.html)
- [MKL Link Line Advisor](https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl-link-line-advisor.html)
- [SIMDe](https://github.com/simd-everywhere/simde) / [SSE2NEON](https://github.com/DLTcollab/sse2neon)
- [oneTBB 文档](https://oneapi-src.github.io/oneTBB/)
