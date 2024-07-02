import tkinter as tk
import time
import subprocess
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import speedtest


def popup_baud_rate(self) :
        transmission_rate = 9600  # in bits per second
        num_bits_per_signal = 8  # for 8-bit data
        baud_rate = transmission_rate / num_bits_per_signal
        return baud_rate


def calculate_latency():
    rtt = 0.2
    return (rtt / 2) * 1000

def update_latency_display(latency_label, root):
    latency = calculate_latency()
    latency_label.config(text=f"{latency} ms")
    root.after(1000, update_latency_display, latency_label, root)  # Update every second

def popup_latency(self):
    root = tk.Tk()
    root.title("Latency")

    # Create a canvas to draw the circular design
    canvas = tk.Canvas(root, width=200, height=200, bg="black", highlightthickness=0)
    canvas.pack(pady=20)

    # Draw a circle
    canvas.create_oval(10, 10, 190, 190, outline="white", width=5)

    # Create a label to display the latency inside the circle
    latency_label = tk.Label(canvas, text="0 ms", font=("Arial", 24))
    latency_label.place(relx=0.5, rely=0.5, anchor="center")

    # Call the update_latency_display function to start updating the display
    update_latency_display(latency_label, root)

    root.mainloop()




def plot_baud_rate(baud_rate):
        time = [i for i in range(10)]  # Example time intervals
        symbols = [baud_rate for _ in range(10)]  # Number of symbols transmitted at each time interval
        
        plt.plot(time, symbols, marker='o')
        plt.xlabel('Time')
        plt.ylabel('Symbols (Baud rate)')
        plt.title('BaudRate')
        plt.grid(True)
        plt.show()



def packet_loss(self,packets_sent,packets_received):
    packet = ((packets_sent - packets_received) / packets_sent) * 100
    print(packet)
    return packet


def update_loses_display(loses_label, root):
    loses = packet_loss()
    loses_label.config(text=f"{loses} ms")
    root.after(1000, update_loses_display, loses_label, root)  # Update every second


def popup_losses(self):
    root = tk.Tk()
    root.title("losses")

    # Create a canvas to draw the circular design
    canvas = tk.Canvas(root, width=200, height=200, bg="black", highlightthickness=0)
    canvas.pack(pady=20)

    # Draw a circle
    canvas.create_oval(10, 10, 190, 190, outline="white", width=5)

    # Create a label to display the latency inside the circle
    loses_label = tk.Label(canvas, text="0 ms", font=("Arial", 24))
    loses_label.place(relx=0.5, rely=0.5, anchor="center")

    # Call the update_latency_display function to start updating the display
    update_latency_display(loses_label, root)

    root.mainloop()







def measure_packet_loss(destination):
    try:
        result = subprocess.run(['ping', '-c', '10', destination], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        packet_loss = None
        for line in lines:
            if "packet loss" in line:
                packet_loss_str = line.split(',')[2].strip()
                packet_loss = float(packet_loss_str.split()[0])
                break
        if packet_loss is None:
            return None
        else:
            return packet_loss
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_packet_loss_curve(destination):
    packet_losses = []
    for i in range(1, 11):  # Perform 10 measurements
        packet_loss = measure_packet_loss(destination)
        if packet_loss is not None:
            packet_losses.append(packet_loss)
    plot_packet_loss_curve(packet_losses)

def plot_packet_loss_curve(packet_losses):
    x_values = range(1, len(packet_losses) + 1)
    plt.plot(x_values, packet_losses, marker='o', linestyle='-')
    plt.xlabel('Measurement Index')
    plt.ylabel('Packet Loss (%)')
    plt.title('Packet Loss Curve')
    plt.grid(True)
    plt.show()
