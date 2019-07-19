from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
import numpy as np
import sys
import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class PythonExample(BaseAgent):

    def initialize_agent(self):
        print("Hippity Hoppity: STARTING MODEL LOADING")
        path = os.path.dirname(__file__)
        print(sys.path)
        sys.path.insert(0, path)
        from model import Model
        self.model = Model(30, 4)
        self.model.load_from_file("Hippity_Hoppity_Get_Off_My_Property/TheModel.h5")
        self.controller_state = SimpleControllerState()
        print("Hippity Hoppity: FINISHED LOADING MODEL")

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        my_car = packet.game_cars[self.index].physics
        my_data = car_data(my_car)
        opponent_car = packet.game_cars[1-self.index].physics
        opponent_data = car_data(opponent_car)
        ball = packet.game_ball.physics
        ball_data = get_ball_data(ball)
        x = np.array([my_data + opponent_data + ball_data])
        output = self.model.model.predict(x)[0]
        print(output)
        self.controller_state.jump = True if output[0] > 0.5 else False
        self.controller_state.pitch = output[1]
        self.controller_state.yaw = output[2]
        self.controller_state.roll = output[3]
        if packet.game_cars[self.index].has_wheel_contact:
            self.controller_state.jump = True
        self.controller_state.throttle = 1
        return self.controller_state

def car_data(car):
    location = [car.location.x, car.location.y, car.location.z]
    location = [location[0]/4096, location[1]/5120, location[2]/2044]
    rotation = [car.rotation.pitch,car.rotation.yaw, car.rotation.roll]
    velocity = [car.velocity.x, car.velocity.y, car.velocity.z]
    velocity = [velocity[0]/2300, velocity[1]/2300, velocity[2]/2300]
    angular_velocity = [car.angular_velocity.x/5.5, car.angular_velocity.y/5.5, car.angular_velocity.z/5.5]
    return location + rotation + velocity + angular_velocity

def get_ball_data(ball):
    location = [ball.location.x, ball.location.y, ball.location.z]
    location = [location[0]/4096, location[1]/5120, location[2]/2044]
    velocity = [ball.velocity.x/2300, ball.velocity.y/2300, ball.velocity.z/2300]
    return location + velocity
