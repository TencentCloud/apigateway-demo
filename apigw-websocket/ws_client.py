#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8865"
    #uri = "ws://service-463f276w-1251890925.gz.apigw.tencentcs.com/websocket/"
    async with websockets.connect(uri) as websocket:
        text="hello world"
        print("client: %s"%text)
        await websocket.send(text)
        recv_text = await websocket.recv()
        print(f"server: {recv_text}")
        await websocket.close()

asyncio.get_event_loop().run_until_complete(hello())
