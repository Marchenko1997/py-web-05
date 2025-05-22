
import asyncio
import websockets


async def main():
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        while True:
            msg = input("Enter a command (e.g. exchange 2 USD EUR): ")
            await websocket.send(msg)
            response = await websocket.recv()
            print(f"\nServer response:\n{response}\n")


if __name__ == "__main__":
    asyncio.run(main())
