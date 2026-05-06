# 1. Use an official, lightweight Python image
FROM python:3.11

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of your project files (main.py, index.html, etc.)
COPY . .

# 5. Expose port 8000 and run the FastAPI server
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]