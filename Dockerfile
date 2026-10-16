# Builds the guide site from the Markdown sources and serves it as static files.
# Stage 1: render Markdown -> site/
FROM python:3.12-slim AS build
WORKDIR /src
RUN pip install --no-cache-dir markdown==3.7
COPY README.md README.fa.md README.ar.md README.zh-CN.md ./
COPY docs ./docs
COPY assets ./assets
COPY site-src ./site-src
COPY scripts/build_site.py ./scripts/build_site.py
RUN python scripts/build_site.py --out /out

# Stage 2: serve
FROM caddy:2-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=build /out /srv
ENV PORT=8080
EXPOSE 8080
