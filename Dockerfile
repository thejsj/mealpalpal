FROM django

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD . /app
WORKDIR /app

CMD [ "/app/entrypoint.sh" ]
