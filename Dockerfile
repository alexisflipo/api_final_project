FROM tiangolo/uvicorn-gunicorn:python3.8

# Create the directory for the container
WORKDIR /src
COPY requirements.txt ./requirements.txt

# ENV PORT=$PORT
# ARG PORT=$PORT
# ARG PORT
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
COPY ./start.sh .
RUN chmod +x start.sh
COPY ./src/ .
CMD ["./start.sh"]
# CMD ["python3", "app.py"]