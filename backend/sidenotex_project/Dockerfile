ARG NODE_VERSION=18
ARG PYTHON_VERSION=3.11
FROM python:$PYTHON_VERSION-slim as runtime

WORKDIR /opt/app/

RUN groupadd -r nonroot
RUN useradd -g nonroot --no-create-home nonroot
# Setup virtualenv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DEBUG=false
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com

RUN python -m venv /opt/venv/
# Install dependencies before copying application code to leverage docker build caching
COPY requirements.txt .
RUN pip install -U pip -r requirements.txt

# Copy application code (see .dockerignore for excluded filesaa)
COPY . .
#COPY --from=build /opt/app/static/assets/ ./static/assets/
RUN mkdir -p /opt/app/static
RUN python manage.py collectstatic --clear --noinput

# Build arguments should be converted to environment variables to persist
ARG DJANGO_SUPERUSER_PASSWORD
ENV DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD
ARG EMAIL_HOST_PASSWORD
ENV EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD

RUN echo "${DJANGO_SUPERUSER_PASSWORD}" > /opt/app/DJANGO_SUPERUSER_PASSWORD && \
    echo "${EMAIL_HOST_PASSWORD}" > /opt/app/EMAIL_HOST_PASSWORD

RUN chown -R nonroot:nonroot /opt/app/
USER nonroot

EXPOSE 8001

CMD ["bin/app", "web"]