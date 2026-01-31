FROM python:3.13.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
# Run as web app to avoid missing libgtk-3 desktop libraries
CMD ["python", "word_game.py", "--web", "--port", "8080"]