import asyncio
import time
import websockets

async def main():
    async with websockets.connect('ws://127.0.0.1:5678') as websocket:
        while 1:
            try:
                #a = readValues() #read values from a function
                #insertdata(a) #function to write values to mysql
                await websocket.send("updated")
                print('data updated')
                time.sleep(20) #wait and then do it again
            except Exception as e:
                print(e)

asyncio.get_event_loop().run_until_complete(main())