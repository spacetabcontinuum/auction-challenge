# Auction Challenge Submission


## Build and Execution
````
$ docker build -t challenge .
$ docker run -i -v /path/to/challenge/config.json:/auction/config.json challenge < /path/to/challenge/input.json
````

## Debug Mode
In Dockerfile, add the flag '--debug' to CMD enter debug mode. This will expose a series of debug messages, warnings and errors to the terminal to give you a better understanding of the auction progress.

````
CMD ["python","-m","auction.main","--debug"]
````

![alt text](https://github.com/spacetabcontinuum/auction-challenge/debug_mode_screenshot.png")
