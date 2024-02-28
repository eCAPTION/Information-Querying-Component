import bz2
import json
from pymongo import MongoClient, TEXT, UpdateOne


# Helpers
def is_entity(label: str):
    return label[0] == "Q"


with open("../latest-all.json.bz2", "rb") as fi:
    decomp = bz2.BZ2Decompressor()
    prev_chunk_leftover = b""

    # Connect to mongo instance and set indices if yet to be set
    client = MongoClient("localhost", 27017)
    db = client.fyp
    wikidata_collection = db.wikidata_collection
    # Create unique index on 'q' (entity ID)
    wikidata_collection.create_index("q", unique=True)
    # Create text index on 'l' (label) with simple tokenisation without stemming or stopwords by setting language to "none"
    wikidata_collection.create_index([("l", TEXT)], default_language="none")

    for data in iter(lambda: fi.read(1024 * 1024 * 32), b""):
        raw = prev_chunk_leftover + decomp.decompress(data)
        current_chunk = raw.split(b"\n")
        if raw[-1] != b"\n":
            prev_chunk_leftover = current_chunk.pop()

        bulk_upsert = []

        for line in current_chunk:
            s = line.decode("utf-8")
            try:
                j = json.loads(s[:-1])
                id = j["id"]
                if not is_entity(id):
                    print(f"not entity: {id}")
                    continue
                id = int(id[1:])
                label = j["labels"].get("en", {}).get("value")
                description = j["descriptions"].get("en", {}).get("value")
                neighbors = [
                    int(statement["mainsnak"]["datavalue"]["value"]["numeric-id"])
                    for p_id, statements in j["claims"].items()
                    for statement in statements
                    if statement["mainsnak"]["datatype"] == "wikibase-item"
                    and statement["mainsnak"]["snaktype"] == "value"
                ]

                node = {"q": id, "l": label, "n": neighbors}

                bulk_upsert.append(UpdateOne({"q": id}, {"$set": node}, upsert=True))

            except Exception as e:
                print(f"Error occurred: {e}\nskipped: {s}")

        wikidata_collection.bulk_write(bulk_upsert, ordered=False)

    print("done")
