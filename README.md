# Software engineering best practices for Databricks notebooks

TODO: Fill in.

* Version control
* Modularizing and sharing code
* Unit tests

[Advanced topics](https://github.com/databricks/notebook-best-practices/tree/advanced)


dbx deploy -> upload assets and create job
dbx launch --job covid_analysis_etl -> launch deployed job just as in production (slow)


Starting point is the same notebook `covid_eda_raw.py`.
Goal: Convert into a Python only job following software best practices using an IDE

Step 1:

1. create new git repo
2. Convert notebookt to python job
    2.1 copy raw notebook into `jobs/covid_trends_job_raw.py`
    2.2 convert to plain python
    2.3 create dbx config
      2.3.1 create conf/deployment.py
      2.3.2 run `dbx configure`
    2.4 Run the job `dbx execute --cluster-name "<CLUSTER_NAME>" --job covid_analysis_etl_raw` 
3. Extract code into a library (just like for the notebook case)
    3.1 create folder `covid_analysis`
    3.2 create `covid_analysis/transforms.py` https://github.com/databricks/notebook-best-practices/blob/main/covid_analysis/transforms.py
    3.2 rename job to `jobs/covid_trends_job.py` and use library code
    3.3 update the job description in conf/deployment.py
    3.4 run the job `dbx execute --cluster-name "<CLUSTER_NAME>" --job covid_analysis_etl`
4. Unit Testing
    4.1 create `tests/transforms_test.py` and `tests/test_data.csv` from https://github.com/databricks/notebook-best-practices/tree/main/tests
    4.2 (optional) configure pytest in `pytest.ini` and `.coveragerc`
    4.3 Add pytests to `requirements.txt`
    4.4 Run `pip install requirements.txt` (TODO should use venv)
    4.5 Run unit tests `pytest`
5. Integrate with CI/CD - this will run unit tests and deploy jobs
    5.1 create `unit-requirements.txt`
    5.2 create a new job config to run as integ test
        5.2.1 Split `covid_analysis_etl` into `covid_analysis_etl_integ` and `covid_analysis_etl_prod`. Pass `--prod` as parameter to the prod job
        5.2.2 Adjust cluster configuration for prod as needed
        5.2.3 Add code to the job to only write the table in prod mode
    5.3 create `.github/workflows/*.yml`





