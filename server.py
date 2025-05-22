
import asyncio
import logging
import websockets
from exchange.client import PrivatBankAPI
from exchange.logger import log_exchange_command

logging.basicConfig(level=logging.INFO)


class ChatServer:
    clients = set()

    async def register(self, ws):
        self.clients.add(ws)
        logging.info("New user connected")

    async def unregister(self, ws):
        self.clients.remove(ws)
        logging.info("User disconnected")

    async def send_to_all(self, message):
        if self.clients:
            await asyncio.gather(*[client.send(message) for client in self.clients])

    async def handle_command(self, message: str):
        if message.startswith("exchange"):
            try:
                parts = message.split()
                days = int(parts[1]) if len(parts) > 1 else 1
                currencies = parts[2:] if len(parts) > 2 else ["USD", "EUR"]

               
                await log_exchange_command(message)

                api = PrivatBankAPI()
                rates = await api.get_exchange_rates(days, currencies)
                return str(rates)
            except Exception as e:
                return f"Error: {e}"
        return f"You said: {message}"

    async def ws_handler(self, ws):
        await self.register(ws)
        try:
            async for msg in ws:
                response = await self.handle_command(msg)
                await self.send_to_all(response)
        finally:
            await self.unregister(ws)


async def main():
    server = ChatServer()
    async with websockets.serve(server.ws_handler, "localhost", 8080):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
