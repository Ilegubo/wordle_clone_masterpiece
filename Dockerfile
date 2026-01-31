# 1. Start from Python (Linux-based)
FROM python:3.13.9

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy dependency list first
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the project files
COPY . .

# 6. Run the application
CMD ["python", "main.py"]
