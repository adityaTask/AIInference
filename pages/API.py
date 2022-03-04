import os
import pandas as pd
from base.selenium_driver import SeleniumDriver
import time
import json
from bs4 import BeautifulSoup
import re
from utilities.oracle_db import connect_query
from utilities.read_config import config



class Api(SeleniumDriver):
    target_desc = []
    source_desc = []
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver

    _authorize = "//span[text()='Authorize']"
    _value = "//input[@type='text']"
    _submit = "//button[@type='submit']"
    _close = '//button[@class="btn modal-btn auth btn-done button"]'

    _post = "//div[@class='opblock-summary-description' and contains(text(),'Predict')]"
    _try_it_out = "//button[@class='btn try-out__btn']"

    _body = "//*[@class='body-param__text']"
    _execute = "//*[@class='btn execute opblock-control__btn']"

    _response = "//pre[@class=' microlight']"

    def authorize(self):
        self.element_click(locator=self._authorize,locator_type="xpath")
        self.send_keys(data=123,locator=self._value,locator_type="xpath")
        self.element_click(locator=self._submit,locator_type="xpath")
        self.element_click(locator=self._close,locator_type="xpath")

    def post_ready(self):
        self.element_click(locator=self._post, locator_type="xpath")
        self.element_click(locator=self._try_it_out, locator_type="xpath")

    def create_json(self,cc,description,no_of_recommendations = 30):
        self.read_source(config['files']['source_file'])
        index =0
        hierarchy=[]
        for i in self.source_desc:
            if i['Label'] == str(cc):
                hierarchy.append(i['Hierarchy_1'])
                hierarchy.append(i['Hierarchy_2'])
                hierarchy.append(i['Hierarchy_3'])
                break
        description_list = [x for x in description.split(",")]
        json_attribute = {"Attributes":description_list,"NumberOfRecommendations":no_of_recommendations,
                          "SourceAnnotation":hierarchy}
        json_dict = {"Requests":[json_attribute]}
        #print(json.dumps(json_dict))
        return json.dumps(json_dict)

    def get_response(self):
        response = self.get_element(locator=self._response,locator_type="xpath").get_attribute('innerHTML')
        soup = BeautifulSoup(response, features="html.parser")
        for script in soup(["script"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ''.join(chunk for chunk in chunks if chunk)
        index_list = re.findall('"Index": \d*,',text)
        index_list = [int(i[9:-1]) for i in index_list]
        conf_list = re.findall('"Confidence": \d.\d*}' ,text)
        conf_list = [i[14:-1] for i in conf_list]
        return (index_list,conf_list)

    def read_target(self, target_file):
        f = open(target_file)
        source_json = json.load(f)
        description_list = []
        for i in source_json:
            description_list.append(i)
        self.target_desc  =  description_list

    def read_source(self, source_file):
        f = open(source_file)
        source_json = json.load(f)
        description_list = []
        for i in source_json:
            description_list.append(i)
        self.source_desc  =  description_list

    def execute(self,cc,description,no_of_recommendations = 30):
        content = self.create_json(cc,description,no_of_recommendations)
        self.clear(locator=self._body, locator_type="xpath")
        self.send_keys(data=content, locator=self._body, locator_type="xpath")
        time.sleep(1)
        self.element_click(locator=self._execute,locator_type="xpath")
        return content

    def get_cc_list(self,fetch_recommendations):
        index_list , con_list = self.get_response()
        if len(index_list) < fetch_recommendations:
            fetch_recommendations = len(index_list)
        target_cc_list = []
        target_desc_list = []
        for i in index_list[:fetch_recommendations]:
            target_cc_list.append(self.target_desc[i]['Label'])
        for i in index_list[:fetch_recommendations]:
            target_desc_list.append(self.target_desc[i]['Description'])
        return index_list,con_list ,target_cc_list, target_desc_list

    def export_file(self,cc,description,fetch_recommendations,no_of_recommendations,target_cc):
        expected_rec = False
        content = self.execute(cc,description,no_of_recommendations)
        time.sleep(1)
        index_list, con_list, target_cc_list, target_desc_list = self.get_cc_list(fetch_recommendations)
        source_cc_list = [cc] * fetch_recommendations
        source_desc_list = [description] * fetch_recommendations
        input_query = [content] * fetch_recommendations
        target_cc_code = []
        for i in target_cc_list:
            target_cc_code.append(connect_query(connection_string=str(config['db']['DB_USER_PW'])+'@'+str(config['db']['DB_NAME']),
                                      sql_query='select commodity_code from M_COMMODITY_CODES where COMMODITY_ID = {0}'.format(int(i))))
        target_cc_code = [i[0][0] for i in target_cc_code]
        if target_cc in target_cc_code:
            expected_rec= True
        if expected_rec:
            exported_file_name = config['files']['export_file']
        else:
            exported_file_name = config['files']['errors_file']
        df = pd.DataFrame(list(zip(source_cc_list,source_desc_list,input_query,index_list, con_list, target_cc_list, target_cc_code, target_desc_list)),
                          columns = ['source_cc_','source_desc','input_query','index','confidence', 'target_cc_id','target_cc_code' ,'target_desc'])
        df.to_csv(exported_file_name,index = False,mode='a')
        return expected_rec











# wd = WebDriver()
# api =Api(wd.web_driver_instance())
# api.read_source("D:\\AIEXE\\source.json")
# api.authorize()
# api.post_ready()
# #api.create_json('BBPTAM9BEAMUABJZ','Butt-Weld Pipet', 'MSS SP-97', 'BE', 'ASTM B493 Grade R60702 (UNS R60702)', 'annealed',30)
# api.export_file('BXEEABMBEAYYABFZ',"Cross , ASME B16.9 , Beveled End , ASTM A403 Grade WP316/WP316L , Type W",5,30)

