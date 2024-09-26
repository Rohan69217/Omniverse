import socket

local_ip = "0.0.0.0"  
local_port = 8881

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((local_ip, local_port))

print("Listening for UDP packets on port", local_port)

while True:

    data, addr = udp_socket.recvfrom(1024)
    
    data_str = data.decode()
    data_list = data_str.split(",")

    accel_x = float(data_list[-3]) 
    accel_y = float(data_list[-2])
    accel_z = float(data_list[-1])

    print(f"Received accelerometer data from {addr}: X={accel_x}, Y={accel_y}, Z={accel_z}")
