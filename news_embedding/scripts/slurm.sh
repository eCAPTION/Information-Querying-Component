#!/bin/sh
#SBATCH --partition=long
#SBATCH --job-name=ecaption
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=
#SBATCH --time=3-0

#### Start MongoDB instance on compute node
#### NOTE: Rmb to kill any running MongoDB instance on the login node first
../mongo/mongodb-linux-x86_64-ubuntu2204-7.0.2/bin/mongod --dbpath ../mongo/data --logpath ../mongo/logs/mongod.log --fork

#### Uncomment the relevant line to run
srun python unzip.py # Run unzip.py
# srun python reversed_edge.py # Run reversed_edge.py
# srun ../mongo/mongodb-database-tools-ubuntu2204-x86_64-100.9.0/bin/mongoexport --collection=wikidata_collection --db=fyp --out mongo_dump.json # Create a JSON export of the specified db and collection
# srun ../mongo/mongodb-database-tools-ubuntu2204-x86_64-100.9.0/bin/mongodump --collection=wikidata_collection --db=fyp --out mongo_dump # Create a MongoDB dump of the specified db and collection. Useful for transferring the db to your local machine

#### Kill the running MongoDB instance on compute node
../mongo/mongodb-linux-x86_64-ubuntu2204-7.0.2/bin/mongod --dbpath ../mongo/data --logpath ../mongo/logs/mongod.log --shutdown
