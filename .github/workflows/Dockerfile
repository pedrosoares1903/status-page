FROM python:3.11-slim

WORKDIR /app

# Dependencies first, on their own layer: this step is only re-run when
# requirements.txt changes, not on every code edit.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py targets.yml ./
COPY src/ ./src/

# Never run as root. If anything ever goes wrong inside this container,
# the process should not own the filesystem.
RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p /app/public \
    && chown -R appuser:appuser /app/public
USER appuser

ENTRYPOINT ["python", "main.py"]