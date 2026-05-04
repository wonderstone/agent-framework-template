---
name: hpc-gpu-crossplatform
description: 跨平台 GPU 计算精华 — OpenCL / Vulkan Compute / SYCL DPC++ / OpenACC / SPIR-V。跨 NVIDIA/AMD/Intel/嵌入式 GPU 的可移植并行计算方案选型与最佳实践。
model: opus
---

# 跨平台 GPU 计算 — 精华技能

## 四大跨平台 API 对比

| API | 语言 | 硬件覆盖 | 成熟度 | 最适合场景 |
|-----|------|---------|--------|-----------|
| **OpenCL 3.0** | C99 kernel + C/C++ host | 最广（含 FPGA/DSP） | 15年+ | 嵌入式、遗留系统、FPGA、最大覆盖面 |
| **SYCL / DPC++** | 单一源 C++17 | NVIDIA/AMD/Intel/FPGA | 快速增长中 | 现代C++项目、HPC、Intel生态 |
| **Vulkan Compute** | GLSL/HLSL→SPIR-V | GPU(含手机/嵌入式) | 成熟 | Android手机GPU、图形+计算融合 |
| **OpenACC** | 指令/pragma | NVIDIA/AMD/Intel | 稳定但增长慢 | 遗留Fortran/C科学代码快速GPU化 |

## 快速决策：选择指南

```
需要跨平台 GPU 计算？
├─ 只需 NVIDIA → CUDA（生态最成熟，勿折腾）
├─ NVIDIA + AMD + Intel，现代 C++ → SYCL / DPC++ (oneAPI 或 AdaptiveCpp)
├─ 最广硬件覆盖 (含手机 GPU、FPGA、DSP) → OpenCL 3.0
├─ Android 移动端 GPU 计算 → Vulkan Compute（OpenCL 在 Android 上驱动缺失严重）
├─ 遗留 Fortran/C 科学代码 → OpenACC（几行 pragma 即可）
├─ GPU 渲染 + 计算混合 → Vulkan Compute（与图形管线共享资源）
└─ 未来防锁定 → SYCL + SPIR-V（多个运行时可选）
```

## SYCL / DPC++ — 现代跨平台首选

### 核心语法（类 CUDA 但标准 C++17）
```cpp
#include <sycl/sycl.hpp>
using namespace sycl;

// 基本并行
queue q(gpu_selector_v);
buffer<float, 1> buf(data, range<1>(N));
q.submit([&](handler& h) {
    auto acc = buf.get_access<access::mode::read_write>(h);
    h.parallel_for(range<1>(N), [=](id<1> i) {
        acc[i] = acc[i] * 2.0f;        // 与 CUDA kernel 几乎相同
    });
}).wait();

// USM (Unified Shared Memory) — 更接近 CUDA 风格
float* data = malloc_shared<float>(N, q);
q.parallel_for(range<1>(N), [=](id<1> i) {
    data[i] = data[i] * 2.0f;
}).wait();
free(data, q);
```

### 两种实现选哪个？
| 实现 | 优点 | 缺点 |
|------|------|------|
| **Intel oneAPI DPC++** | 官方, 工具链全 (VTune, Advisor) | Intel GPU 优先，NVIDIA/AMD 通过插件 |
| **AdaptiveCpp** (原 hipSYCL) | 真正多后端 (CUDA/HIP/OpenCL/Vulkan/LevelZero) | 社区驱动，Intel 官方支持弱 |

### 关键提示
- 用 **USM (malloc_shared)** 而非 buffer/accessor 写新代码（更像 CUDA 心智模型）
- subgroup (类似 CUDA warp) 操作可跨 API 移植：`sycl::sub_group`
- `-fsycl` 编译，`-fsycl-targets=nvptx64-nvidia-cuda,amdgcn-amd-amdhsa` 指定后端

## OpenCL 3.0 — 最广覆盖

### 最小可用 kernel
```c
// kernel.cl
__kernel void vec_add(__global const float* a,
                      __global const float* b,
                      __global float* c) {
    int gid = get_global_id(0);
    c[gid] = a[gid] + b[gid];
}
```
```c
// host.c (简化)
clGetPlatformIDs(1, &platform, NULL);
clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, NULL);
context = clCreateContext(NULL, 1, &device, NULL, NULL, NULL);
queue = clCreateCommandQueueWithProperties(context, device, 0, NULL);
program = clCreateProgramWithSource(context, 1, &src, NULL, NULL);
clBuildProgram(program, 1, &device, NULL, NULL, NULL);
kernel = clCreateKernel(program, "vec_add", NULL);
clEnqueueNDRangeKernel(queue, kernel, 1, NULL, &global, &local, 0, NULL, NULL);
```

