# import asyncio
# import websockets
# import cv2
# import numpy as np
# from test import Process

# async def handle_client(websocket, path):
#     print("Someone connected")
#     process=Process()
#     try:
#         while True:
#             data = await websocket.recv()
#             nparr = np.frombuffer(data, np.uint8)
#             img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#             response=process.ProcessImage(img_np)
#             if response=="1":
#               print("=============================Cheater=============================")
#               await websocket.send(response)
#     except websockets.exceptions.ConnectionClosed:
#         print("Someone disconnected")


# if __name__ == "__main__":
#     start_server = websockets.serve(handle_client, 'localhost', 8756)

#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()

from multiprocessing import process
from urllib import response
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import numpy as np
import cv2
from test import Process

app=FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections:list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.process=Process()
        self.active_connections.append(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    def disconnect(self, websocket: WebSocket):
        self.process=None
        self.active_connections.remove(websocket)

manager=ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data=await websocket.receive_bytes()
            nparr=np.frombuffer(data, np.uint8)
            img_np=cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            response=manager.process.ProcessImage(img_np)
            if response=="1":
                print("=============================Cheater=============================")
                await manager.send_personal_message(f"{response}", websocket)

    except WebSocketDisconnect: 
        manager.disconnect(websocket)
    # await websocket.accept()
    # process=Process()
    # while True:
    #     data = await websocket.receive_bytes()
    #     nparr = np.frombuffer(data, np.uint8)
    #     img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    #     response=process.ProcessImage(img_np)
    #     if response=="1":
    #         print("=============================Cheater=============================")
    #         await websocket.send(response)