import asyncio
import websockets
import cv2
import numpy as np
from test import processOutput
counter=5
flag=False
k=0
b=-1
c=-1
f1=0
f2=False
ls=[]
async def handle_client(websocket, path):
    print("Someone connected")
    try:
        while True:
            data = await websocket.recv()
            nparr = np.frombuffer(data, np.uint8)
            img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # cv2.imshow('Received Video', img_np)
            processOutput(img_np);
            if cv2.waitKey(1) & 0xFF == ord('q'):
              break
            # print(f"Received data: {data}")
            # Process the received data here
            # Send a response back to the client
            # response = "Server received your message"
            # await websocket.send(response)
    except websockets.exceptions.ConnectionClosed:
        print("Someone disconnected")

start_server = websockets.serve(handle_client, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
