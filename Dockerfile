FROM python:3.13.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Run as a web service on port 8080
CMD ["python", "word_game.py", "--web", "--port", "8080"]