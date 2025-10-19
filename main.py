import tkinter as tk
from tkinter import messagebox
import algorithms as algo

def run_algorithm(algo_name):
    try:
        disk_size = int(disk_entry.get())
        head = int(head_entry.get())
        requests = list(map(int, req_entry.get().split(",")))
    except ValueError:
        messagebox.showerror("Error", "Please enter valid inputs!")
        return

    if algo_name == "FCFS":
        order, total, avg = algo.fcfs(requests, head)
    elif algo_name == "SSTF":
        order, total, avg = algo.sstf(requests, head)
    elif algo_name == "SCAN":
        order, total, avg = algo.scan(requests, head, disk_size, "left")
    elif algo_name == "C-SCAN":
        order, total, avg = algo.cscan(requests, head, disk_size)
    elif algo_name == "LOOK":
        order, total, avg = algo.look(requests, head, "left")
    elif algo_name == "C-LOOK":
        order, total, avg = algo.clook(requests, head)

    result_text.set(f"Order: {order}\nTotal Movement: {total}\nAverage Seek Time: {avg:.2f}")
    algo.plot(order, head, algo_name)

root = tk.Tk()
root.title("Disk Scheduling Simulator")
root.geometry("500x400")

tk.Label(root, text="Disk Size:").pack()
disk_entry = tk.Entry(root)
disk_entry.insert(0, "200")
disk_entry.pack()

tk.Label(root, text="Head Start Position:").pack()
head_entry = tk.Entry(root)
head_entry.insert(0, "50")
head_entry.pack()

tk.Label(root, text="Requests (comma-separated):").pack()
req_entry = tk.Entry(root)
req_entry.insert(0, "82,170,43,140,24,16,190")
req_entry.pack()

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, wraplength=400, justify="left").pack()

tk.Label(root, text="Choose Algorithm:").pack()

for name in ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"]:
    tk.Button(root, text=name, command=lambda n=name: run_algorithm(n)).pack(pady=2)

root.mainloop()
