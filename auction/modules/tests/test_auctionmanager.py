import unittest

from auction_dynamics import AuctionManager
from settings import Bidder,Entity

class TestAuctionManager(unittest.TestCase):

    def test_store_bid_adds_to_bids_list(self):
        bid_data = {
            'bidder': 'test_bidder',
            'bid': 100
            }
        result = AuctionManager()
        result.store_bid(bid_data['bidder'],bid_data['bid'])
        self.assertEqual(len(result.bids),1)

    def test_calculate_adjusted_bid_positive(self):
        bid_data = {
            'bidder': 'test_bidder',
            'bid': 100
            }
        bidder_input = [{
            'name': 'test_bidder',
            'adjustment': 0.2500
            }]
        bidder_settings = Entity()
        bidder_settings.get_entities(bidder_input,['name','adjustment'],Bidder)
        result = AuctionManager()
        result.store_bid(bid_data['bidder'],bid_data['bid'])
        result.calculate_adjusted_bid(bidder_settings)
        self.assertEqual(result.bids[0].adjusted_bid, 125)

    def test_calculate_adjusted_bid_negative(self):
        bid_data = {
            'bidder': 'test_bidder',
            'bid': 100
            }
        bidder_input = [{
            'name': 'test_bidder',
            'adjustment': -0.2500
            }]
        bidder_settings = Entity()
        bidder_settings.get_entities(bidder_input,['name','adjustment'],Bidder)
        result = AuctionManager()
        result.store_bid(bid_data['bidder'],bid_data['bid'])
        result.calculate_adjusted_bid(bidder_settings)
        self.assertEqual(result.bids[0].adjusted_bid, 75)

    def test_calculate_adjustment_factor_bid_missing(self):
        bid_data = {
            'bidder': 'test_bidder',
            'bid': 100
            }
        bidder_input = [{
            'name': 'different_test_bidder',
            'adjustment': -0.2500
            }]
        bidder_settings = Entity()
        bidder_settings.get_entities(bidder_input,['name','adjustment'],Bidder)
        result = AuctionManager()
        result.store_bid(bid_data['bidder'],bid_data['bid'])
        result.calculate_adjusted_bid(bidder_settings)
        self.assertEqual(result.bids[0].adjusted_bid, 100)

    def test_calculate_adjustment_no_bids(self):
        bid_data = {}
        bidder_input = []
        bidder_settings = Entity()
        bidder_settings.get_entities(bidder_input,['name','adjustment'],Bidder)
        result = AuctionManager()
        result.calculate_adjusted_bid(bidder_settings)
        self.assertEqual(result.bids, [])

    def test_get_top_bid_no_adjustment(self):
        bid_data = [{
            'bidder': 'losing_bidder',
            'bid': 99,
            },
            {
            'bidder': 'winning_bidder',
            'bid': 100,
            }]
        bidder_input = [{
            'name': 'losing_bidder',
            'adjustment': 0
            },
            {
            'name': 'winning_bidder',
            'adjustment': 0
            }]
        bidder_settings = Entity()
        bidder_settings.get_entities(bidder_input,['name','adjustment'],Bidder)
        result = AuctionManager()
        for b in bid_data:
            result.store_bid(b['bidder'],b['bid'])
        result.get_top_bid()
        self.assertEqual(result.top_bid.bidder,'winning_bidder')

    def test_get_top_bid_with_adjustment(self):
        bid_data = [{
            'bidder': 'losing_bidder',
            'bid': 100,
            },
            {
            'bidder': 'winning_bidder',
            'bid': 100,
            }]
        bidder_input = [{
            'name': 'losing_bidder',
            'adjustment': 0
            },
            {
            'name': 'winning_bidder',
            'adjustment': 0.01
            }]
        bidder_settings = Entity()
        bidder_settings.get_entities(bidder_input,['name','adjustment'],Bidder)
        result = AuctionManager()
        for b in bid_data:
            result.store_bid(b['bidder'],b['bid'])
        result.calculate_adjusted_bid(bidder_settings)
        result.get_top_bid()
        self.assertEqual(result.top_bid.bidder,'winning_bidder')

    def test_get_top_bid_empty(self):
        bid_data = []
        bidder_input = [{
            'name': 'losing_bidder',
            'adjustment': 0
            },
            {
            'name': 'winning_bidder',
            'adjustment': 0.01
            }]
        bidder_settings = Entity()
        bidder_settings.get_entities(bidder_input,['name','adjustment'],Bidder)
        result = AuctionManager()
        for b in bid_data:
            result.store_bid(b['bidder'],b['bid'])
        result.calculate_adjusted_bid(bidder_settings)
        result.get_top_bid()
        self.assertEqual(result.top_bid,{})

    def test_get_top_bid_no_bidder_settings(self):
        bid_data = [{
            'bidder': 'losing_bidder',
            'bid': 99,
            },
            {
            'bidder': 'winning_bidder',
            'bid': 100,
            }]
        bidder_input = []
        bidder_settings = Entity()
        bidder_settings.get_entities(bidder_input,['name','adjustment'],Bidder)
        result = AuctionManager()
        for b in bid_data:
            result.store_bid(b['bidder'],b['bid'])
        result.calculate_adjusted_bid(bidder_settings)
        result.get_top_bid()
        self.assertEqual(result.top_bid.bidder,'winning_bidder')

if __name__ == '__main__':
    unittest.main()
