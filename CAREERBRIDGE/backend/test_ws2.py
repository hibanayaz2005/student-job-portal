import asyncio, websockets

async def test():
    try:
        # Connecting with cookie using additional_headers for modern websockets package
        async with websockets.connect(
            'ws://localhost:8000/ws/chat/', 
            additional_headers={"Cookie": "sessionid=123"}
        ) as ws:
            print('Connected to localhost with cookie')
            await ws.send('{"event_type": "message", "message": "Hello", "sender_id": "test_user"}')
            print('Sent')
            try:
                res = await asyncio.wait_for(ws.recv(), timeout=2)
                print('Received:', res)
            except asyncio.TimeoutError:
                print('Timeout waiting for receive')
    except Exception as e:
        print('Localhost error with cookie:', e)

if __name__ == "__main__":
    asyncio.run(test())
