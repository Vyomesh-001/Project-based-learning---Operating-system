import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import algorithms as algo

annotations = []

def on_plot_click(event):
    for ann in annotations:
        ann.remove()
    annotations.clear()

    if event.inaxes:
        x_click = event.xdata
        y_click = event.ydata
        text = f"Order: {x_click:.0f}\nCylinder: {y_click:.0f}"
        ax = event.inaxes

        ann = ax.annotate(
            text, xy=(x_click, y_click), xytext=(10, 10),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.4", fc="yellow", alpha=0.8),
            arrowprops=dict(arrowstyle="->")
        )

        annotations.append(ann)
        canvas_path.draw()


def run_full_simulation():
    try:
        disk_size = int(disk_entry.get())
        head = int(head_entry.get())
        requests = list(map(int, req_entry.get().replace(" ", "").split(",")))
    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers!")
        return

    direction = direction_var.get()
    selected_algo = algo_var.get()

    algorithms = {
        "FCFS": lambda: algo.fcfs(requests, head),
        "SSTF": lambda: algo.sstf(requests, head),
        "SCAN": lambda: algo.scan(requests, head, disk_size, direction),
        "C-SCAN": lambda: algo.cscan(requests, head, disk_size),
        "LOOK": lambda: algo.look(requests, head, direction),
        "C-LOOK": lambda: algo.clook(requests, head)
    }

    all_results = {}

    if selected_algo != "ALL":
        order, total, avg = algorithms[selected_algo]()
        all_results[selected_algo] = {"order": order, "total": total, "avg": avg}
    else:
        for name, func in algorithms.items():
            order, total, avg = func()
            all_results[name] = {"order": order, "total": total, "avg": avg}

    update_treeview(all_results)
    update_path_plot(all_results, head)
    update_bar_chart(all_results)


def update_path_plot(results, initial_head):
    fig_path.clf()
    ax_path = fig_path.add_subplot(111)
    ax_path.set_title("Disk Head Movement Path")
    ax_path.set_xlabel("Order of Service")
    ax_path.set_ylabel("Cylinder Number")

    for name, data in results.items():
        path = [initial_head] + data['order']
        x = list(range(len(path)))
        ax_path.plot(x, path, marker='o', label=name)

    ax_path.legend(loc='upper right')
    canvas_path.draw()


def update_bar_chart(results):
    fig_bar.clf()
    ax_bar = fig_bar.add_subplot(111)
    ax_bar.set_title("Total Head Movement Comparison")
    ax_bar.set_ylabel("Total Movement")

    algos = list(results.keys())
    totals = [results[a]['total'] for a in algos]

    
    color_map = {
        "FCFS": "blue",
        "SSTF": "orange",
        "SCAN": "green",
        "C-SCAN": "red",
        "LOOK": "purple",
        "C-LOOK": "brown"
    }

    colors = [color_map[a] for a in algos]

    ax_bar.bar(algos, totals, color=colors, width=0.45)

    canvas_bar.draw()


def update_treeview(results):
    for item in tree.get_children():
        tree.delete(item)

    for name, data in results.items():
        tree.insert("", "end", values=(
            name,
            data["total"],
            f"{data['avg']:.2f}",
            str(data["order"])
        ))


root = tk.Tk()
root.title("Disk Scheduling Simulator")
root.state('zoomed')

input_frame = tk.Frame(root, padx=10, pady=10, bd=2, relief=tk.RIDGE)
input_frame.pack(fill='x')

tk.Label(input_frame, text="Disk Size:").grid(row=0, column=0)
disk_entry = tk.Entry(input_frame, width=10)
disk_entry.insert(0, "200")
disk_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Head Start Position:").grid(row=0, column=2)
head_entry = tk.Entry(input_frame, width=10)
head_entry.insert(0, "50")
head_entry.grid(row=0, column=3)

tk.Label(input_frame, text="Requests:").grid(row=1, column=0)
req_entry = tk.Entry(input_frame, width=40)
req_entry.insert(0, "82,170,43,140,24,16,190")
req_entry.grid(row=1, column=1, columnspan=3)

tk.Label(input_frame, text="Initial Direction:").grid(row=0, column=4)
direction_var = tk.StringVar(value="left")
tk.Radiobutton(input_frame, text="Left", variable=direction_var, value="left").grid(row=0, column=5)
tk.Radiobutton(input_frame, text="Right", variable=direction_var, value="right").grid(row=0, column=6)

tk.Label(input_frame, text="Select Algorithm:").grid(row=2, column=0)
algo_var = tk.StringVar()
algo_combo = ttk.Combobox(
    input_frame, textvariable=algo_var,
    values=["ALL", "FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"],
    state="readonly", width=15
)
algo_combo.current(0)
algo_combo.grid(row=2, column=1)

tk.Button(
    input_frame, text="Run Simulation",
    command=run_full_simulation, bg="lightblue"
).grid(row=2, column=4, columnspan=3)

vis_frame = tk.Frame(root)
vis_frame.pack(fill='both', expand=True)
vis_frame.grid_columnconfigure(0, weight=1)
vis_frame.grid_columnconfigure(1, weight=1)

fig_path = plt.Figure(figsize=(5, 4), dpi=100)
canvas_path = FigureCanvasTkAgg(fig_path, master=vis_frame)
canvas_widget_path = canvas_path.get_tk_widget()
canvas_widget_path.grid(row=0, column=0, sticky='nsew')

toolbar_path = NavigationToolbar2Tk(canvas_path, vis_frame, pack_toolbar=False)
toolbar_path.grid(row=1, column=0, sticky='ew')

fig_path.canvas.mpl_connect('button_press_event', on_plot_click)

fig_bar = plt.Figure(figsize=(5, 4), dpi=100)
canvas_bar = FigureCanvasTkAgg(fig_bar, master=vis_frame)
canvas_widget_bar = canvas_bar.get_tk_widget()
canvas_widget_bar.grid(row=0, column=1, sticky='nsew')

toolbar_bar = NavigationToolbar2Tk(canvas_bar, vis_frame, pack_toolbar=False)
toolbar_bar.grid(row=1, column=1, sticky='ew')

console_frame = tk.Frame(root, padx=10, pady=5, bd=2, relief=tk.GROOVE)
console_frame.pack(fill='x')

tk.Label(console_frame, text="Analysis Console:", font=('Arial', 10, 'bold')).pack(anchor='w')

columns = ("Algorithm", "Total Movement", "Avg Seek", "Sequence")
tree = ttk.Treeview(console_frame, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col)

tree.pack(fill='x')

run_full_simulation()
root.mainloop()

=======
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

