python3 -m venv .venv

source .venv/bin/activate

flask --app hello run


docker build -t pythontest:latest . 