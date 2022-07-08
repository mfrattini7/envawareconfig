# Envawareconfig

Load configurations from yaml files with automatic environment variable substitution.

## Installation

with [pip](https://pip.pypa.io/en/stable/):

`pip install envawareconfig`

with [poetry](https://python-poetry.org/):

`poetry add envawareconfig`

## QuickStart

Suppose you have a configuration file like this:

```yaml
# test-config.yaml
database:
  name: my-database
  user: "${DB_USER:admin}"
  password: "${DB_PASSWORD}"
```

and that you have set the environment variable `DB_PASSWORD` to `my-secret-password`
while `DB_USER` has been left unset.

then running the following code:

```python
# main.py

from envawareconfig import load_config

config = load_config("tests/test-config.yaml")
```

would result in:
```python
config = {
    "database": {
        "name": "my-database",
        "user": "admin",
        "password": "my-secret-password"
    }
}
```

Notice that `${DB_PASSWORD}` has been expanded and `${DB_USER:admin}` used the default value.
