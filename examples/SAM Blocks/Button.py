from irobot_edu_sdk.backend.SAMBlocks_bluetooth import Bluetooth
from irobot_edu_sdk.SAMBlocks import SAMBlock
import asyncio

Button = SAMBlock(Bluetooth())

async def run():
    Button.on_button_press(lambda: print("Button pressed"))
    Button.on_button_release(lambda: print("Button released"))

    await Button.connect()
    print("Connected to SAM Block")

    # Set the status LED to blue
    await Button.write_status_led(0, 0, 255)

    # Wait for button events
    print("Waiting 10s for button events...")
    await asyncio.sleep(10)

    # Disconnect from the SAM Block
    await Button.disconnect()


if __name__ == "__main__":
    asyncio.run(run())
    print("Button example completed")
