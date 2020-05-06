FROM python:3.8

COPY auction auction
ENV PYTHONPATH "${PYTHONPATH}:/auction"
ENV PYTHONPATH "${PYTHONPATH}:/auction/modules"

## Comment out the line below if you want to run either debug or test mode
CMD ["python","-m","auction.main"]

## Uncomment the line below to run debug mode
#CMD ["python","-m","auction.main","--debug"]

## Uncomment the lines below to run tests
#WORKDIR ./auction/modules
#CMD ["python","-m","unittest","discover","-v"]
