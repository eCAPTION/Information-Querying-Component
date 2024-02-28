# Scripts
This `README.md` outlines the steps required to setup the [WikiData Knowledge Graph](https://www.wikidata.org/wiki/Wikidata:Introduction) for use in the News Embedding Component of eCAPTION.

### Prerequisites
Assumes that the following scripts are being run on the NUS SoC compute cluster (which uses Slurm).

1. Download the latest WikiData dump [here](https://dumps.wikimedia.org/wikidatawiki/entities/).
    - `latest-all.json.bz2`
    - Takes up to 5.5 hours to download onto the NUS SoC compute cluster (~85gb, as of Sep 2023)
1. Download and install MongoDB from tarball with the instructions [here](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu-tarball/).
   - This is important since we are running MongoDB as part of a Slurm job.

### `slurm.sh`
Entrypoint script to run the rest of the below scripts on the NUS SoC compute cluster (which uses Slurm).
1. Update the paths to the local MongoDB binaries.
2. Uncomment the relevant line you wish to run.
3. Update the `--mail-user` to include email updates from Slurm.
4. Run `sbatch slurm.sh` to run the script.
5. Run `squeue | grep <USERNAME>` to view the ongoing job.

### `unzip.py`
Contains the script for unzipping and preprocessing WikiData dumps (.bz2 format) to a stripped down adjacency list format stored in MongoDB. Briefly, only WikiData entities are stored, each being a MongoDB document along with its corresponding English label and list of neighbouring entity IDs.

For example, a document for an entity would look like:
```
{
    "q": <ENTITY_ID>,
    "l": <ENTITY_LABEL>,
    "n": [<NEIGHBOR_ENTITY_ID>]
}
```

A unique index is created for the entity ID field `q` to facilitate search queries by entity ID. A separate text index was also created on the entity label field `l` to facilitate text searches if needed (depending on graph traversal implementation).
> NOTE: The text index on `l` can be removed in the future if the traversal implementation does not require it, which saves memory usage in the MongoDB instance.

This script unzips the .bz2 dump sequentially in chunks, and takes up to 2 days (for ~104million entities, as of Sep 2023) on the NUS SoC compute cluster due to its sheer size. A possible optimization in the future could be to unzip the .gz dump in parallel instead.
> NOTE: Update the path to the .bz2 file and the details of the MongoDB instance in the script.

### `reversed_edge.py`
To enhance the Lowest Common Ancestor Graph Traversal outlined in the NewsLink paper, a bidirected knowledge graph was used. This script generates the adjacency list for "reversed edges" and stores them in a separate MongoDB collection.

Notably, this MongoDB collection differs from the one above by not having the label `l` field.

To use this script, first create a .json export of the collection created from `unzip.py` (refer to the relevant line in `slurm.sh`).
> NOTE: Update the path to the adjacency list .json export file generated from `unzip.py` and the details of the MongoDB instance in the script.

