FROM python:3.12

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "flask", "--app", "my_app", "run", "--host=0.0.0.0" ]
