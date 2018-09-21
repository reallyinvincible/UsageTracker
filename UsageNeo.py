import tkinter as tk
import psutil
from matplotlib import style
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import ttk

//Using style other than default Style
style.use("dark_background")
LARGE_FONT = ("Verdana", 12)
time = -50
ram = [0 for i in range(50)]
cpu = [0 for i in range(50)]
disk = [0 for i in range(50)]

class Data_Usage(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Usage Tracker")
        container = tk.Frame(self)

        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        frame = HomePage(container, self)

        self.frames[HomePage] = frame

        frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Usage Tracker", font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)

        RAM_Button = ttk.Button(self, text = "RAM Usage", command = check_ram)
        RAM_Button.pack()

        DISK_Button = ttk.Button(self, text="Disk Usage", command = check_disk)
        DISK_Button.pack()

        CPU_Button = ttk.Button(self, text="CPU Usage", command = check_cpu)
        CPU_Button.pack()

def check_ram():
    time = -50
    fig1 = plt.figure()
    ax2 = plt.subplot2grid((10,9), (7,3), rowspan = 4, colspan = 3)
    ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 5, colspan = 1)
    used_ram = 0
    total_ram = 0

    def animate_ram(i):
        global time,ram
        ax1.clear()
        ax2.clear()
        used_ram = psutil.virtual_memory()[3]
        total_ram = psutil.virtual_memory()[0]
        if (time < 0):
            ram.pop()
            ram.insert(0, psutil.virtual_memory()[2])
            ax2.pie([ram[0], (100 - ram[0])], labels=['Used RAM\n' + str(round(used_ram / (1024 ** 3), 1)) + 'GB',
                                                        'Available RAM\n' + str(
                                                            round((total_ram - used_ram) / (1024 ** 3), 1)) + 'GB'],
                    shadow=True, startangle=90, autopct='%1.1f%%', explode=(0.1, 0.1), colors=['crimson', 'c'],
                    labeldistance=1.3)
            ax1.plot([i for i in range(50)], ram, label="RAM Usage")
        else:
            ram = ram[1:]
            ram.append(psutil.virtual_memory()[2])
            ax2.pie([ram[-1], (100 - ram[-1])], labels=['Used RAM\n' + str(round(used_ram / (1024 ** 3), 1)) + 'GB',
                                                        'Available RAM\n' + str(
                                                            round((total_ram - used_ram) / (1024 ** 3), 1)) + 'GB'],
                    shadow=True, startangle=90, autopct='%1.1f%%', explode=(0.1, 0.1), colors=['crimson', 'c'],
                    labeldistance=1.3)
            ax1.plot([i for i in range(time, time + 50)], ram, label="RAM Usage")

        time += 1
        plt.title("RAM Usage Percentage")
        plt.xlabel("Time")
        plt.ylabel("Percentage Use")
        plt.legend()
    ani_ram = animation.FuncAnimation(fig1, animate_ram, interval=1000)
    plt.show()
    

def check_disk():
    time = -50
    fig1 = plt.figure()
    ax2 = plt.subplot2grid((10,9), (7,3), rowspan = 4, colspan = 3)
    ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 5, colspan = 1)

    def animate_disk(i):
        global time,disk
        ax1.clear()
        ax2.clear()
        used_disk = 0
        total_disk = 0
        for drive in psutil.disk_partitions(all=False):
            if os.name == 'nt':
                if 'cdrom' in drive.opts or drive.fstype == '':
                    continue
                usage = psutil.disk_usage(drive.mountpoint)
                total_disk += usage.total
                used_disk += usage.used
        if (time < 0):
            disk.pop()
            disk.insert(0, (used_disk/total_disk*100))
            ax2.pie([disk[0], (100 - disk[0])], labels=['Used DISK\n' + str(round(used_disk / (1024 ** 3), 1)) + 'GB',
                                                          'Available DISK\n' + str(
                                                              round((total_disk - used_disk) / (1024 ** 3), 1)) + 'GB'],
                    shadow=True, startangle=90, autopct='%1.1f%%', explode=(0.1, 0.1), colors=['crimson', 'c'],
                    labeldistance=1.3)
            ax1.plot([i for i in range(50)], disk, label="DISK Usage")
        else:
            disk = disk[1:]
            disk.append((used_disk / total_disk * 100))
            ax2.pie([disk[-1], (100 - disk[-1])], labels=['Used DISK\n' + str(round(used_disk / (1024 ** 3), 1)) + 'GB',
                                                          'Available DISK\n' + str(
                                                              round((total_disk - used_disk) / (1024 ** 3), 1)) + 'GB'],
                    shadow=True, startangle=90, autopct='%1.1f%%', explode=(0.1, 0.1), colors=['crimson', 'c'],
                    labeldistance=1.3)
            ax1.plot([i for i in range(time, time + 50)], cpu, label="DISK Usage")

        time += 1
        plt.title("DISK Usage Percentage")
        plt.xlabel("Time")
        plt.ylabel("Percentage Use")
        plt.legend()

    ani_disk = animation.FuncAnimation(fig1, animate_disk, interval=1000)
    plt.show()

def check_cpu():
    time = -50
    fig1 = plt.figure()
    ax2 = plt.subplot2grid((10,9), (7,3), rowspan = 4, colspan = 3)
    ax1 = plt.subplot2grid((10,1), (0,0), rowspan = 5, colspan = 1)

    def animate_cpu(i):
        global time,cpu
        ax1.clear()
        ax2.clear()
        if(time < 0):
            cpu.pop()
            cpu.insert(0, psutil.cpu_percent(interval=1))
            ax2.pie([cpu[0], (100 - cpu[0])], labels=['Used CPU', 'Available CPU'], shadow=True, startangle=90,
                    autopct='%1.1f%%', explode=(0.1, 0.1), colors=['crimson', 'c'])
            ax1.plot([i for i in range(50)], cpu, label="CPU Usage")
        else:
            cpu = cpu[1:]
            cpu.append(psutil.cpu_percent(interval=1))
            ax2.pie([cpu[-1], (100 - cpu[-1])], labels=['Used CPU', 'Available CPU'], shadow=True, startangle=90,
                    autopct='%1.1f%%', explode=(0.1, 0.1), colors=['crimson', 'c'])
            ax1.plot([i for i in range(time, time + 50)], cpu, label="CPU Usage")

        time += 1
        plt.title("CPU Usage Percentage")
        plt.xlabel("Time")
        plt.ylabel("Percentage Use")
        plt.legend()

    ani_cpu = animation.FuncAnimation(fig1, animate_cpu, interval=1000)
    plt.show()


app = Data_Usage()
app.mainloop()
