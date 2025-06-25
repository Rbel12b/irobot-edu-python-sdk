from irobot_edu_sdk.backend.SAMBlocks_bluetooth import Bluetooth
from irobot_edu_sdk.SAMBlocks import SAMBlock
import asyncio

RGB_LED = SAMBlock(Bluetooth())

def hsv_to_rgb(h, s, v):
    """Convert HSV to RGB color space."""
    if s == 0.0:
        return (v, v, v)
    i = int(h * 6.0)  # Assume h is in [0, 1)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)
    i %= 6
    if i == 0:
        return (v, t, p)
    elif i == 1:
        return (q, v, p)
    elif i == 2:
        return (p, v, t)
    elif i == 3:
        return (p, q, v)
    elif i == 4:
        return (t, p, v)
    elif i == 5:
        return (v, p, q)

async def run():
    await RGB_LED.connect()
    print("Connected to SAM Block")

    for i in range(360):
        # Convert degrees to radians for HSV
        h = i / 360.0
        s = 1.0
        v = 1.0
        r, g, b = hsv_to_rgb(h, s, v)
        # Write RGB values to the SAM Block
        await RGB_LED.write_rgb_led(int(r * 255), int(g * 255), int(b * 255))
        await asyncio.sleep(0.01)  # Sleep for a short duration to see the effect

    # Disconnect from the SAM Block
    await RGB_LED.disconnect()


if __name__ == "__main__":
    asyncio.run(run())
    print("RGB LED example completed")
