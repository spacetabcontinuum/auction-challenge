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

def find(list, key, value):
    for i, d in enumerate(list):
        if d[key] == value:
            return i
    return -1

def validate_input_and_store_bids(input,valid_sites,sorted_bidder_list):
    for i in input:
        for site in valid_sites.collection:
            if i['site'] == site.domain:
                for u in i['units']:
                    site.set_ad_unit(u)
                    log.message('Loaded ad unit ' + u + ' for ' + site.domain )

                sorted_raw_bids = sorted(i['bids'], key=lambda k: (k['bidder'], k['unit']))

                bid_count = 0
                for raw_bid in sorted_raw_bids:
                    bid_count += 1
                    bidder_index = find(sorted_bidder_list.collection,'name',raw_bid['bidder'])
                    if bidder_index == -1:
                        log.warning('Bidder ' + raw_bid['bidder'] + ' not found for site ' + site.domain + '. Ignoring response as invalid.')
                        break
                    else:
                        raw_bid['adjustment_factor'] = sorted_bidder_list.collection[0].adjustment

                        if raw_bid['unit'] in i['units']:
                            for ad_unit in site.ad_units:
                                if ad_unit.name == raw_bid['unit']:
                                    ad_unit.auction_manager.store_valid_bid(raw_bid['bidder'],raw_bid['bid'],raw_bid['adjustment_factor'])
                                    log.message('Bidder response for ' + raw_bid['unit'] + ': ' + str(raw_bid['bid']) + ' from ' + raw_bid['bidder'] + ' (bid adjustment of ' + str(raw_bid['adjustment_factor']) + ')' )
                        else:
                            log.warning('Ad Unit ' + raw_bid['unit'] + ' not found. Ignoring response as invalid.')

def hold_auctions(all_possible_auctions):
    auction_output = []
    for site in all_possible_auctions.collection:
        for ad in site.ad_units:
            log.message('Holding auction for ' + ad.name + ' in ' + site.domain)
            ad.auction_manager.get_top_bid()
        site.get_winning_bids_above_site_floor()
        log.announcement('Auction is complete!')
        auction_output.append(site.winning_bids)
    return auction_output


if (__name__ == '__main__'):
    import sys

    log = LogSettings()
    log.debug_enabled()

    current_directory = os.getcwd()

    # Load json libraries
    config = load_config_library(current_directory+'auction/config.json')
    input = load_input_library()

    # Create known list of sites, bidders
    known_site_entities = settings.Entity()
    known_site_entities.get_valid_entities(config['sites'],['name','bidders','floor'],settings.Site)

    known_bidders = settings.Entity()
    known_bidders.get_valid_entities(config['bidders'],['name','adjustment'],settings.Bidder)

    known_bidders.sort_collection('name')

    # Filter input against known sites, bidders and ad units
    validate_input_and_store_bids(input,known_site_entities,known_bidders)

    # Hold the auction and get winners
    auction_output = hold_auctions(known_site_entities)

    # Print auction output
    print(auction_output)
