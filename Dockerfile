FROM python:latest
ENV PYTHONUNBUFFERED=1
WORKDIR /rms
COPY . /rms
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
EXPOSE 8000:8000
CMD ["python", "manage.py", "migrate", "&", "python", "manage.py", "runserver", "0.0.0.0:8000"]