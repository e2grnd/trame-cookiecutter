FROM gcr.io/sandbox-225221/python:trame-egl 
ARG NPM_GITHUB_REGISTRY_TOKEN
RUN test -n "$NPM_GITHUB_REGISTRY_TOKEN" || (echo "NPM_GITHUB_REGISTRY_TOKEN is not set" && false)


RUN apt-get update; \
  apt-get install -y --no-install-recommends \
  git

USER trame-user
RUN git config --global url."https://${NPM_GITHUB_REGISTRY_TOKEN}@github.com/".insteadOf "ssh://git@github.com/"

USER root
