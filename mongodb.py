import pprint

import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(
    'mongodb+srv://ceadministrator:B3urH8ffZakl96ew@nemesis.aswz80g.mongodb.net/?retryWrites=true&w=majority&appName=nemesis')

db = client.resources

collection = db.ouiLookup


async def do_find_one():
    document = await db.ouiLookup.find_one({'FC:EC:DA': {'$exists': 1}})
    pprint.pprint(document)


loop = client.get_io_loop()
loop.run_until_complete(do_find_one())
