FROM python:3.13-alpine
LABEL maintainer="gabrieldelimaafonso@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY portfolio /portfolio

WORKDIR /portfolio

RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /portfolio/requirements.txt && \
  adduser --disabled-password --no-create-home duser && \
  chmod -R a+rw /portfolio

ENV PATH="/venv/bin:${PATH}"

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:8000"]
