import json
import os
import settings
import response
import auction_dynamics
import adunit

from format import PrintLog as log

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

def return_valid_sites(config):
    sitelist = []
    for site in config['sites']:
        s = settings.Site(site['name'],site['bidders'],site['floor'])
        if DEBUG:
            log.message('Loaded config for ' + s.domain + '. Site floor = ' + str(site['floor']))
        sitelist.append(s)
    return sitelist

def return_valid_bidders(config):
    bidderlist = []
    for bidder in config['bidders']:
        b = settings.Bidder(bidder['name'],bidder['adjustment'])
        if DEBUG:
            log.message('Loaded bidder settings for ' + b.name)
        bidderlist.append(b)
    return bidderlist

def find(list, key, value):
    for i, d in enumerate(list):
        if d[key] == value:
            return i
    return -1

def validate_input_and_store_bids(input,valid_sites,sorted_bidder_list):
    for i in input:
        for site in valid_sites:
            if i['site'] == site.domain:
                for u in i['units']:
                    site.set_ad_unit(u)
                    if DEBUG:
                        log.message('Loaded ad unit ' + u + ' for ' + site.domain )

                sorted_raw_bids = sorted(i['bids'], key=lambda k: (k['bidder'], k['unit']))

                bid_count = 0
                for raw_bid in sorted_raw_bids:
                    bid_count += 1
                    bidder_index = find(sorted_bidder_list,'name',raw_bid['bidder'])
                    if bidder_index == -1:
                        if DEBUG:
                            log.warning('Bidder ' + raw_bid['bidder'] + ' not found for site ' + site.domain + '. Ignoring response as invalid.')
                        break
                    else:
                        if bidder_index > 0:
                            if DEBUG:
                                j = 0
                                if bid_count != 1:
                                    j = 1
                                while j < bidder_index:
                                    log.warning('Bidder ' + sorted_bidder_list[j].name + ' had no bids for site ' + site.domain + '.')
                                    j += 1
                            del sorted_bidder_list[0:bidder_index-1]
                        raw_bid['adjustment_factor'] = sorted_bidder_list[0].adjustment

                        if raw_bid['unit'] in i['units']:
                            for ad_unit in site.ad_units:
                                if ad_unit.name == raw_bid['unit']:
                                    ad_unit.auction_manager.store_valid_bid(raw_bid['bidder'],raw_bid['bid'],raw_bid['adjustment_factor'])
                                    if DEBUG:
                                        log.message('Bidder response for ' + raw_bid['unit'] + ': ' + str(raw_bid['bid']) + ' from ' + raw_bid['bidder'] + ' (bid adjustment of ' + str(raw_bid['adjustment_factor']) + ')' )
                        else:
                            if DEBUG:
                                log.warning('Ad Unit ' + b['unit'] + ' not found. Ignoring response as invalid.')

def hold_auctions(all_possible_auctions):
    auction_output = []
    for site in all_possible_auctions:
        for ad in site.ad_units:
            if DEBUG:
                log.message('Holding auction for ' + ad.name + ' in ' + site.domain)
            ad.auction_manager.get_top_bid()
        site.get_winning_bids_above_site_floor()
        log.announcement('Auction is complete!')
        auction_output.append(site.won_bids)
    return auction_output


if (__name__ == '__main__'):
    import sys

    if '--debug' in sys.argv:
        DEBUG = True
    else:
        DEBUG = False

    current_directory = os.getcwd()


    # Load json libraries
    config = load_config_library(current_directory+'auction/config.json')
    input = load_input_library()

    # Create known list of sites, bidders
    known_site_entities = return_valid_sites(config)
    known_bidders = return_valid_bidders(config)
    known_bidders_sorted = sorted(known_bidders, key=lambda k: k['name'])

    # Filter input against known sites, bidders and ad units
    validate_input_and_store_bids(input,known_site_entities,known_bidders_sorted)

    # Hold the auction and get winners
    auction_output = hold_auctions(known_site_entities)

    # Print auction output
    print(auction_output)
