import asyncio
import websockets

uri = "ws://localhost:8765"


async def spammer():
    nickname = 'sexy_chik_18'
    async with websockets.connect(uri) as websocket:
        await websocket.send(nickname)
        await websocket.send('?')

        wait_peoples = True
        while wait_peoples:
            peoples = await websocket.recv()
            peoples = peoples.split(', ')
            if nickname in peoples:
                wait_peoples = False

        peoples.remove(nickname)
        while True:
            for name in peoples:
                for _ in range(10):
                    await websocket.send(f'{name}: Привет! давай познакомимся! Заходи на сайт ххх.сом')
            await asyncio.sleep(1)


loop = asyncio.get_event_loop()
loop.run_until_complete(spammer())
