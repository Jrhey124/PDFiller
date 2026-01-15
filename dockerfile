FROM python:3.12-slim

# Install LibreOffice Writer + dependencies
RUN apt-get update && apt-get install -y \
    libreoffice-writer \
    libreoffice-core \
    fonts-dejavu \
    libxinerama1 libglu1-mesa libsm6 libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole repo
COPY . /app/

EXPOSE 8000

# Run manage.py from the docxsite folder
CMD ["python", "/app/docxsite/manage.py", "runserver", "0.0.0.0:8000"]
