ARG NODE_VERSION=18
ARG PYTHON_VERSION=3.11

# Build assets
#FROM node:$NODE_VERSION as build
#WORKDIR /opt/app/
#COPY package.json yarn.lock ./
#RUN yarn install
#COPY . .
#RUN yarn build:js
#RUN yarn build:css
# Runtime
FROM python:$PYTHON_VERSION-slim as runtime

WORKDIR /opt/app/

RUN groupadd -r nonroot
RUN useradd -g nonroot --no-create-home nonroot

# RUN apt-get update -y && apt-get install -y curl postgresql-client

# Setup virtualenv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DEBUG=false
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com
ENV DJANGO_SUPERUSER_PASSWORD=TtBAQGb9CmUn8ueNWXVg39Rq

RUN python -m venv /opt/venv/

# Install dependencies before copying application code to leverage docker build caching
COPY requirements.txt .
RUN pip install -U pip -r requirements.txt

# Copy application code (see .dockerignore for excluded filesaa)
COPY . .
#COPY --from=build /opt/app/static/assets/ ./static/assets/
RUN mkdir -p /opt/app/static
RUN python manage.py collectstatic --clear --noinput
RUN chown -R nonroot:nonroot /opt/app/
USER nonroot

EXPOSE 8001

CMD ["bin/app", "web"]
