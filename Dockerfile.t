FROM python:3.11

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your specific requirements file into the container
COPY requirements.txt .

# 4. Install the libraries exactly as you froze them
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy all your Python files into the container
COPY . .

# 6. Expose the port FastAPI uses
EXPOSE 8000

# 7. Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]