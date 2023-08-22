# import uvicorn
# import config


# if __name__ == "__main__":
#     uvicorn.run('config:app', host='127.0.0.1', port=8000)

import asyncio, os
from os import environ
from dotenv import load_dotenv

from uvicorn import Server, Config

load_dotenv()


class MyServer(Server):
    async def run(self, sockets=None):
        self.config.setup_event_loop()
        return await self.serve(sockets=sockets)


async def run():
    apps = []
    config1 = Config("config:app", host="127.0.0.1", port="8000")
    server1 = MyServer(config=config1)
    apps.append(server1.run())

    config2 = Config("graph.schema:app", host="127.0.0.1", port="7000")
    server2 = MyServer(config=config2)
    apps.append(server2.run())

    return await asyncio.gather(*apps)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
