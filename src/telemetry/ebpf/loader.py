# Optional: requires bcc and root privileges
from bcc import BPF
from time import sleep

def run():
    with open('src/telemetry/ebpf/ctxswitch.c') as f:
        b = BPF(text=f.read())
    # symbol may differ by kernel; adjust as needed
    b.attach_kprobe(event="finish_task_switch.isra.0", fn_name="on_sched_switch")
    print("Collecting context switches... Ctrl-C to stop")
    while True:
        sleep(1)
        total = 0
        for _, v in b.get_table('ctx_count').items():
            total += v.value
        print({'ctx_switches': int(total)})

if __name__ == '__main__':
    run()
