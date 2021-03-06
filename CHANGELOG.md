# Changelog

Adheres to the [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
and [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) recommendations.
After v1.0, will follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).


## [0.6.0] - unreleased


## [0.5.x] - 2020-05-15

### Fixed
- `poetry.lock was not deleted
- some files, including `__init__.py`, were ignored
- fixed options in `tox.ini`
- removed some stupid items in `pyproject.toml`
- proper handling of dashes and underscores
- git config was not used
- removed `.coverage` sqllite file

## [0.5.0] - 2020-05-11

### Added
- `CITATION.cff` and `codemeta.json`
- `CONTRIBUTING.md` and issue and pull request templates
- Unfinished `update` command

### Changed
- The way authors, maintainers, and contributors are listed

### Fixed
- Split `cli.py` into multiple files


## [0.4.x] - 2020-05-09

### Fixed
- Incorrect processing of pip requirements in `env`
- Missing `path` argument to `env`


## [0.4.0] - 2020-05-09

### Added
- Tyrannosaurus commands to tox
- Upload sdist and wheel to release
- Workflow to release on tag

### Changed
- Python version for building to 3.8
- Renamed `reqs` to `info`

### Removed
- `check-added-large-files`, which is too slow

### Fixed
- The test workflow wasn’t testing
- A bug getting the `git config` when called with `new`


## [0.3.0] - 2020-05-08

### Added
- Command `env`


## [0.2.0] - 2020-05-08

### Added
- Commands `new`, `sync`, `recipe`, and `clean`

### Fixed
- Several minor build issues
- Documentation formatting


## [0.1.0] - 2020-05-05

### Added
- Github actions


## [0.0.3] - 2020-05-05

### Fixed
- Failing docs build.
- Renamed changelog to `CHANGELOG.md` and added structure.


## [0.0.2] - 2020-04-31

Completely different project with a different purpose.

### Changed
- Revamped build structure, removing `setup.py`.

### Added
- A `tox.ini` with a single entry point.

### Removed
- `metadata.py`. Use `__init__.py` instead.
- Various nonsense code


## [0.0.1] - 2020-04-02

### Added
Nonsense code and docs that were never used.
