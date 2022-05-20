# Databricks notebook source
# MAGIC %md Test runner for `pytest`

# COMMAND ----------

# MAGIC %pwd
# MAGIC %ls ../
# MAGIC %pip install -r ../requirements.txt

# COMMAND ----------

import pytest
import os

# Run all tests in the repository root.
notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
repo_root = os.path.dirname(os.path.dirname(notebook_path))
os.chdir(f'/Workspace/{repo_root}')
%pwd

# pytest.main runs our tests directly in the notebook environment, providing
# fidelity for Spark and other configuration variables.
#
# A limitation of this approach is that changes to the test will be
# cache by Python's import caching mechanism.
#
# To iterate on tests during development, use 'Detach & Re-attach'
# between invocations in order to restart the Python process and
# thus clear the import cache to pick up changes.
retcode = pytest.main(["."])

# Fail the cell execution if we have any test failures.
assert retcode == 0, 'The pytest invocation failed. See the log above for details.'
