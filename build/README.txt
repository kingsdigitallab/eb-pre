
The requirements.txt works with a python 3.10 environment (last tested on 2026-02-13).

```
# TODO: convert this into a Docker compose!

# cd into the root folder of the repository.
# run a python 3.10 container:
docker run -ti --rm -v .:/prj python:3.10-slim bash

# then within the container, install dependencies
sudo apt update && sudo apt install -y build-essential gcc python3-dev
cd /prj
python -m venv venv
. venv/bin/activate
pip install -r build/requirements.txt

```
