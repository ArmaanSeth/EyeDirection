import asyncio
import websockets
import cv2
import mediapipe as mp
import numpy as np
import math
import socket
# python websocket server
async def handle_client(websocket, path):
    print("Someone connected")
    while True:
        data = await websocket.recv()
        print(f"Received data: {data}")
        # Process the received data here
        # Send a response back to the client
        response = "Server received your message"
        await websocket.send(response)

start_server = websockets.serve(handle_client, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
