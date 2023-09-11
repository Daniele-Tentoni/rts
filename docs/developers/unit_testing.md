# Unit testing

Unit tests are useful to assure that a feature don't break the current working game.

Run them with those commands:

Use as usual following commands to run pytest test suites:

```
poetry run python -m pytest <options> # outside the venv

# or

python -m pytest <options> # inside the venv
```

### Often used options

Use `-v` to get verbose output.

Use `--duration=n` to report the n-th long running tests.

Use `--cov=rts` to measure the code coverage.

Use `--cov-report term-missing:skip-covered --cov=rts` to report missing covered lines without showing full covered files.

The complete command used by me in last development is `poetry run python -m pytest tests --cov=rts --cov-report term-missing:skip-covered`.

Tests are executed remotely only for pull_requests. Runs them before commit and push changes. Pre commit hooks will be added to the project in near future.

### Unit testing on video/audio-less devices

For example, in Github Actions environment, where our unit tests runs each pull request, there aren't video and audio devices. In that case, pygame expose two environment variables called *SDL_VIDEODRIVER* and *SDL_AUDIODRIVER* to set to dummy values to permit to run pygame suite without errors about the broken initialization.

You can set those environment variables with this configuration:

```
- name: Run pytest
  env: # Added those env vars
    SDL_VIDEODRIVER: "dummy"
    SDL_AUDIODRIVER: "disk"
  run: poetry run python -m pytest tests/
```
