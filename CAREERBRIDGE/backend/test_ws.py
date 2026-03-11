import asyncio, websockets
import json

async def test():
    try:
        # no cookies
        async with websockets.connect('ws://127.0.0.1:8000/ws/chat/') as ws:
            print('Connected without cookies!')
    except Exception as e:
        print('Error 1:', e)
    
    # Try sending bogus cookie
    try:
        async with websockets.connect('ws://127.0.0.1:8000/ws/chat/', extra_headers={'Cookie': 'sessionid=123'}) as ws:
            print('Connected with cookies!')
    except Exception as e:
        print('Error 2:', e)

asyncio.run(test())
