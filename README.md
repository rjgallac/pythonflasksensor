python3 -m venv .venv

source .venv/bin/activate

flask --app hello run


docker build -t pythontest:latest . 


docker run -p5001:5000 pythontest:latest