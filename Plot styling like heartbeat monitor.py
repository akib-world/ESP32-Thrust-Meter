import serial
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque


# Update this to your Bluetooth/USB port and baud rate
ser = serial.Serial('COM4', 115200)

# Plot styling like heartbeat monitor
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 5))

# Heartbeat-like line: green, bold
line, = ax.plot([], [], color='blue', linewidth=3, alpha=0.8)

# Deques to store sliding window data
max_points = 200
times = deque(maxlen=max_points)
values = deque(maxlen=max_points)

# Set up fixed axis range for ECG-like behavior
ax.set_xlim(0, max_points)
ax.set_ylim(0, 10)  # Adjust according to your expected thrust range
ax.set_title('Real-time Thrust (Heartbeat Style)', fontsize=14)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Thrust (N)')
ax.grid(False)

def update_graph(frame):
    while ser.in_waiting:
        try:
            data = ser.readline().decode().strip()
            if data:
                json_data = json.loads(data)
                times.append(json_data["time"])
                values.append(json_data["thrust"])

                # Display only last N points for sliding effect
                line.set_data(range(len(values)), values)
                
                print(f"Time: {json_data['time']}s, Thrust: {json_data['thrust']:.2f}N")
        except json.JSONDecodeError:
            print(f"Invalid data: {data}")

    return line,

ani = FuncAnimation(fig, update_graph, interval=50, blit=True)
plt.tight_layout()
plt.show()
ser.close()
