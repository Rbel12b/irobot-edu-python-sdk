from irobot_edu_sdk.backend.SAMBlocks_bluetooth import Bluetooth
from irobot_edu_sdk.SAMBlocks import SAMBlock
import asyncio

DCMotor = SAMBlock(Bluetooth())

async def run():
    await DCMotor.connect()
    print("Connected to SAM Block")

    # Set motor speed to 50%
    await DCMotor.write_motor(50)
    print("Motor set to 50% speed")

    # Wait for a while to observe the motor running
    await asyncio.sleep(5)

    # Stop the motor
    await DCMotor.write_motor(0)
    print("Motor stopped")

    # Disconnect from the SAM Block
    await DCMotor.disconnect()


if __name__ == "__main__":
    asyncio.run(run())
    print("DC Motor example completed")
