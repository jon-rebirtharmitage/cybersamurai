import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(
    'mongodb+srv://ceadministrator:B3urH8ffZakl96ew@nemesis.aswz80g.mongodb.net/?retryWrites=true&w=majority&appName=nemesis')

db = client.resources

collection = db.ouiLookup

async def do_insert(k, v):
    document = {k: v}
    result = await db.ouiLookup.insert_one(document)

file = open('oui.txt', 'r', encoding="utf8")
lines = file.read().splitlines()
for index, line in enumerate(lines):
    a = line.split("\t")
    if len(a[0]) <= 8:
        k = a[0]
        v = a[1]
        loop = client.get_io_loop()
        loop.run_until_complete(do_insert(k, v))

