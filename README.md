# pynetbox-api
FastAPI layer above pynetbox lib.

## Install (Dev Mode Only)

Before installing, you must provide environment variables at `./pynetbox_api/env.py`.

The project supports only dev-mode package installation currently, as it is on beta stage.

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
uv run fastapi dev
```