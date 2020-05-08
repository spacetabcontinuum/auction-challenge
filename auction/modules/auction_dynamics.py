import json
import response
from format import LogSettings

log = LogSettings()
log.debug_enabled()

class AuctionManager:
    def __init__(self):
        self.bids = []
        self.top_bid = {}
        self.hold_auction = False
    def store_bid(self,bidder,bid_value):
        self.bids.append(response.Bid(bidder,bid_value))
        self.hold_auction = True
    def calculate_adjusted_bid(self,bidder_settings):
        if not self.hold_auction:
            return
        bidderlist = bidder_settings.get_list_of_all('name')
        if len(bidderlist) == 0:
            log.message('No bidder adjustments required.')
            return
        for b in self.bids:
            try:
                bidder_index = bidderlist.index(b['bidder'])
                b.adjustment_factor = bidder_settings.collection[bidder_index]['adjustment']
                b.adjusted_bid = b.bid_value * (1.0000 + b.adjustment_factor)
                log.message('Adjusted bid of ' + str(b.bid_value) + ' from ' + b.bidder + ' by ' + str(b.adjustment_factor*100) + '%. Competed in auction as ' + str(b.adjusted_bid))
            except:
                log.message('Could not find bidder adjustment value for ' + b['bidder'] + '. Assuming no adjustment factor necessary (adjusted bid = orignal bid).')
    def get_top_bid(self):
        if not self.hold_auction:
            log.warning('No participating bids.')
            return
        participating_bids = self.bids
        top_adjusted_bid_value = 0
        top_bid = {}
        for b in participating_bids:
            if b.adjusted_bid == top_adjusted_bid_value:
                log.message('Bid from ' + b.bidder + ' for ' + str(b.adjusted_bid) + ' matches a previous bid from ' + top_bid.bidder + '. Ignoring the late bid.')
            elif b.adjusted_bid >= top_adjusted_bid_value:
                top_adjusted_bid_value = b.adjusted_bid
                top_bid = b
        self.top_bid = top_bid
        log.message('Top bid is: ' + str(self.top_bid))

def hold_the_auction(site_settings,bidder_settings):
    auction_output = []
    for site in site_settings:
        for ad in site.ad_units:
            log.message('Holding auction for ' + ad.name + ' in ' + site.domain)
            ad.auction_manager.calculate_adjusted_bid(bidder_settings)
            ad.auction_manager.get_top_bid()
        site.get_winning_bids_above_site_floor()
        auction_output.append(site.winning_bids)
        log.message('We have winners for site ' + site.domain + ': ' + str(site.winning_bids))
    log.announcement('Auction is complete!')
    auction_output_json = json.dumps(auction_output)
    return auction_output_json
