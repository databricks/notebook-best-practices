# Databricks notebook source
# MAGIC %md Test runner for `pytest`

# COMMAND ----------

# MAGIC %pip install -r ../requirements.txt

# COMMAND ----------

import pytest

%cd ../tests
retcode = pytest.main(["--junitxml=/tmp/test-unit.xml", "-lr", "."])

# Fail the cell execution if we have any test failures.
assert retcode == 0, 'The pytest invocation failed. See the log above for details.'
