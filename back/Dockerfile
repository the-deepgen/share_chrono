FROM alpine

RUN sudo apt install virtualenv python3.8-dev python3-pip python3-tk cmake

COPY . /back

WORKDIR /back

RUN pip install pipenv

RUN cd back && pipenv install

CMD ["py", "server.py"]