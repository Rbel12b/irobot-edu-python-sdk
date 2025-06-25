from irobot_edu_sdk.backend.SAMBlocks_bluetooth import Bluetooth
from irobot_edu_sdk.SAMBlocks import SAMBlock
import asyncio

Potentiometer = SAMBlock(Bluetooth("SAM Potentiometer"))
Servo = SAMBlock(Bluetooth("SAM Servo Motor"))
Button = SAMBlock(Bluetooth("SAM Button"))

async def run():
    await Servo.connect()
    await Potentiometer.connect()
    await Button.connect()
    print("Connected to SAM Blocks")

    while True:
        # Read the potentiometer value
        pot_value = Potentiometer.get_sensor_value()
        print(f"Potentiometer value: {pot_value}")

        # Map the potentiometer value to a servo angle (0-180 degrees)
        servo_angle = int((pot_value / 255) * 180)
        print(f"Setting servo angle to: {servo_angle} degrees")

        # Write the servo angle
        await Servo.write_servo(servo_angle)

        # Check if the button is pressed
        if Button.get_sensor_value() != 0:
            break

        # Wait for a short period before reading again
        await asyncio.sleep(0.1)

    # Disconnect from the SAM Block
    await Servo.disconnect()


if __name__ == "__main__":
    asyncio.run(run())
    print("Servo example completed")
