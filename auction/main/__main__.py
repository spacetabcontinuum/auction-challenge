import sys
import json
import os
import settings
import response
import auction_dynamics
import adunit
from format import LogSettings

def load_config_library(config_file):
    try:
        with open(config_file,'r') as config:
            return json.load(config)
        config.closed
    except:
        log.error('Config file not found. Exiting.')
        sys.exit(1)

def load_input_library():
    try:
        input_library = json.load(sys.stdin)
        return input_library
    except:
        log.error('Input data is not type JSON. Exiting.')
        sys.exit(1)

if (__name__ == '__main__'):

    current_directory = os.getcwd()

    # Load json libraries
    config = load_config_library(current_directory+'auction/config.json')
    input = load_input_library()

    # Create known list of site settings
    known_site_entities = settings.Entity()
    known_site_entities.get_entities(config['sites'],['name','bidders','floor'],settings.Site)

    # Create known list of bidder settings
    known_bidders = settings.Entity()
    known_bidders.get_entities(config['bidders'],['name','adjustment'],settings.Bidder)

    # Filter input against known sites, bidders and ad units
    response.BidBouncer.filter_bid_responses(input,known_site_entities)

    # Hold the auction and get winners
    auction_output = auction_dynamics.hold_the_auction(known_site_entities.collection,known_bidders)

    # Print auction output
    print(auction_output)
