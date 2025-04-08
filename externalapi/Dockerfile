FROM python:3.10-slim
WORKDIR /app
COPY main.py .
RUN pip install fastapi uvicorn
EXPOSE 8081
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
