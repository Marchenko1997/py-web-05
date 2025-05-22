import aiohttp
from datetime import datetime, timedelta


class PrivatBankAPI:
    BASE_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

    async def fetch_exchange_rate(self, session, date):
        url = self.BASE_URL + date

        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Error fetching for {date}: {e}")
            return None

    async def def_exhcange_rates(self, days:int, currecncies: list):
        results = []

        async with aiohttp.ClientSession() as session:
            for i in range(days):
                date = (datetime.now() - timedelta(days=i)).strftime("%d.%m.%Y")
                data = await self.fetch_exchange_rate(session, date)
                if not data:
                    continue

                day_result = {}

                for rate in data.get("exchangeRate", []):
                    if rate.get("currency") in currecncies:
                        day_result[rate["currency"]] = {
                            "sale": rate.get("saleRate"),
                            "purchase": rate.get("purchaseRate"),
                        }
                
                if day_result:
                    results.append({date: day_result})

        return results
