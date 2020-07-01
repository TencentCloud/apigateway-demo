#!/usr/bin/env python

import asyncio
import websockets
import time 
async def echo(websocket, path):
    print("get a client ,connetctionId: ")
    print(websocket.request_headers.get('Sec-WebSocket-Key'))

    async for message in websocket:
        await websocket.send(message)
        await websocket.send("hello client")
        #time.sleep(3)
        #await websocket.send("hello client")

start_server = websockets.serve(echo, "0.0.0.0", 8865)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
