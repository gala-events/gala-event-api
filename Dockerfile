FROM python:3.7-alpine as base

FROM base as builder

RUN mkdir /install

WORKDIR /install

ADD ./src/api/requirements.txt ./requirements.txt

RUN apk add gcc libc-dev make

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install -r requirements.txt

FROM base

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY ./src/api ./

ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH=/app

EXPOSE 80

ENV MONGO_HOST_URI=mongo

# ENTRYPOINT ["/bin/sh"]

CMD ["uvicorn", "server:app", "--reload", "--host", "0.0.0.0", "--port", "80" ]
