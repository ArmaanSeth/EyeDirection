import asyncio
import websockets
import cv2
import numpy as np
from test import Process

async def handle_client(websocket, path):
    print("Someone connected")
    process=Process()
    try:
        while True:
            data = await websocket.recv()
            nparr = np.frombuffer(data, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            response=process.ProcessImage(img_np)
            if response=="1":
              print("=============================Cheater=============================")
              await websocket.send(response)
    except websockets.exceptions.ConnectionClosed:
        print("Someone disconnected")


if __name__ == "__main__":
    start_server = websockets.serve(handle_client, 'localhost', 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()