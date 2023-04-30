FROM python:3.10

ENV HOME=/tmp

RUN mkdir $HOME/genie.io
WORKDIR $HOME/genie.io

COPY utils utils
COPY CLI.py CLI.py
COPY secrets.env secrets.env
COPY constants.py constants.py
COPY genie_driver.py genie_driver.py
COPY requirements.txt requirements.txt
COPY mount_food_101.py mount_food_101.py

EXPOSE 5000

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN python -m venv venv &&\
    source venv/bin/activate && \
    pip3 install --upgrade pip &&\
    pip3 install -r requirements.txt &&\
    chmod -R 775 .


ENTRYPOINT ["/bin/bash", "-c", "export $(cat secrets.env | xargs) && source venv/bin/activate && python mount_food_101.py && python genie_driver.py --new-genie --num-types=20 --api-mode"]