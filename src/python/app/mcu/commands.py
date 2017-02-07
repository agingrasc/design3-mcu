"""" Module contenant les commandes valident que l'IA peut envoyer au robot. """
from abc import abstractmethod, ABCMeta

from mcu import protocol
from mcu.protocol import PencilStatus, Leds


class Command(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def pack_command(self) -> bytes:
        pass


class Move(Command):
    def __init__(self, x, y, theta):
        super().__init__()
        self.x = x
        self.y = y
        self.theta = theta

    def pack_command(self) -> bytes:
        # FIXME: voir comment integrer le regulateur
        return protocol.generate_move_command(self.x, self.y, self.theta)


class Camera(Command):
    def __init__(self, x_theta, y_theta):
        super().__init__()
        self.x_theta = x_theta
        self.y_theta = y_theta

    def pack_command(self) -> bytes:
        return protocol.generate_camera_command(self.x_theta, self.y_theta)


class Pencil(Command):
    def __init__(self, status: PencilStatus):
        super().__init__()
        self.status = status

    def pack_command(self) -> bytes:
        return protocol.generate_pencil_command(self.status)


class Led(Command):
    def __init__(self, led: Leds):
        super().__init__()
        self.led = led

    def pack_command(self) -> bytes:
        return protocol.generate_led_command(self.led)
