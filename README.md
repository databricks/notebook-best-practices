# Example: Using software engineering best practices in Databricks notebooks

TODO: Create or link to Aha ideas:

* GH deploy keys auth support for scoped access
* Support for discovering tests to be run, so that users do not need a repo admin in order to add new tests.

Setup instructions:

Corresponding to [Python 3.8.10 in the 10.4 LTS release](https://docs.databricks.com/release-notes/runtime/10.4.html#system-environment).

OSX

```
brew install pyenv pipenv
pyenv install 3.8.10
pipenv install -r requirements.txt --python 3.8.10
```