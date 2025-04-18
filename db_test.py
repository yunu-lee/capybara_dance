import pymongo

ATLAS_URI = os.getenv('ATLAS_URI')

client = pymongo.MongoClient(ATLAS_URI)
collection = client['real_estate']['apt']
df = pd.DataFrame(list(collection.find()))

print(df)
