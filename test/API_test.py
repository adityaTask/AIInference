import pytest
from pages.API import Api
import unittest
from utilities.read_csv import getCSVData
from ddt import ddt,data,unpack
from utilities.read_config import config


@pytest.mark.usefixtures("one_time_setup")
@ddt
class Api_Test(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def class_setup(self,one_time_setup):
        self.api = Api(self.driver)

    @pytest.mark.run(order=1)
    def test_authorize(self):
        self.api.authorize()
        self.api.post_ready()

    @pytest.mark.run(order=2)
    @data(*getCSVData(config['files']['input_file']))
    #@data([['OEBLAP2SBEAWEZZZZ', 'Elbolet® , Generic Manufacturer , Class 3000 , Beveled End , ASTM A182 Grade F 304/F 304L', '5', '30'], ['BXEEABMBEAYYABFZ', 'Cross , ASME B16.9 , Beveled End , ASTM A403 Grade WP316/WP316L , Type W', '5', '30'], ['HLEAXCDFFAYKAANZ', 'Lateral , Crane® Resistoflex® Lined Flanged Fittings with Fitting Dimensions per ASME B16.5 , Class 150 , Flat-face flanged end , ASTM A395 housing x ASTM A395 flanges , PVDF (Polyvinylidene fluoride)', '5', '30'], ['BTEEABMBEACKABFZ', 'Tee , ASME B16.9 , Beveled End , ASTM A234 Grade WPB , Type W', '5', '30'], ['MNDJAP2AVAZGZZZZ', 'Tee , Generic Manufacturer , Swagelok® compression tubing end x Swagelok® compression tubing end x Female threaded end , 316 stainless steel (16 Cr-12 Ni-2 Mo)', '5', '30']])
    @unpack
    def test_api(self,cc,description,fetch_recommendations,no_of_recommendations,target_cc):
        self.api.read_target(str(config['files']['target_file']))
        result = self.api.export_file(cc =cc,description = description,fetch_recommendations=int(fetch_recommendations),
                             no_of_recommendations =int(no_of_recommendations),target_cc=target_cc)
        assert result