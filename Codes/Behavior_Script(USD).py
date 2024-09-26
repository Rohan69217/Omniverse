#Runs in Omniverse
from omni.kit.scripting import BehaviorScript
import socket
from pxr import Gf
import carb


class AccelDataBs(BehaviorScript):
    #__init__ function
    def on_init(self):
        carb.log_info(f"{type(self).__name__}.on_init()->{self.prim_path}")

        local_ip = "0.0.0.0"
        local_port = 8765
        #local port is the same as the one mentioned in the code to send the data
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((local_ip, local_port))
        self.udp_socket.setblocking(False)
        print("Listening for Data from : ", local_port)

    #destroy function to clean up resources and reset
    def on_destroy(self):
        carb.log_info(f"{type(self).__name__}.on_destroy()->{self.prim_path}")
        if self.udp_socket:
            self.udp_socket.close()
            self.udp_socket = None

        cube_prim = self.stage.GetPrimAtPath("/World/Cube")
        if cube_prim:
            cube_prim.GetAttribute('xformOp:rotateXYZ').Set(Gf.Vec3f(0, 0, 0))

    #executed when play button is pressed
    def on_play(self): 
        print(f"{__class__.__name__}.on_play()->{self.prim_path}")
        local_ip = "0.0.0.0"
        local_port = 8765
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((local_ip, local_port))
        self.udp_socket.setblocking(False)
        self.dt = 0.1

    #executed when ause button is pressed
    def on_pause(self):
        print(f"{__class__.__name__}.on_pause()->{self.prim_path}")

    #calls destroy fn
    def on_stop(self):
        print(f"{__class__.__name__}.on_stop()->{self.prim_path}")
        self.on_destroy()

    def on_update(self, current_time: float, delta_time: float):
        carb.log_info(f"{type(self).__name__}.on_update({current_time}, {delta_time})->{self.prim_path}")
        self.get_data()

    #get accel data and set rotation of cube
    def get_data(self):
        try:
            accel_data, addr = self.udp_socket.recvfrom(1024)

            data = accel_data.decode()
            data_list = data.split(",")

            accel_x = float(data_list[0])
            accel_y = float(data_list[1])
            accel_z = float(data_list[2])

            cube_prim = self.stage.GetPrimAtPath('/World/Cube')
            xform = cube_prim.GetAttribute('xformOp:rotateXYZ')
            xform.Set(Gf.Vec3f(accel_x, accel_y, accel_z))

        except (ValueError, AttributeError) as e:
            carb.log_warn(f"Failed to process UDP data: {data}. Error: {str(e)}")
        except socket.error as e:
            carb.log_warn(f"Socket error: {str(e)}")
