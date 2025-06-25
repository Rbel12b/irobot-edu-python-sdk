import inspect
from enum import Enum, auto
import asyncio

class SAM_BLOCK_TYPE(Enum):
    DC_MOTOR = 0
    SERVO = auto()
    RGB_LED = auto()
    TILT_SENSOR = auto()
    BUTTON = auto()
    PRESSURE_SENSOR = auto()
    LIGHT_SENSOR = auto()
    TEMPERATURE_SENSOR = auto()
    POTENTIOMETER = auto()
    PROXIMITY_SENSOR = auto()

class Backend:

    _on_button_press_handlers = []
    _on_button_release_handlers = []
    button_pressed_event = asyncio.Event()
    button_release_event = asyncio.Event()

    async def _emit(self, handlers):
        for h in handlers:
            if inspect.iscoroutinefunction(h):
                await h()
            else:
                h()

    async def connect(self):
        """Connect to robot"""
        raise NotImplementedError()

    async def is_connected(self) -> bool:
        """Returns True if robot is connected"""
        raise NotImplementedError()

    async def disconnect(self):
        """Disconnect from robot"""
        raise NotImplementedError()

    async def write_status(self, msg: bytes):
        """Write to the status led characteristic (3 bytes)"""
        raise NotImplementedError()
    
    async def write_actor(self, msg: bytes):
        """Write to the actor characteristic (3 bytes)"""
        raise NotImplementedError()

    def get_sensor(self) -> int:
        """Read sensor value from block"""
        raise NotImplementedError()
    
    def get_battery(self) -> int:
        """Read battery level (percentage) from block"""
        raise NotImplementedError()
    
    def on_button_press(self, handler):
        """Register a handler for button press events.
         The hadler will block other events until it returns.
         Hadlers are executed in the order they are registered."""
        self._on_button_press_handlers.append(handler)

    def on_button_release(self, handler):
        """Register a handler for button release events.
         The hadler will block other events until it returns.
         Hadlers are executed in the order they are registered."""
        self._on_button_release_handlers.append(handler)

    def get_block_name(self) -> str:
        """Get the name of the block"""
        return NotImplementedError()
    
    def get_block_type(self) -> SAM_BLOCK_TYPE:
        name_to_type = {
            "SAM DC Motor": SAM_BLOCK_TYPE.DC_MOTOR,
            "SAM Servo Motor": SAM_BLOCK_TYPE.SERVO,
            "SAM RGB LED": SAM_BLOCK_TYPE.RGB_LED,
            "SAM Tilt": SAM_BLOCK_TYPE.TILT_SENSOR,
            "SAM Button": SAM_BLOCK_TYPE.BUTTON,
            "SAM Pressure": SAM_BLOCK_TYPE.PRESSURE_SENSOR,
            "SAM LDR": SAM_BLOCK_TYPE.LIGHT_SENSOR,
            "SAM Temperature": SAM_BLOCK_TYPE.TEMPERATURE_SENSOR,
            "SAM Potentiometer": SAM_BLOCK_TYPE.POTENTIOMETER,
            "SAM IR Sensor": SAM_BLOCK_TYPE.PROXIMITY_SENSOR,
        }
        name = self.get_block_name()
        if name in name_to_type:
            return name_to_type[name]
