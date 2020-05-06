# Auction Challenge Submission

## About the program

Hello! This repo contains my submission to the Sortable auction-challenge. This program handles two sources of input (config.json and input.json) and prints the results of the auction to the terminal. I have included a debug mode, as well as unit tests for the main auction compontents.

This is an object-oriented Python program. Incomming data is handled by the Reponse class and if valid, stored in instances of the main 6 main classes: Entity, Site, Ad Unit, AuctionManager, Bid and Bidder. These classes are nested (or related to one another) as outlined in the diagram below, with the AuctionManager handling the majority of the auction logic.

![class_structure](/images/class_structure.png?raw=true)

Each site provided in the config will generate a new Site instance. The input data is then validated against this sitelist, afterwhich both the ad units and bidders from each bid are filtered based against the master sitelist. Since the auction happens at the ad unit level, only one AuctionManager instance is created for each ad unit. The AuctionManager handles adding valid bids to its' instance to include in the auction.

Next, the execution direction begings to flow towards the higher classes. The AuctionManager pulls in the adjustment factor for each bidder and calculates an adjusted bid value. All bids for the ad unit then are evaluated and a top bid is produce. Within the Site instance, the top bid is evaluated for whether the adjusted bid value clears the site floor. The unadjusted/raw bid value is what is included in the auction output.

![execution_flow](/images/execution_flow.png?raw=true)

### Build and Execution
````
$ docker build -t challenge .
$ docker run -i -v /path/to/challenge/config.json:/auction/config.json challenge < /path/to/challenge/input.json
````

### Debug Mode
The auction can be run in debug mode by uncommenting the line below in the Dockerfile, then re-building the Docker image and executing the program as described above. Running debug mode will expose a series of messages, warnings and errors to the terminal to give you a better understanding of the auction as it progresses.

````
CMD ["python","-m","auction.main","--debug"]
````

![debug screenshot](/images/debug_mode_screenshot.png?raw=true)

### Test Mode
The program also includes several unit tests for the main auction components (~100% test coverage for Site and AuctionManager classes). The unit tests operate outside of the main auction program and can be run by uncommenting the lines below in the Dockerfile, rebuilding the Docker image and executing the program via `docker run challenge`.

````
ENV PYTHONPATH "${PYTHONPATH}:/auction/modules"
WORKDIR ./auction/modules
CMD ["python","-m","unittest","discover","-v"]
````
