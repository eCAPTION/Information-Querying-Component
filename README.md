# Information Querying Component
The Information Querying Component is a knowledge graph augmented news article similarity search system which takes in a news article URL and returns articles of diversified viewpoints alongside facts and information related to the topic or event. This information is then passed to the Infographic Generation component to be placed in an infographic format before being returned to the user via the chatbot interface.

### Local Development
- Ensure Kafka and Zookeeper are installed and running (e.g. `brew install kafka` on MacOS).
- The setup instructions for each service can be found in the `README.md` located in the respective directories.
- Ensure the `.env` file is set up and configured in the root directory (e.g. in the root directory, run `cp .env.example .env` and update the relevant variables).

### Dockerized Setup
- To run the Dockerized setup, ensure Docker is installed on the machine
- Run the following command in the root directory to start/ stop the full dockerized setup:
  ```bash
  make start-docker
  make stop-docker
  ```
- The gateway REST API is exposed to the local machine on port 8000 (e.g. http://localhost:8000).
- Kafka and Zookeeper are exposed on ports 29092 and 22181 respectively (to connect to GUI tools like Kafka Offset Explorer 2 for local development)
