FROM python:3.9
WORKDIR /

RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -U torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

COPY ./requirements.txt .
RUN pip install --no-cache-dir -U -r requirements.txt

COPY ./demo/ /app/
COPY ./saved_models/best_models/ /saved_models/best_models/
COPY ./prose/ /prose/

WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
