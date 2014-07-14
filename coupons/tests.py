from django.test.testcases import TestCase
from coupons.models import Sheet

class CouponSheetTest(TestCase):
    fixtures = ('test_fixtures', )
    
    def setUp(self):
        self.sheet = Sheet.objects.get(pk=1) 
    
    def test_get_all_coupons(self):        
        self.assertEqual(5, len(self.sheet.get_all_coupons()))
    