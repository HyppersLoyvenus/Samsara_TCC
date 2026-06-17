FROM python:3.14.6-alpine
WORKDIR /usr/src/app 

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x teste.sh
ENTRYPOINT ["./teste.sh"]
