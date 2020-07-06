FROM python:3.8-alpine

COPY . /src
RUN apk add --no-cache gcc musl-dev
RUN python -m venv /venv
RUN /venv/bin/pip install -r /src/requirements/prod.txt

CMD /venv/bin/python /src/main.py /src/sample.txt