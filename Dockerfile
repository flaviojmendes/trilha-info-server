FROM python:3.9  

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code/

COPY /etc/letsencrypt/live/api.trilha.info/cert.pem /code/cert.pem
COPY /etc/letsencrypt/live/api.trilha.info/privkey.pem /code/privkey.pem

CMD ["python", "main.py"]