FROM python:3.12-slim

# pour voir les logs de flask directement
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# message par defaut, on peut le changer avec -e MESSAGE="..."
ENV MESSAGE="Bienvenue depuis Docker"

EXPOSE 5000

CMD ["python", "main.py"]
