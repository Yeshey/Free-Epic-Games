# https://www.reddit.com/r/learnpython/comments/n9t9wn/python_websocket_server_with_a_javascript_client/
import asyncio
import websockets

async def server(ws:str, path:int):
    inp = input('Client joined. Greet it. \nType ')
    await ws.send(inp)
    while True:
        message = await ws.recv()
        print(f'Msg [{message}]')

        print("hmmm")
        
Server = websockets.serve(server, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(Server)
asyncio.get_event_loop().run_forever() 
