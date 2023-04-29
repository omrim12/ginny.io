FROM python:3.10

ENV HOME=/tmp

RUN mkdir $HOME/genie.io
WORKDIR $HOME/genie.io

COPY utils $HOME/genie.io/utils
COPY CLI.py $HOME/genie.io/CLI.py
COPY constants.py $HOME/genie.io/constants.py
COPY genie_driver.py $HOME/genie.io/genie_driver.py
COPY genie_net.h5 $HOME/genie.io/genie_net.h5
COPY genie_metadata.json $HOME/genie.io/genie_metadata.json
COPY requirements.txt $HOME/genie.io/requirements.txt
COPY images/food-101/food-101/meta/labels.txt $HOME/genie.io/images/food-101/food-101/meta/labels.txt

EXPOSE 5000

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN python -m venv venv &&\
    source venv/bin/activate && \
    pip3 install --upgrade pip &&\
    pip3 install -r requirements.txt

ENTRYPOINT ["/bin/bash", "-c", "source venv/bin/activate && python genie_driver.py --new-genie --num-types=20 --api-mode"]