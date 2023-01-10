FROM tensorflow/tensorflow:2.7.4
ENV env_local_registry_path="models"
WORKDIR /app
COPY . .
COPY requirements.txt requirements.txt
COPY setup.py setup.py
RUN mkdir -p /tmp/model
RUN mkdir -p /tmp/tokenizer
COPY ${env_local_registry_path}/model /tmp/model
COPY ${env_local_registry_path}/tokenizer /tmp/tokenizer
RUN pip install -e .
CMD uvicorn api.fast:app --host 0.0.0.0 --reload --port $PORT
