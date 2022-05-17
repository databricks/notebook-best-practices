# Using software engineering best practices in Databricks notebooks

Setup ingredients:

https://docs.github.com/en/developers/overview/managing-deploy-keys#machine-users

https://github.com/join to create the repo user

TODO: Create or link to Aha ideas:

* GH deploy keys auth support for scoped access
* Support for discovering tests to be run, so that users do not need a repo admin in order to add new tests.

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
