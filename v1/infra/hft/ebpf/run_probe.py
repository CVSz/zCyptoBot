from bcc import BPF


def main() -> None:
    b = BPF(src_file="infra/hft/ebpf/latency.c")
    b.attach_kprobe(event="sys_sendto", fn_name="trace_start")
    b.attach_kretprobe(event="sys_sendto", fn_name="trace_end")
    b.trace_print()


if __name__ == "__main__":
    main()
