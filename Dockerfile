FROM python:3

WORKDIR /src

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP /src/src/app:webapp
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
