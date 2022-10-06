FROM python:3.9
WORKDIR .

# Install appropriate dependencies.
# RUN apt-get -y update  && apt-get install -y \
#     python3-dev \
#     apt-utils \
#     python-dev \
#     build-essential \   
# && rm -rf /var/lib/apt/lists/* 

COPY requirements.txt .
RUN pip install --no-cache-dir -U -r  requirements.txt

COPY demo/ ./app
COPY saved_models/best_models ./saved_models/best_models
COPY prose/ ./prose

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
