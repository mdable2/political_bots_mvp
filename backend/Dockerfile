FROM pytorch/pytorch:1.9.1-cuda11.1-cudnn8-runtime

ADD ./requirements.txt ./requirements.txt

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

ADD . .

ENTRYPOINT ["gunicorn", "server:app", "--workers", "3", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--log-level", "info"]