FROM tiangolo/uvicorn-gunicorn:python3.8

# Create the directory for the container
WORKDIR /src
COPY requirements.txt ./requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt


COPY ./src/ ./src

# Run by specifying the host and port
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "443"]