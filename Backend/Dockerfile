# Install the base image
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
#RUN --mount=type=cache,target=/root/.cache/uv \
#    --mount=type=bind,source=uv.lock,target=uv.lock \
#    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#    uv sync --frozen --no-install-project

# Copy the project into the image
ADD . /app

# Sync the project
#RUN --mount=type=cache,target=/root/.cache/uv \
#    uv sync --frozen
RUN uv sync --frozen

RUN uv run manage.py migrate

# Run the application
#CMD ["uv", "run", "manage.py", "runserver"]
#CMD ["uv", "run", "manage.py", "migrate"]