FROM python:3.12-alpine AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM base AS test
RUN pip install pytest pytest-asyncio httpx
CMD ["pytest", "test_app.py", "--asyncio-mode=auto"]

FROM base AS production
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
