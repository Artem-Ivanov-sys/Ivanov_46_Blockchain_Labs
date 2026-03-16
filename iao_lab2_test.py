from aiohttp import ClientSession
from asyncio import run
from pprint import pprint
from json import dumps
from typing import Any, Dict

class Logger:
    @staticmethod
    def get(url: str):
        print(f"[{'GET': ^10}] {url}")
    
    @staticmethod
    def response(data: Any):
        print(f"[{'RESPONSE': ^10}] ", end="")
        pprint(data)
        print()
    
    @staticmethod
    def post(url: str, payload_data: Any = None):
        print(f"[{'POST': ^10}] {url}", end="")
        print("  ---POST-->  "+payload_data if payload_data else "")
    
    @staticmethod
    def error(message: str):
        print(f"[{'ERROR': ^10}] {message}")


async def main():
    async with ClientSession() as session:
        Logger.get("/mine")
        async with session.get("http://127.0.0.1:5000/mine") as response:
            check_status(response.status)
            retrieved_data = await response.json()
            Logger.response(retrieved_data)
        
        payload_data = dumps({"sender": "0", "recipient": "1", "amount": 1})
        Logger.post("/transactions/new", payload_data)
        async with session.post("http://127.0.0.1:5000/transactions/new", json=payload_data) as response:
            check_status(response.status)
            retrieved_data = await response.json()
            Logger.response(retrieved_data)
        
        Logger.get("/chain")
        async with session.get("http://127.0.0.1:5000/chain") as response:
            check_status(response.status)
            retrieved_data = await response.json()
            Logger.response(retrieved_data)

def check_status(status_code: int):
    if status_code//100 in [4, 5]:
        raise Exception(f"[{'ERROR': ^10}] {status_code}")


if __name__ == "__main__":
    run(main())