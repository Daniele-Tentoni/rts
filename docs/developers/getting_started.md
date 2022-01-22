# Getting started

Here you learn what you need and have to do start to develop. Any contribute is appreciated. We are opening to both bug fixing or new feature requests.

## Tools

Tools you need:
1) [Pyenv](https://github.com/pyenv/pyenv#installation) as environment manager
2) [Poetry](https://python-poetry.org/docs/#installation) as dependency manager

Then you can install project dependencies with Poetry:

```
poetry install
```

Then you have to open the poetry shell and start your preferred IDE in the virtual environment:

```
poetry shell
code . # Run vscode
```

## Git repository

You have to fork the main repository to get your copy, since that you have to work on it and assure that all tests passes before opening a Pull Request to the main repository. To achieve that, follow [this guide](https://docs.github.com/en/get-started/quickstart/fork-a-repo) from Github friends.

## Contributions

We are opening to both bug fixing or new feature requests. If you have a **Major Feature**, first open and outline your proposal so that it can be discussed; if you have a **Minor Feature**, you can open directly a pull request. Adding new test cases is always appreciated.

### Coding Rules

To ensure consistency throughout the source code, keep these rules in mind as you are working:

- All features or bug fixes must be tested by one or more specs (unit-tests);
- All public API methods from the game core must be documented;
- Follow as much as possible formatting given by automated formatter (to be added).

### Commit Message Format

Follow as much as possible the indication given in [this document from Angular](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-format) for Semantic Version Commit Message Format.

In the future, we will identify some specific scope for this project to use in commit's headers.
