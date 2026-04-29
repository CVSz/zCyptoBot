#include <linux/bpf.h>

int xdp_prog(struct xdp_md *ctx) {
    (void)ctx;
    return XDP_PASS;
}
