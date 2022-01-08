# RTS

Real time strategy project.

Connect towers to send soldiers to another one. Win how can conquest all towers on the board. Connect to your friends or play online with other players from all around the world. For player guides, visit [RTS on Read The Docs](https://rts.readthedocs.io).

**Table of Contents**:

- [How to install](#how-to-install)
- [How to develop](#how-to-develop)
- [How to test](#how-to-test)
- [How to contribute](#how-to-contrinute)

## How to install

```sh
# Install deps
poetry install

# Run
poetry run python -m rts

# Or
poetry shell
python -m rts
```

Important! The game is actively tested only on Ubuntu, let me know if work fine or not on other systems.

Run `poetry install` to install dependencies.

## How to develop

Necessary tools:

- Pyenv:

  ```
  # Install pyenv
  curl https://pyenv.run | bash

  # Print last versions of CPython
  pyenv update
  pyenv install --list | grep " 3\."

  # Install the last version
  pyenv install <last_version>
  ```

- Poetry:
  ````
  # Install poetry
  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
  echo "export PATH=\"$HOME/.poetry/bin:$PATH\"" >> .bashrc
  ```
  ````

Before continue, read about [how to contribute](#how-to-contribute).

Now you can [run it](#how-to-install) or [test it](#how-to-test).

## How to test

```
poetry run python -m pytest -v tests/ # outside the venv

# or

python -m pytest -v tests/ # inside the venv
```

Tests are executed remotely only for pull_requests. Runs them before commit and push changes. Pre commit hooks will be added to the project in near future.

## How to contribute

Any contribute is appreciated. Fork the repo and open pull request or open issue for any advice.

I'm opening to both bug fixing or new feature requests. If you have a **Major Feature**, first open and outline your proposal so that it can be discussed; if you have a **Minor Feature**, you can open directly a pull request. Adding a new test case is always appreciated.

### Coding Rules

To ensure consistency throughout the source code, keep these rules in mind as you are working:

- All features or bug fixes must be tested by one or more specs (unit-tests);
- All public API methods from the game core must be documented;
- Follow as much as possible formatting given by automated formatter (to be added).

### Commit Message Format

Follow as much as possible the indication given in [this document from Angular](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-format) for Semantic Version Commit Message Format.

In the future, we will identify some specific scope for this project to use in commit's headers.
