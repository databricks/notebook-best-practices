# Databricks notebook source
# MAGIC %md
# MAGIC Test runner for `pytest`

# COMMAND ----------

%pip install -r ../requirements.txt

# COMMAND ----------

# MAGIC %md
# MAGIC pytest.main runs our tests directly in the notebook environment, providing fidelity for Spark and other configuration variables.
# MAGIC 
# MAGIC A limitation of this approach is that changes to the test will be cached by Python's import caching mechanism.
# MAGIC 
# MAGIC To iterate on tests during development, we restart the Python process and thus clear the import cache to pick up changes.

# COMMAND ----------

dbutils.library.restartPython()
print("Python interpreter will be restarted.")

# COMMAND ----------

import pytest
import os
import sys

# Run all tests in the repository root.
# notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
# repo_root = os.path.dirname(os.path.dirname(notebook_path))
#os.chdir('..')
#%pwd

# Skip writing pyc files on a readonly filesystem.
sys.dont_write_bytecode = True

retcode = pytest.main(["../tests", "-p", "no:cacheprovider"])

# Fail the cell execution if we have any test failures.
#assert retcode == 0, 'The pytest invocation failed. See the log above for details.'

# COMMAND ----------

import json
json.loads(dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson())

# COMMAND ----------

