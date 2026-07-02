# Dockerfile

# Slim variant — smaller image, no extras. Like using node:18-alpine over node:18.
FROM python:3.11-slim

# Set working directory inside the container — like your project root
WORKDIR /app

# Copy requirements first — before the rest of the code.
# Docker builds in layers. If requirements.txt hasn't changed,
# this layer is cached and pip install is skipped on rebuild.
# Same reason you'd COPY package.json + npm install BEFORE COPY . in Node Dockerfiles.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the source code
COPY . .

# Document that the container listens on 8000 (doesn't actually publish it — that's Compose's job)
EXPOSE 8000

# Start the server. No --reload in production images.
# We'll override this in Compose for dev to get hot reload.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]