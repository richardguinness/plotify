FROM tensorflow/tensorflow:2.7.4
# ENV env_local_registry_path=$local_registry_path
# ENV env_local_registry_path="models/22-12-08-09-42"
ENV env_local_registry_path="/models"
# RUN echo ${env_local_registry_path}
WORKDIR /app
COPY . .
COPY requirements_prod.txt requirements.txt
COPY setup.py setup.py
RUN mkdir -p /tmp/model
RUN mkdir -p /tmp/tokenizer
COPY ${env_local_registry_path}/model /tmp/model
COPY ${env_local_registry_path}/tokenizer /tmp/tokenizer
RUN pip install -e .
CMD uvicorn api.fast:app --host 0.0.0.0 --reload --port $PORT
