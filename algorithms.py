import matplotlib.pyplot as plt

def fcfs(requests, head):
    order = []
    total = 0
    for req in requests:
        total += abs(head - req)
        order.append(req)
        head = req
    return order, total, total / len(requests)  

def sstf(requests, head):
    reqs = requests.copy()
    order, total = [], 0
    while reqs:
        closest = min(reqs, key=lambda x: abs(x - head))
        total += abs(head - closest)
        order.append(closest)
        head = closest
        reqs.remove(closest)
    return order, total, total / len(order)

def scan(requests, head, disk_size, direction="left"):
    order = []
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    left.sort(reverse=True)
    right.sort()
    total = 0
    if direction == "left":
        seq = left + [0] + right
    else:
        seq = right + [disk_size - 1] + left
    for req in seq:
        total += abs(head - req)
        order.append(req)
        head = req
    return order, total, total / len(order)

def cscan(requests, head, disk_size):
    order = []
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    left.sort()
    right.sort()
    seq = right + [disk_size - 1, 0] + left
    total = 0
    for req in seq:
        total += abs(head - req)
        order.append(req)
        head = req
    return order, total, total / len(order)

def look(requests, head, direction="left"):
    order = []
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    left.sort(reverse=True)
    right.sort()
    total = 0
    if direction == "left":
        seq = left + right
    else:
        seq = right + left
    for req in seq:
        total += abs(head - req)
        order.append(req)
        head = req
    return order, total, total / len(order)

def clook(requests, head):
    order = []
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]
    left.sort()
    right.sort()
    seq = right + left
    total = 0
    for req in seq:
        total += abs(head - req)
        order.append(req)
        head = req
    return order, total, total / len(order)

def plot(order, head, title):
    seq = [head] + order
    plt.plot(range(len(seq)), seq, marker="o")
    plt.title(title)
    plt.xlabel("Step")
    plt.ylabel("Track Number")
    plt.grid(True)
    plt.show()
