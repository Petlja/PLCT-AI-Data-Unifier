# PLCT AI Data Unifier

Tools to fetch and lightly preprocess Sphinx-based documentation repositories.

This tool prepares course content for the PLCT AI pipeline. It extracts and enriches data from supported course formats, then outputs a normalized dataset that is used as input to the AI context builder (instead of processing raw markup files directly).

In the [PLCT Server deployment flow](https://github.com/Petlja/PLCT-Server/blob/main/doc/getting_started.md), this tool sits before context generation and helps produce cleaner, consistent input for AI context creation.

- [PLCT](https://github.com/Petlja/PLCT-CLI)
- [PetljaDoc](https://github.com/Petlja/PetljaDoc)

## Setup

Prerequisites:

- [uv](https://docs.astral.sh/uv/)
- Git

This project uses `uv` to manage the virtual environment and dependencies.

Quick start:

```powershell
# Create the virtual environment and install dependencies from pyproject.toml
uv sync

# Create a local config file from sample
Copy-Item config-sample.yaml plct-ai-data-unifier-config.yaml

# Run the bootstrap command (installs pandoc, syncs repos, prepares dataset)
uv run aidu bootstrap --config plct-ai-data-unifier-config.yaml --base-dir repos --output-dir dataset
```


## Commands

### `bootstrap`

Convenience command that runs the full local setup flow: ensures Pandoc is installed, syncs repositories listed in `plct-ai-data-unifier-config.yaml` (or another config), then prepares the dataset by converting activity files into normalized Markdown.

Options:

- `--config`: path to config file (`.yaml`, `.yml`, or `.json`)
- `--base-dir`: directory where repositories are cloned/updated
- `--output-dir`: directory where the normalized dataset is written
- `--jobs`: number of worker threads: 1 = serial; default is number of CPUs

What it does:
- Runs `get-pandoc` (installs Pandoc via `pypandoc` if missing).
- Runs `git-sync` to clone or update repositories from your config file into `--base-dir`.
- Runs `prepare-dataset` to collect activity files and convert them into markdown under `--output-dir`.

Basic usage:

```powershell
uv run aidu bootstrap
```

Options examples:

```powershell
uv run aidu bootstrap --config my-config.yaml --base-dir repos --output-dir dataset
```


### `get-pandoc`

Installs Pandoc (using `pypandoc`) if it is not already available, or reports the installed version.

Basic usage:

```powershell
uv run aidu get-pandoc
```

### `git-sync`

Clone or update repositories listed in a config file (`.yaml`, `.yml`, or `.json`).

Options:

- `--config`: path to config file (`.yaml`, `.yml`, or `.json`)
- `--base-dir`: directory where repositories are cloned/updated

Basic usage:

```powershell
uv run aidu git-sync
```

Options examples:

```powershell
uv run aidu git-sync --config my-config.yaml
uv run aidu git-sync --base-dir repos
```

The config file is a YAML with a top-level `repos` array. Each item may be either a string (the repo URL) or an object with key `url`.

Example `config-sample.yaml`:

```yaml
repos:
  - url: https://example.com/repo1.git
  - url: https://example.com/repo2.git
```

### `prepare-dataset`

Convert activity/source files from each repository into a normalized Markdown dataset. This command detects the project type (when possible), collects the list of files from `_sources/index.yaml` or `_sources/index.md`, and converts them to Markdown using Pandoc.

Additional options:

- `--base-dir`: directory where repositories are cloned/updated
- `--output-dir`: directory where the normalized dataset is written
- `--jobs`: number of worker threads: 1 = serial; default is number of CPUs


Basic usage:

```powershell
uv run aidu prepare-dataset
```

Options examples:

```powershell
uv run aidu prepare-dataset --base-dir repos --output-dir dataset --jobs 1
uv run aidu prepare-dataset --base-dir repos --output-dir dataset
uv run aidu prepare-dataset --base-dir repos --output-dir dataset --jobs 4
```

