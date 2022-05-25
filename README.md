# Using software engineering best practices in Databricks notebooks

Setup ingredients:

https://docs.github.com/en/developers/overview/managing-deploy-keys#machine-users

https://github.com/join to create the repo user

https://docs.github.com/en/enterprise-server@3.1/organizations/managing-membership-in-your-organization/adding-people-to-your-organization

TODO: Create or link to Aha ideas:

* Support for discovering tests to be run, so that users do not need a repo admin in order to add new tests.
* Support for triggered execution, so that trivial changes unrelated to the notebook and its deps do not require test execution.
* GHA should report something during cluster startup to avoid appearing wedged for several minutes.

Setup instructions:

Corresponding to [Python 3.8.10 in the 10.4 LTS release](https://docs.databricks.com/release-notes/runtime/10.4.html#system-environment).

OSX

```
brew install pyenv pipenv
pyenv install 3.8.10
pyenv shell 3.8.10
cd ~/. && python -m venv notebook-best-practices-env && popd
```

From the repo root
```
source ~/notebook-best-practices-env/bin/activate
pip install -r requirements.txt
```

TODO: Demo of test execution being unable to modify production table.
