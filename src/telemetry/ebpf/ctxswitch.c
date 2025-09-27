#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
BPF_HASH(ctx_count, u32, u64);

int on_sched_switch(struct pt_regs *ctx, struct task_struct *prev) {
    u32 cpu = bpf_get_smp_processor_id();
    u64 *val = ctx_count.lookup(&cpu);
    if (!val) {
        u64 one = 1;
        ctx_count.update(&cpu, &one);
    } else {
        __sync_fetch_and_add(val, 1);
    }
    return 0;
}
