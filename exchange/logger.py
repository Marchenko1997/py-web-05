from aiofile import AIOFile
from aiopath import AsyncPath
from datetime import datetime

async def log_exchange_command(command_text: str):
    path = AsyncPath("logs/exchange.log")

    await path.parent.mkdir(parents=True, exist_ok=True)
    async with AIOFile(path, "a") as afp:
        await afp.write(f"[{datetime.now()}] command: {command_text}\n")

