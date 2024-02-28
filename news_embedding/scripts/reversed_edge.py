import json
from pymongo import MongoClient, UpdateOne

with open("mongo_dump.json", "rb") as fi:
    # Connect to mongo instance and set indices if yet to be set
    client = MongoClient("localhost", 27017)
    db = client.fyp
    wikidata_reversed_collection = db.wikidata_reversed_collection
    # Create unique index on 'q' (entity ID)
    wikidata_reversed_collection.create_index("q", unique=True)

    number_of_lines_at_a_time = 120  # TODO: Tweak
    num_lines = 0
    node_to_parents: dict[int, set[int]] = {}

    for line in fi:
        try:
            j = json.loads(line)
            entityid = int(j["q"])
            neighbors = map(lambda x: int(x), j["n"])

            for neighbor in neighbors:
                # Check whether an update already exists in current chunk
                if node_to_parents.get(neighbor) == None:
                    # Get the latest adjlist info for neighbor node
                    result = wikidata_reversed_collection.find_one(
                        {"q": neighbor}, {"n": True}
                    )
                    if result == None:
                        node_to_parents[neighbor] = set()
                    else:
                        node_to_parents[neighbor] = set(result["n"])

                node_to_parents[neighbor].add(entityid)
        except Exception as e:
            print(f"Error occurred: {e}\nskipped: {line}")

        num_lines += 1
        if num_lines == number_of_lines_at_a_time:
            bulk_upsert = []
            for nodeid, parents in node_to_parents.items():
                node = {"q": nodeid, "n": list(parents)}

                bulk_upsert.append(
                    UpdateOne({"q": nodeid}, {"$set": node}, upsert=True)
                )

            try:
                wikidata_reversed_collection.bulk_write(bulk_upsert, ordered=False)
            except:
                print(f"Error in bulk upsert:")
                print(bulk_upsert)

            # Reset
            num_lines = 0
            node_to_parents = {}

    print("done")
