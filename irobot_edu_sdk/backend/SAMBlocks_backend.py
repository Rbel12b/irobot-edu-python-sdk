class Backend:
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
