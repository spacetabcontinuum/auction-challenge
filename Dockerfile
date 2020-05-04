FROM python:3.8



#COPY requirements.txt /challenge
#RUN pip install -f requirements.txt


COPY auction auction
ENV PYTHONPATH "${PYTHONPATH}:/auction/modules"

CMD ["python","-m","auction.main","--debug"]
