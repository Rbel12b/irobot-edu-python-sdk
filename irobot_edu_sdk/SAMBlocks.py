from .backend.SAMBlocks_backend import Backend, SAM_BLOCK_TYPE

class SAMBlock:
    def __init__(self, backend: Backend):
        self.backend = backend

    async def connect(self):
        await self.backend.connect()
        await self.write_status_led(150, 150, 150)

    async def disconnect(self):
        await self.write_status_led(255, 100, 100)
        await self.backend.disconnect()

    async def write_status_led(self, red: int, green: int, blue: int):
        if red < 0 or red > 255 or green < 0 or green > 255 or blue < 0 or blue > 255:
            raise ValueError("RGB values must be between 0 and 255")
        msg = bytes([red, green, blue])
        await self.backend.write_status(msg)

    async def write_rgb_led(self, red: int, green: int, blue: int):
        if red < 0 or red > 255 or green < 0 or green > 255 or blue < 0 or blue > 255:
            raise ValueError("RGB values must be between 0 and 255")
        msg = bytes([red, green, blue])
        await self.backend.write_actor(msg)

    async def write_motor(self, speed: int):
        if speed < -100 or speed > 100:
            raise ValueError("Speed must be between -100 and 100")
        # Convert speed
        if speed < 0:
            if speed < -100:
                speed = -100
            speed = (abs(speed) * 1.27) + 128
        else:
            if speed > 100:
                speed = 100
            speed = speed * 1.27

        msg = bytes([int(speed), 0, 0])
        await self.backend.write_actor(msg)

    async def write_servo(self, angle: int):
        if angle < 0 or angle > 180:
            raise ValueError("Angle must be between 0 and 180")
        msg = bytes([angle, 0, 0])
        await self.backend.write_actor(msg)

    def get_sensor_value(self) -> int:
        return self.backend.get_sensor()
    
    def get_battery_level(self) -> int:
        return self.backend.get_battery()
    
    def on_button_press(self, handler):
        """Register a handler for button press events.
        The handler will block other events until it returns.
        Handlers are executed in the order they are registered."""
        self.backend.on_button_press(handler)

    def on_button_release(self, handler):
        """Register a handler for button release events.
        The handler will block other events until it returns.
        Handlers are executed in the order they are registered."""
        self.backend.on_button_release(handler)

    def get_block_name(self) -> str:
        """Get the name of the block."""
        return self.backend.get_block_name()
    
    def get_block_type(self) -> SAM_BLOCK_TYPE:
        """Get the type of the block."""
        return self.backend.get_block_type()

    def wait_for_button_press(self):
        """Wait for a button press event."""
        if self.get_block_type() != SAM_BLOCK_TYPE.BUTTON:
            raise ValueError("This method is only available for button blocks.")
        return self.backend.button_pressed_event.wait()
    
    def wait_for_button_release(self):
        """Wait for a button release event."""
        if self.get_block_type() != SAM_BLOCK_TYPE.BUTTON:
            raise ValueError("This method is only available for button blocks.")
        return self.backend.button_release_event.wait()