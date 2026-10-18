FROM ghcr.io/astral-sh/uv:0.13.1@sha256:4a1f3666816dafadd20ceb71eac9a7d56d7ef30279f7d64048519ab901ada336 AS uv
FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1
COPY --from=uv /uv /uvx /usr/local/bin/
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 1000 dev && useradd --uid 1000 --gid dev --create-home dev \
    && mkdir -p /workspaces/kit/.venv /home/dev/.cache/uv \
    && chown -R dev:dev /workspaces/kit /home/dev/.cache
ENV UV_LINK_MODE=copy
USER dev
WORKDIR /workspaces/kit
CMD ["sleep", "infinity"]
