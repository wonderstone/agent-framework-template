#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <Accelerate/Accelerate.h>  // Apple Accelerate = BLAS on macOS

#define N 1024                         // 1024x1024 matrices

static float A[N*N], B[N*N], C[N*N];

double now_ms() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec * 1000.0 + ts.tv_nsec / 1e6;
}

/* ── Version 1: Naive i‑j‑k, terrible cache behavior ── */
void matmul_naive() {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) {
            float sum = 0;
            for (int k = 0; k < N; k++)
                sum += A[i*N + k] * B[k*N + j];  // B 按列访问 → stride-N, cache miss 爆炸
            C[i*N + j] = sum;
        }
}

/* ── Version 2: Loop reorder (i‑k‑j) + tiling, per skill advice ── */
void matmul_tiled() {
    const int TILE = 64;  // fit L1 cache (M1: 128 KB per cluster, 64x64x4 ≈ 16 KB)
    for (int ii = 0; ii < N; ii += TILE)
        for (int kk = 0; kk < N; kk += TILE)
            for (int jj = 0; jj < N; jj += TILE)
                for (int i = ii; i < ii+TILE && i < N; i++)
                    for (int k = kk; k < kk+TILE && k < N; k++) {
                        float aik = A[i*N + k];
                        for (int j = jj; j < jj+TILE && j < N; j++)
                            C[i*N + j] += aik * B[k*N + j];
                    }
}

/* ── Version 3: Apple Accelerate (BLAS), per skill recommendation ── */
void matmul_blas() {
    cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                N, N, N, 1.0f, A, N, B, N, 0.0f, C, N);
}

int main() {
    // init
    for (int i = 0; i < N*N; i++) { A[i] = (float)rand()/RAND_MAX; B[i] = (float)rand()/RAND_MAX; }

    double t0, ms;

    // warmup
    memset(C, 0, sizeof(C));
    matmul_naive();
    memset(C, 0, sizeof(C));
    matmul_tiled();
    memset(C, 0, sizeof(C));
    matmul_blas();

    // ── naive ──
    memset(C, 0, sizeof(C));
    t0 = now_ms();
    matmul_naive();
    ms = now_ms() - t0;
    printf("naive (i-j-k)       %8.0f ms   %.1f MFLOPS\n", ms,
           (2.0*N*N*N/1e6) / (ms/1000));

    // ── tiled ──
    memset(C, 0, sizeof(C));
    t0 = now_ms();
    matmul_tiled();
    ms = now_ms() - t0;
    printf("tiled (i-k-j+64)    %8.0f ms   %.1f MFLOPS\n", ms,
           (2.0*N*N*N/1e6) / (ms/1000));

    // ── Accelerate ──
    memset(C, 0, sizeof(C));
    t0 = now_ms();
    matmul_blas();
    ms = now_ms() - t0;
    printf("cblas_sgemm         %8.0f ms   %.1f MFLOPS\n", ms,
           (2.0*N*N*N/1e6) / (ms/1000));

    return 0;
}
