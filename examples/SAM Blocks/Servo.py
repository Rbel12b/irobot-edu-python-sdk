from irobot_edu_sdk.backend.SAMBlocks_bluetooth import Bluetooth
from irobot_edu_sdk.SAMBlocks import SAMBlock
import asyncio

Servo = SAMBlock(Bluetooth())

async def run():
    await Servo.connect()
    print("Connected to SAM Block")

    # Set servo angle to 90 degrees
    await Servo.write_servo(90)
    print("Servo set to 90 degrees")
    
    # Wait for a while to observe the servo position
    await asyncio.sleep(2)

    # Set servo angle to 0 degrees
    await Servo.write_servo(0)
    print("Servo set to 0 degrees")

    # Disconnect from the SAM Block
    await Servo.disconnect()


if __name__ == "__main__":
    asyncio.run(run())
    print("Servo example completed")
