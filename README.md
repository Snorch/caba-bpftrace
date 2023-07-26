Usage example:

- Create pid namespace:

```
unshare -mp --fork --mount-proc
```

- Find id of pid namespace from init process:

```
ls -l /proc/54643/ns/pid
lrwxrwxrwx 1 root root 0 июл 26 15:09 /proc/54643/ns/pid -> 'pid:[4026534507]'
```

- Start collecting CABA data:

```
./caba.bt 4026534507
Attaching 4 probes...
usage: caba.bt [pidns_inum]
Tracing process tree events in pidns 4026534507 and descendants. Hit Ctrl-C to end.
...
```

- Run the load in pid namespace (from unshare):

```
gcc -o tests/test01 tests/test01.c
./tests/test01
```

- Save output of caba.bt:

```
cat trace
kprobe:sched_post_fork: 92454 54643
kprobe:sched_post_fork: 92455 92454
kprobe:sched_post_fork: 92456 92455
kprobe:sched_post_fork: 92457 92456
kprobe:release_task: 92455
kprobe:sched_post_fork: 92458 92457
kprobe:release_task: 92457
kprobe:sched_post_fork: 92459 92458
kprobe:sched_post_fork: 92460 92459
kprobe:sched_post_fork: 92461 92460
kprobe:release_task: 92459
kprobe:sched_post_fork: 92462 92461
kprobe:release_task: 92461
kprobe:sched_post_fork: 92463 92462
kprobe:sched_post_fork: 92464 92463
kprobe:release_task: 92463
kprobe:sched_post_fork: 92465 92464
kprobe:sched_post_fork: 92466 92465
kprobe:sched_post_fork: 92467 92466
kprobe:release_task: 92465
kprobe:sched_post_fork: 92468 92467
kprobe:sched_post_fork: 92469 92468
kprobe:release_task: 92467
kprobe:sched_post_fork: 92470 92469
kprobe:release_task: 92469
kprobe:sched_post_fork: 92471 92470
kprobe:sched_post_fork: 92472 92471
kprobe:sched_post_fork: 92473 92472
kprobe:release_task: 92471
kprobe:sched_post_fork: 92474 92473
kprobe:release_task: 92473
```

Visualize output of caba.bt (don't kill test01 processes yet, provide 54643 - pidns init pid):

```
./caba_parse.py trace 54643 trace.png
```

![alt text](https://github.com/snorch/caba-bpftrace/blob/master/trace.png?raw=true)

Red arrows show parent relations and Blue arrows show CABA relations, which indicate the original place from where processes were created.
