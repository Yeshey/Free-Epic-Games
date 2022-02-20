# https://websockets.readthedocs.io/en/stable/

'''
import asyncio

async def do_io():
    print('io start')
    await asyncio.sleep(5)
    print('io end')

async def do_other_things():
    print('doing other things')

loop = asyncio.new_event_loop()

loop.run_until_complete(do_io())
loop.run_until_complete(do_other_things())

loop.close()

'''

import asyncio
import websockets

async def server(ws:str, path:int):
    print('Client joined.')
    #await ws.send(inp)
    while True:
        message = await ws.recv()
        print(f'Msg [{message}]')
        break
    print("I'm out")

async def main():
    start_server = await websockets.serve(server, 'localhost', 5678)
    await start_server.wait_closed()

asyncio.run(main())

'''
# https://www.reddit.com/r/learnpython/comments/n9t9wn/python_websocket_server_with_a_javascript_client/
import asyncio
import websockets

async def server(ws:str, path:int):
    print('Client joined.')
    #await ws.send(inp)
    while True:
        message = await ws.recv()
        print(f'Msg [{message}]')
        break
    print("I'm out")
    #asyncio.get_event_loop().stop()

        
server = await websockets.serve(lambda websocket, path: ws.msgHandler(websocket, path), "localhost", 5678)
await server.wait_closed()

Server = websockets.serve(server, '127.0.0.1', 5678)
loop = asyncio.get_event_loop()

asyncio.run(Server)
loop.run_forever() 
'''

'''
async def server(ws:str, path:int):
    print('Client joined.')
    #await ws.send(inp)
    while True:
        message = await ws.recv()
        print(f'Msg [{message}]')
        break
    print("I'm out")
        
Server = websockets.serve(server, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(Server)
asyncio.get_event_loop().run_forever() 
'''