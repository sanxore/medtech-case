# Medtech case:

## Python et Data Engineering:

### Project structure:

- `configs` folder:
  - `clean_*.json` files contain cleaning config for each file
  - `transform.json` contain input and output files paths


- `data` folder:
  - all input files
  - `cleaned_*.csv` output of the clean tasks
  - `transformed_*.json` output of the transformer (the graph)


- `task_clean` package:
  - `tasks.py` contain all task functions can be called by the dag:
    - `cleansing` function is a generic task based on a config to clean csv file (can be used out of this scope)
  - `utils.py` contain all functions needed by the cleansing tasks


- `task_trasnsform` package:
  - `tasks.py` contain all task functions can be called by the dag:
    - `trasnform` function is a specific task for this case based on a config to transform data to graph
  - `utils.py` contain all functions needed by the transform tasks


- `dag.py` is the pipeline dag calling cleansing tasks first and than the graph building task


- Improvement: Add unit tests to the `utils.py` functions

### CI:

The CI is configured in `./github/workflows/linter.yml` file based on pre-commit configuration.
- Checks applied by the CI;
  - end-of-file-fixer
  - trailing-whitespace
  - check-case-conflict
  - black (default conf)
  - isort (normalize import order)
![image](https://github.com/sanxore/medtech-case/assets/14028677/218ae941-7594-4b32-8ea6-8ee48e86eb48)


- Improvements:
  - Add unit tests validation


### Data Piepeline :

```commandline
[drugs.csv cleansing]------------->|
                                   |
[pubmed.csv cleansing]------------>|------>[transform cleaned files to a graph]
                                   |
[clinical_trials.csv cleansing]--->|
```

- Tha pipeline is a DAG
- The cleansing tasks use a generic cleansing function and write the result in a csv file
- The transform use cleaned files to generate the nodes and the edges and write them to a json file

#### Cleansing:
- Text:
  - lower, remove punctuation, remove extra spaces, fix_unicode, remove new lines ...

- Dates:
  - standardize dates to `yyyy-MM-dd` format

- Improvements:
  - ATC code validator

#### Transform :
- Graph:
  - nodes: drugs, clinical trails, journals, medpubs

- JSON format:

```json
{
  "nodes": {
    "mtc_code | id_clinical_tr | id_pubmed | journal": {
      "label": "",
      "metadata": {},
      "type": "drug | pubmed | clinical_trial | journal"
    },
    ...
  },
  "edges": [
    {
      "src": "node_id",
      "dst":  "node_id",
      "label":  "published_at",
      "metadata": {"date": "2023-01-01"}
    },
    .....
  ]
}
```

### Scalability:
  - We can replace pandas with Spark or load files to BigQuery and do the processing with BQ.
  - Tha output file will be very big, maybe we should consider a tabular design of the graph
  - The design i did can be migrated to Airflow (tasks, dag ...)


## SQL

- le chiffre d’affaires (le montant total des ventes), jour par jour, du 1er janvier 2019 au 31 décembre 2019. Le résultat
sera trié sur la date à laquelle la commande a été passée.

```sql
WITH sales_by_date AS (
SELECT
  date,
  SUM(prod_price * prod_qty) AS ventes
FROM transactions
WHERE date BETWEEN "2019-01-01" AND "2019-12-31"
GROUP BY date
)
SELECT
  date,
  ventes
FROM sales_by_date
ORDER BY date
```

- déterminer, par client et sur la période allant du
1er janvier 2020 au 31 décembre 2020, les ventes meuble et déco réalisées.

```sql
WITH ventes_meuble_client AS (
SELECT
  client_id,
  SUM(prod_price * prod_qty) AS ventes_meuble
FROM transactions t JOIN product_nomenclature p ON t.prod.id = p.product_id
WHERE date BETWEEN "2020-01-01" AND "2020-12-31"
AND product_type = "MEUBLE"
GROUP BY client_id
),
ventes_deco_client AS (
SELECT
  client_id,
  SUM(prod_price * prod_qty) AS ventes_deco
FROM transactions t JOIN product_nomenclature p ON t.prod.id = p.product_id
WHERE date BETWEEN "2020-01-01" AND "2020-12-31"
AND product_type = "DECO"
GROUP BY client_id
)
SELECT
  client_id,
  ventes_meuble,
  ventes_deco
FROM ventes_meuble_client m OUTER JOIN ventes_deco_client d ON m.client_id = d.client_id
```
For the categories with no sales the value will be NULL
