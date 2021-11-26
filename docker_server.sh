#!/bin/bash
mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp web_server.py tempdir/.
cp Customer.sqlite tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

echo "FROM python" >> tempdir/Dockerfile
echo "RUN pip install flask" >> tempdir/Dockerfile
echo "RUN pip install flask_sqlalchemy" >> tempdir/Dockerfile
echo "RUN pip install flask_marshmallow" >> tempdir/Dockerfile

echo "COPY  ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY  ./templates /home/myapp/templates/" >> tempdir/Dockerfile
echo "COPY  web_server.py /home/myapp/" >> tempdir/Dockerfile
echo "COPY  Customer.sqlite /home/myapp/" >> tempdir/Dockerfile

echo "EXPOSE 8080" >> tempdir/Dockerfile
echo "CMD python3 /home/myapp/web_server.py" >> tempdir/Dockerfile

cd tempdir
docker build -t webserver .

docker run -it -d -p 8080:8080 --name webserverrunning webserver

docker ps -a