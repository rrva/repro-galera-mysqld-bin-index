docker build -t galera-repro .
virtualenv env
./env/bin/pip install -r requirements.txt
