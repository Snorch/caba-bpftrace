#!/usr/bin/python3
import sys
import pydot

if len(sys.argv) != 4:
    print(f"usage: {sys.argv[0]} </path/to/parse> <init_pid> </path/to/result>")
    exit(1)

cabds_map={int(sys.argv[2]): []}
caba_map={}

with open(sys.argv[1]) as f:
    for line in f:
        if "kprobe:sched_post_fork:" in line:
            forked_task, forked_task_caba = [int(i) for i in line.strip().split()[1:3]]
            cabds_map[forked_task] = []
            cabds_map[forked_task_caba].append(forked_task)
            caba_map[forked_task] = forked_task_caba
        elif "kprobe:release_task:" in line:
            released_task = int(line.strip().split()[1])
            new_caba = caba_map[released_task]

            for cabd in cabds_map[released_task]:
                caba_map[cabd] = new_caba
            cabds_map[new_caba].remove(released_task)
            cabds_map[new_caba] += cabds_map[released_task]

            del cabds_map[released_task]
            del caba_map[released_task]

gr = pydot.Dot(graph_type='digraph')

for node in cabds_map.keys():
    nod = pydot.Node(node, label=node)
    gr.add_node(nod)

for node in cabds_map.keys():
    for edge in cabds_map[node]:
        edg = pydot.Edge(node, edge, color='blue')
        gr.add_edge(edg)

ppid_map={}
for node in cabds_map.keys():
    if node == int(sys.argv[2]):
        continue
    with open(f"/proc/{node}/status") as status:
        for line in status:
            if "PPid:" in line:
                ppid_map[node] = int(line.strip().split()[1])

for node in ppid_map.keys():
    edg = pydot.Edge(ppid_map[node], node, color='red')
    gr.add_edge(edg)

gr.write_png(sys.argv[3])
# gr.write(sys.argv[3])
