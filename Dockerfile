FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0"]
