FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
WORKDIR /Peer39task
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ..
CMD ["uvicorn","main:main","--host","0.0.0.0","--port", "8000"]