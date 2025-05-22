import sys
import asyncio
from exchange.client import PrivatBankAPI
from exchange.logger import log_exchange_command

async def main():
    if len(sys.argv) < 2:
        print("Enter the number of days (maximum 10)")
        return
    try:
        days = int(sys.argv[1])
        if not 1 <= days <= 10:
            raise ValueError
    except ValueError:
        print("Enter the number of days (maximum 10)")
        return
    currencies = sys.argv[2:] if len(sys.argv) > 2 else ["USD", "EUR"]
    await log_exchange_command(f"exchange {days} {' '.join(currencies)}")

    api = PrivatBankAPI()

    results = await api.get_exchange_rates(days, currencies)

    from pprint import pprint
    pprint(results)

if __name__ == "__main__":
    asyncio.run(main())
