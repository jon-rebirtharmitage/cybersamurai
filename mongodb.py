import motor.motor_asyncio
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://ceadministrator:B3urH8ffZakl96ew@nemesis.aswz80g.mongodb.net/?retryWrites=true&w=majority&appName=nemesis')

db = client.test_database

collection = db.test_collection
async def do_insert():
    document = {"key": "value"}
    result = await db.test_collection.insert_one(document)
    print("result %s" % repr(result.inserted_id))

loop = client.get_io_loop()
loop.run_until_complete(do_insert())
