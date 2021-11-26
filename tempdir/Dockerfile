FROM python
RUN pip install flask
RUN pip install flask_sqlalchemy
RUN pip install flask_marshmallow
COPY  ./static /home/myapp/static/
COPY  ./templates /home/myapp/templates/
COPY  web_server.py /home/myapp/
COPY  Customer.sqlite /home/myapp/
EXPOSE 8080
CMD python3 /home/myapp/web_server.py
