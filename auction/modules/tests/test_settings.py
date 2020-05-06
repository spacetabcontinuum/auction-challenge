import unittest

from settings import Site,Entity

class TestSite(unittest.TestCase):

    def test_set_ad_units_to_site(self):
        result = Site('test.com','test-bidder',0)
        result.set_ad_unit('test-ad-unit')
        self.assertEqual(result.ad_units[0].name,'test-ad-unit')

    def test_get_winning_bids_above_floor_no_floor(self):
        bidder_settings = Entity()
        result = Site('test.com','test-bidder',0)
        result.set_ad_unit('test-ad-unit')
        result.ad_units[0].auction_manager.store_bid('test-bidder',100)
        result.ad_units[0].auction_manager.calculate_adjusted_bid(bidder_settings)
        result.ad_units[0].auction_manager.get_top_bid()
        result.get_winning_bids_above_site_floor()
        result_bool = False
        if result.winning_bids[0]:
            result_bool = True
        self.assertEqual(result_bool,True)

    def test_get_winning_bids_above_floor_with_floor(self):
        bidder_settings = Entity()
        result = Site('test.com','test-bidder',110)
        result.set_ad_unit('test-ad-unit')
        result.ad_units[0].auction_manager.store_bid('test-bidder',100)
        result.ad_units[0].auction_manager.calculate_adjusted_bid(bidder_settings)
        result.ad_units[0].auction_manager.get_top_bid()
        result.get_winning_bids_above_site_floor()
        result_bool = False
        if result.winning_bids[0]:
            result_bool = True
        self.assertEqual(result_bool,False)

    def test_get_winning_bids_above_floor_no_top_bid(self):
        bidder_settings = Entity()
        result = Site('test.com','test-bidder',110)
        result.set_ad_unit('test-ad-unit')
        result.ad_units[0].auction_manager.calculate_adjusted_bid(bidder_settings)
        result.ad_units[0].auction_manager.get_top_bid()
        result.get_winning_bids_above_site_floor()
        result_bool = False
        if result.winning_bids[0]:
            result_bool = True
        self.assertEqual(result_bool,False)

if __name__ == '__main__':
    unittest.main()
