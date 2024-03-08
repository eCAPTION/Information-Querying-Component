# NLP Service
The NLP service takes in the text content of a URL supplied by the web scraper component and generates the maximal entity cooccurrence  set as outlined by the NewsLink paper.

Briefly, the text content is split into individual sentences on which named entity recognition is performed to identify entities. The list of entities is then filtered to exclude certain types of entities before the maximal entity cooccurrence set is generated. Refer to the `get_maximal_entity_cooccurrence_set` function for more details.

### Local Development
1. Ensure the `.env` file is set up and configured in the root directory (e.g. in the root directory, run `cp .env.example .env` and update the relevant variables).
2. Navigate to the `nlp` directory (e.g. run `cd nlp`)
3. Install the dependencies (e.g. run `pip3 install -r requirements.txt`, preferably in a virtual environment).
4. Download the spacy `en_core_web_sm` package by running the following command:
   ```bash
   spacy download en_core_web_sm
   ```
5. Run the following command to start the web scraper service in development mode.
    ```bash
    faust -A main worker -l info
    ```

### Extensions
1. The NewsLink paper used the pretrained named entity recognition library from spacy for the NER process. However, initial observations reveal that the model could not perform reliably in identifying entity names in the Singapore context, possibly due to lack or imbalance of such data during training. To counter this, the NER process could be finetuned in the future to perform more reliably on articles in the Singapore context.
2. Furthermore, the original NewsLink paper utilized exact string 'contains' matching to link entities identified during the NER process to the corresponding entity representation in the WikiData knowledge graph. More sophisticated techniques such as named entity linking could be explored to improve the matching of entities within the text to the underlying representation in the knowledge graph. Again, such models would likely need to be finetuned to perform satisfactorily in the Singapore context.
