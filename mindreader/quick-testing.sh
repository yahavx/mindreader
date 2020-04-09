cd ~/mindreader
source .env/bin/activate

docker run -d -p 27017:27017 mongo
docker run -d -p 5672:5672 rabbitmq

python -m mindreader us 3
python -m mindreader.server run-server
python -m mindreader.parsers run-parsers
python -m mindreader.saver run-saver

python -m mindreader.client upload-sample
python -m mindreader.api run-server
snap run intellij-idea-community

# sphinx
export PYTHONPATH=$PWD
sphinx-quickstart docs/
make html -C ./docs
cd docs/build/html/
python -m http.server

PYTHONPATH=. sphinx-autogen docs/index.rst

# pytest
pytest --cov=mindreader --cov-report=html tests/ && cd htmlcov/ && python -m http.server

# full pipeline
cd ~/mindreader
source .env/bin/activate
python -m mindreader.server run-server &
python -m mindreader.parsers run-parsers &
python -m mindreader.saver run-saver &

