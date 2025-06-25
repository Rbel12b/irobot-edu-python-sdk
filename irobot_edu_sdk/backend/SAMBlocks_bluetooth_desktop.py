"""
This is a Bluetooth Low Energy class that implements the Backend interface methods.

It is compatible with CPython on macOS, Windows, and Linux using the Bleak library.
"""

from asyncio import sleep, Lock
from typing import Optional
from bleak import BleakClient, BleakScanner
from .SAMBlocks_backend import Backend


class Bluetooth(Backend):
    BATTERY_SERVICE = "0000180f-0000-1000-8000-00805f9b34fb"
    BATTERY_LEVEL_CHAR = "00002a19-0000-1000-8000-00805f9b34fb"
    SAM_BLOCKS_SERVICE = "3b989460-975f-11e4-a9fb-0002a5d5c51b"
    SAM_BLOCKS_SENSOR_CHAR = "4c592e60-980c-11e4-959a-0002a5d5c51b"
    SAM_BLOCKS_ACTOR_CHAR = "84fc1520-980c-11e4-8bed-0002a5d5c51b"
    SAM_BLOCKS_STATUSLED_CHAR = "5baab0a0-980c-11e4-b5e9-0002a5d5c51b"

    def __init__(self, name: str = None, address: Optional[str] = None):
        """If no name is provided, connects to the first device found."""
        self._name = name
        self._address = address
        self._device = None
        self._client: Optional[BleakClient] = None
        self._txlock = Lock()
        self._sensor_value = 0
        self._battery_level = 0

    def sensor_read_handler(self, characteristic, data):
        msg = bytes(data)
        
        if len(msg) != 1:
            print(f"Received unexpected data length: {len(msg)} bytes")
            return
        
        self._sensor_value = msg[0]

    def battery_read_handler(self, characteristic, data):
        msg = bytes(data)
        
        if len(msg) != 1:
            print(f"Received unexpected data length: {len(msg)} bytes")
            return
        
        self._battery_level = msg[0]

    async def connect(self):
        """This method does not exit until a robot is found"""

        while not self._address:
            if self._name is not None: # If a name is given, try to connect to that
                device = await BleakScanner.find_device_by_name(self._name)
                if device:
                    self._address = device.address
                    self._device = device
            else: # If no name is given, connect to first device with SAM BLocks service
                discovered = await BleakScanner.discover(return_adv=True)
                for device, adv_data in discovered.values():
                    if "SAM" in (device.name or ""):
                        if self._name is None or self._name == device.name:
                            self._address = device.address
                            self._device = device
                            break
        if self._device:
            print(f'Connecting to {device.name} ({device.address})')
            self._client = BleakClient(self._device)
        else:
            print(f'Connecting to {self._address}')
            self._client = BleakClient(self._address)

        if await self._client.connect():
            await self._client.start_notify(self.BATTERY_LEVEL_CHAR, self.battery_read_handler)
            await self._client.start_notify(self.SAM_BLOCKS_SENSOR_CHAR, self.sensor_read_handler)            


    async def is_connected(self) -> bool:
        return self._client.is_connected if self._client else False

    async def disconnect(self):
        if await self.is_connected():
            await self._client.disconnect()
        self._client = None

    async def write_status(self, msg: bytes):
        if self._client:
            async with self._txlock:
                await self._client.write_gatt_char(self.SAM_BLOCKS_STATUSLED_CHAR, msg, True)
    
    async def write_actor(self, msg: bytes):
        if self._client:
            async with self._txlock:
                await self._client.write_gatt_char(self.SAM_BLOCKS_ACTOR_CHAR, msg, True)

    def get_sensor(self) -> int:
        return self._sensor_value
    
    def get_battery(self) -> int:
        return (self._battery_level / 255) * 100
