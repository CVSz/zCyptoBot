FROM python:3.12-slim
WORKDIR /app
COPY src/ /app/src/
RUN pip install fastapi uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
