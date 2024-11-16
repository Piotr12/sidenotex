ARG NODE_VERSION=18
ARG PYTHON_VERSION=3.11
FROM python:$PYTHON_VERSION-slim as runtime

WORKDIR /opt/app/

RUN groupadd -r nonroot
RUN useradd -g nonroot --no-create-home nonroot

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DEBUG=false
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com

RUN python -m venv /opt/venv/
COPY requirements.txt .
RUN pip install -U pip -r requirements.txt

COPY . .
RUN mkdir -p /opt/app/static
RUN python manage.py collectstatic --clear --noinput

RUN chown -R nonroot:nonroot /opt/app/
USER nonroot

EXPOSE 8001

CMD ["bin/app", "web"]