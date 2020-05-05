from format import LogSettings

log = LogSettings()
log.debug_enabled()


class BidBouncer:
    def filter_bid_responses(input,valid_sites):
        valid_sitelist = valid_sites.get_list_of_all('domain')
        for raw_input in input:
            try:
                site_index = valid_sitelist.index(raw_input['site'])
                valid_ad_units = raw_input['units']
                for unit in raw_input['units']:
                    valid_sites.collection[site_index].set_ad_unit(unit)
                    log.message('Loaded ad unit ' + unit + ' for ' +  valid_sites.collection[site_index].domain)
                valid_bidders = valid_sites.collection[site_index].bidders
                for bid in raw_input['bids']:
                    if bid['bidder'] in valid_bidders:
                        try:
                            ad_unit_index = valid_ad_units.index(bid['unit'])
                            valid_sites.collection[site_index].ad_units[ad_unit_index].auction_manager.store_valid_bid(bid['bidder'],bid['bid'])
                        except:
                            log.warning('Ad Unit ' + bid['unit'] + ' not found for site ' + valid_sites.collection[site_index].domain + ' Ignoring response as invalid.')
                    else:
                        log.warning('Bidder ' + bid['bidder'] + ' not found for site ' + valid_sites.collection[site_index].domain + '. Ignoring response as invalid.')
            except:
                log.warning('Site ' + raw_input['site'] + ' not found. Ignoring all bids.')

class Bid:
    def __init__(self,bidder,bid_value):
        self.bidder = bidder
        self.bid_value = bid_value
        self.adjustment_factor = 0
        self.adjusted_bid = 0
    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)
