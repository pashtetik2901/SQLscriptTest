FROM python
WORKDIR /app
COPY database /app/database
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload" ]