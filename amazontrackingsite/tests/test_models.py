from django.test import TestCase
from amazontrackingsite.models import *

# Create your tests here.

class AmazonPageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        url = "https://www.amazon.fr/dp/B0B81LNQ2M/ref=s9_acsd_hps_bw_c2_x_5_i?pf_rd_m=A1X6FK5RDHNB96&pf_rd_s=merchandised-search-2&pf_rd_r=0YSDJNWBMEKQTJ0DMFR1&pf_rd_t=101&pf_rd_p=c9c4aed1-2935-4658-853c-5be99a4fddde&pf_rd_i=301132"
        AmazonPage.objects.create(url=url, product_name='Amazon.fr - Le soleil pour étoile - MAZEL, Den - Livres')

    def test_url_label(self):
        amazon_page = AmazonPage.objects.get(id=1)
        field_label = amazon_page._meta.get_field('url').verbose_name
        self.assertEquals(field_label, 'url')

    def test_product_name_label(self):
        amazon_page = AmazonPage.objects.get(id=1)
        field_label = amazon_page._meta.get_field('product_name').verbose_name
        self.assertEquals(field_label, 'product name')

    # def test_object_name_is_last_name_comma_first_name(self):
    #     author = Author.objects.get(id=1)
    #     expected_object_name = f'{author.last_name}, {author.first_name}'
    #     self.assertEquals(expected_object_name, str(author))

    # def test_get_absolute_url(self):
    #     amazon_page = AmazonPage.objects.get(id=1)
    #     # This will also fail if the urlconf is not defined.
    #     self.assertEquals(amazon_page.get_absolute_url(), '/catalog/author/1')
