import serial
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

ser = serial.Serial('COM4', 115200)  # Windows
# ser = serial.Serial('/dev/ttyUSB0', 115200)  # Linux/Mac


plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(10, 6))
times = deque(maxlen=100)
values = deque(maxlen=100)
line, = ax.plot([], [], 'b-')
ax.set_title('USB Trust Data ')
ax.set_xlabel('Time (Seconds)')
ax.set_ylabel('Thrust (N)')
ax.grid(True)

def update_graph(frame):
    while ser.in_waiting:
        try:
            data = ser.readline().decode().strip()
            if data:
                json_data = json.loads(data)
                times.append(json_data["time"])
                values.append(json_data["thrust"])
                
                line.set_data(times, values)
                ax.relim()
                ax.autoscale_view()
                
                print(f"Time: {json_data['time']}s, Thrust: {json_data['thrust']:.2f}N")
                
        except json.JSONDecodeError:
            print(f"Invalid data: {data}")
    
    return line,

ani = FuncAnimation(fig, update_graph, interval=50, blit=True)
plt.tight_layout()
plt.show()
ser.close()