### OpenCL 2026 现状
- NVIDIA: OpenCL 支持退化（优先 CUDA），更新缓慢
- Intel: 转向 oneAPI/Level Zero，OpenCL 仅维护
- AMD: 持续支持但更新不如 HIP/ROCm
- **最适合**: 嵌入式 GPU (Mali/Adreno/PowerVR)、FPGA、DSP、遗留代码维护

## Vulkan Compute — 手机 GPU 的救星

### 为什么选 Vulkan Compute over OpenCL？
- Android 手机：绝大多数 GPU (Adreno/Mali/PowerVR) 有 Vulkan 驱动但**无** OpenCL 驱动
- 图形+计算一体化：与 render pass 共享资源（如实时视频处理+显示）
- 更细粒度控制：显式 pipeline barriers, memory barriers, queue management

### 降低复杂度 — Kompute 库
```cpp
// Kompute: 隐藏 Vulkan 数百行样板代码
Manager mgr;
auto tensorA = mgr.tensor({1, 2, 3, 4, 5}, {DType::Float32});
auto tensorB = mgr.tensor({5, 4, 3, 2, 1}, {DType::Float32});
auto tensorC = mgr.tensor({0, 0, 0, 0, 0}, {DType::Float32});

// Shader 作为 Python 字符串传入
mgr.algorithm({tensorA, tensorB}, {tensorC}, shaderSource)->eval();
```

### Vulkan Compute 局限
- 极其啰嗦（样板代码数百行）— 必须用 Kompute 或类似封装
- 不支持 FP64（双精度）— 硬件限制
- subgroup 操作支持不统一（需检查 `VkPhysicalDeviceSubgroupProperties`）

## OpenACC — 遗留代码的快速 GPU 化

```fortran
! Fortran: 一行 pragma 即可 GPU 并行
!$acc parallel loop copyin(a,b) copyout(c)
do i = 1, N
    c(i) = a(i) + b(i)
end do
!$acc end parallel loop
```

```c
// C: 同样简单
#pragma acc parallel loop copyin(a[0:N],b[0:N]) copyout(c[0:N])
for (int i = 0; i < N; i++)
    c[i] = a[i] + b[i];
```

- 编译器支持：NVIDIA HPC SDK, GCC 13+ (部分)
- 局限：仅适合循环级并行，复杂 kernel 需要 CUDA/HIP

## SPIR-V — 统一的中间表示

```
Kernel 源 → SPIR-V → GPU 驱动 (Vulkan / OpenCL / SYCL)

编译工具:
- clspv:     OpenCL C → Vulkan SPIR-V
- clspv-opt: SPIR-V 优化器
- dxc:       HLSL → DXIL / SPIR-V
- slang:     Slang → SPIR-V
```

SPIR-V 的价值在于**分离 kernel 编写和运行时选择**：
- 同一个 SPIR-V 二进制可以被 Vulkan Compute 或 OpenCL 运行时加载
- 允许在部署时根据设备动态选择最佳后端

## 跨平台优化通用原则

以下技巧在 CUDA/OpenCL/SYCL/Vulkan 中均有效：

1. **Tiling**: 让工作组/block 的数据 fit local memory/shared memory
2. **Coalesced access**: 连续工作项访问连续地址（对所有 GPU 架构都适用）
3. **Subgroup/Warp 操作**: 利用 `sub_group` / `warp` 级 shuffle/reduce
4. **异步操作**: 重叠 kernel 执行与数据传输（多队列/多 stream）
5. **避免 host-device 同步**: 批量提交 + fence 而非逐个等待

## 精选参考

- [SYCL 2020 Specification](https://www.khronos.org/sycl/)
- [Intel oneAPI DPC++](https://www.intel.com/content/www/us/en/developer/tools/oneapi/dpc-compiler.html)
- [AdaptiveCpp](https://github.com/AdaptiveCpp/AdaptiveCpp)
- [OpenCL 3.0 Specification](https://www.khronos.org/opencl/)
- [Vulkan Compute Guide](https://docs.vulkan.org/guide/latest/compute.html)
- [Kompute](https://github.com/KomputeProject/kompute)
- [OpenACC Programming Guide](https://www.openacc.org/)
- [SPIR-V Guide](https://www.khronos.org/spir/)
