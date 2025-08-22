FROM python:3.12.6-alpine3.20
LABEL maintainer="gabrieldelimaafonso@gmail.com"

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY portfolio /portfolio
COPY scripts /scripts

WORKDIR /portfolio

RUN chmod +x /scripts/commands.sh && \
  chmod -R a+rw /portfolio


EXPOSE 8000

RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /portfolio/requirements.txt && \
  adduser --disabled-password --no-create-home duser

ENV PATH="/venv/bin:/scripts:${PATH}"

CMD ["commands.sh"]