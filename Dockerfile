# Stage 1: Builder
FROM python:3.10-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

COPY . .

# Stage 2: Final image
FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --from=builder /app /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
