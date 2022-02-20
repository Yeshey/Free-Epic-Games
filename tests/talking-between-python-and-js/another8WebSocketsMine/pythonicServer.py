# https://websockets.readthedocs.io/en/stable/
import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        print(message)

async def main():
    async with websockets.serve(echo, "localhost", 5678):
        await asyncio.Future()  # run forever

asyncio.run(main())


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