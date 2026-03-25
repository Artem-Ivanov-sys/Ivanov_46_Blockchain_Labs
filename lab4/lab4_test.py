from aiohttp import ClientSession
from asyncio import run
from pprint import pprint
from json import dumps
from typing import Any

class Logger:
    @staticmethod
    def get(url: str):
        print(f"[{'GET': ^10}] {url}")
    
    @staticmethod
    def response(data: Any):
        print(f"[{'RESPONSE': ^10}] ")
        pprint(data)
        print()
    
    @staticmethod
    def post(url: str, payload_data: Any = None):
        print(f"[{'POST': ^10}] {url}", end="")
        print("  ---POST-->  "+payload_data if payload_data else "")
    
    @staticmethod
    def error(message: str):
        print(f"[{'ERROR': ^10}] {message}")

class Test:
    def __init__(self, session):
        self.session = session
        self.methods = {
            "get": self.session.get,
            "post": self.session.post,
        }

    async def testUrl(self,requestType, url, payloadData = None):
        if not self.checkRequestType(requestType):
            Logger.error("Wrong request type.")
            return
        
        Logger.get(url) if requestType == "get" else Logger.post(url, payloadData)
        async with self.methods[requestType](url, json=payloadData) as response:
            Test.check_status(response.status)
            retrieved_data = await response.json()
            Logger.response(retrieved_data)
    
    def checkRequestType(self, requestType):
        if requestType not in self.methods.keys():
            return False
        return True
    
    @staticmethod
    def check_status(status_code: int):
        if status_code//100 in [4, 5]:
            raise Exception(f"[{'ERROR': ^10}] {status_code}")


async def main():
    async with ClientSession() as session:
        test = Test(session)
        await test.testUrl("post", "http://127.0.0.1:5000/nodes/register", dumps({"nodes": ["http://127.0.0.1:5001"]}))
        await test.testUrl("get", "http://127.0.0.1:5001/mine")
        # await test.testUrl("get", "http://127.0.0.1:5000/mine")
        await test.testUrl("get", "http://127.0.0.1:5000/nodes/resolve")


if __name__ == "__main__":
    run(main())