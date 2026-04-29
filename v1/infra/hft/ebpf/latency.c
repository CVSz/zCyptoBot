#include <uapi/linux/ptrace.h>

BPF_HASH(start, u64);

int trace_start(struct pt_regs *ctx) {
    u64 pid = bpf_get_current_pid_tgid();
    u64 ts = bpf_ktime_get_ns();
    start.update(&pid, &ts);
    return 0;
}

int trace_end(struct pt_regs *ctx) {
    u64 pid = bpf_get_current_pid_tgid();
    u64 *tsp = start.lookup(&pid);
    if (tsp != 0) {
        u64 delta = bpf_ktime_get_ns() - *tsp;
        bpf_trace_printk("latency(ns): %llu\\n", delta);
        start.delete(&pid);
    }
    return 0;
}
