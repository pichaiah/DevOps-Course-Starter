FROM python:3.8-slim-buster as base
WORKDIR /usr/src/app
RUN pip install poetry
ENV PATH=/root/.poetry/bin:${PATH}

################## prod ####################
FROM base as production
WORKDIR /usr/src/app
ENV PORT=5000
COPY pyproject.toml .
RUN poetry install
COPY ./ ./
RUN chmod 777 run.sh
ENTRYPOINT ./run.sh

################ development ################
FROM base as development
COPY ./pyproject.toml ./
RUN poetry install
ENTRYPOINT poetry run flask run --host=0.0.0.0

############## test #######################
FROM base as test
COPY pyproject.toml .
RUN poetry install


# Install the latest versions of Mozilla Firefox and Geckodriver
RUN export DEBIAN_FRONTEND=noninteractive && apt-get update \
  && apt-get install --no-install-recommends --no-install-suggests --assume-yes \
    curl \
    bzip2 \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    xvfb \
  && FIREFOX_DOWNLOAD_URL='https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64' \
  && curl -sL "$FIREFOX_DOWNLOAD_URL" | tar -xj -C /opt \
  && ln -s /opt/firefox/firefox /usr/local/bin/ \
  && BASE_URL='https://github.com/mozilla/geckodriver/releases/download' \
  && VERSION=$(curl -sL 'https://api.github.com/repos/mozilla/geckodriver/releases/latest' | grep tag_name | cut -d '"' -f 4) \
  && curl -sL "${BASE_URL}/${VERSION}/geckodriver-${VERSION}-linux64.tar.gz" | tar -xz -C /usr/local/bin \
  && apt-get purge -y \
    curl \
    bzip2 \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /tmp/* /usr/share/doc/* /var/cache/* /var/lib/apt/lists/* /var/tmp/*
  
# Copy all files
COPY ./ ./

# Setup the entry point
ENTRYPOINT ["poetry", "run", "pytest"]
