FROM python:3.9.6-slim

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src src
COPY pyproject.toml pyproject.toml
COPY setup.cfg setup.cfg
COPY setup.py setup.py
RUN pip install -e .
RUN python -m pip install "pymongo[srv]"
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('wordnet')"

EXPOSE 8080
EXPOSE 5000

CMD ["python", "src/nlp_case/server/app/main.py" ]