# MyWebsite

## Overview

MyWebsite is a personal website for Benjamin Hamon, hosted at www.benjaminhamon.com.

The project is open source software. See [About](about.md) for more information.

## Development

To set up a workspace for development, create a `python3` virtual environment then install the project locally, so that scripts will execute successfully.

```
pip3 install --upgrade --editable .
```

To generate the project metadata and install dependencies, run the `develop` command:

```
python3 ./scripts/main.py develop
```

To run the website:

```
python3 ./scripts/website.py --address localhost --port 5000
```
