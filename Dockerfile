FROM python:3.12

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python", "./my_app.py"]
