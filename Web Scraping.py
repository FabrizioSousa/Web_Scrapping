
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

class PegarEmails:

    def __init__(self):
        self.TIME_SLEEP = 5
        self.PAGINAS_PASSADAS = 0
        self.LOC_EMAIL = 0
        self.array_email = []
        self.SITE_LINK = "https://acheumarquiteto.caubr.gov.br"
        self.SITE_MAP = {
                "buttons":{
                        "pesquisar":
                            {
                                "xpath": "/html/body/div[1]/form[1]/div/div[2]/div[2]/p[3]/button/div[1]/b"
                            },
                        "tabletr":
                            {
                                "xpath": "/html/body/div[2]/div/div[2]/table/tbody/tr[%%NUMBER%%]"
                            },                       
                        "botao_avancar":
                            {
                                "xpath": "/html/body/div[2]/div/div[2]/div[3]/span[5]"
                            },
                        "email":
                            {
                                "xpath": "/html/body/div[2]/div/div[2]/table/tbody/tr[18]/td/div/div[1]/div[1]/div[3]/span/a"
                            }
                    }
            }
        self.driver = webdriver.Chrome(ChromeDriverManager().install())    
        self.driver.maximize_window()
        
    
    def abrir_site(self):
        self.driver.get(self.SITE_LINK)         
        Site_scrap.clicar_pesquisar()
        time.sleep(self.TIME_SLEEP)
        
    def clicar_pesquisar(self):
        self.driver.find_element_by_xpath(self.SITE_MAP["buttons"]["pesquisar"]["xpath"]).click()
        time.sleep(10)
        self.PAGINAS_PASSADAS = self.PAGINAS_PASSADAS+1 
        print(str(self.PAGINAS_PASSADAS) + "º página(s)" )
        self.driver.execute_script("window.scrollBy(0,300)");
        Site_scrap.mudar_pagina()
        time.sleep(2)
        Site_scrap.abrir_tr()
        
        
    def mudar_pagina(self):
        self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        time.sleep(2)
        self.driver.find_element_by_xpath(self.SITE_MAP["buttons"]["botao_avancar"]["xpath"]).click()     
        time.sleep(10)
        self.PAGINAS_PASSADAS = self.PAGINAS_PASSADAS+1 
        print(str(self.PAGINAS_PASSADAS) + "º página(s)" )
        Site_scrap.abrir_tr()
        
    def abrir_tr(self):
        x=1
        try:
            while x<70:
                objeto = self.SITE_MAP["buttons"]["tabletr"]["xpath"].replace("%%NUMBER%%", str(x))
                self.driver.find_element_by_xpath(objeto).click()     
                time.sleep(1)
                try:                    
                    email = self.driver.find_element_by_partial_link_text("@")
                    self.array_email.append(email.get_attribute('innerHTML'))
                    self.LOC_EMAIL = self.LOC_EMAIL +1
                    time.sleep(1)
                    self.driver.find_element_by_xpath(objeto).click()
                    time.sleep(1)
                    # self.driver.execute_script("window.scrollBy(0,350)");
                    x = x+2
                except NoSuchElementException:
                    self.driver.find_element_by_xpath(objeto).click()
                    time.sleep(1)
                    self.driver.execute_script("window.scrollBy(0,300)");
                    x = x+2
            time.sleep(1)  
            self.df = pd.DataFrame({'email': self.array_email})
            self.df.head()
            Site_scrap.mudar_pagina()
        except NoSuchElementException:
            self.df = pd.DataFrame({'email': self.array_email})
            print(self.df)
            time.sleep(1)
            Site_scrap.mudar_pagina()
            
Site_scrap = PegarEmails()
Site_scrap.abrir_site()
# get_attribute('innerHTML')
# html = self.driver.page_source
# /html/body/div[2]/div/div[2]/table/tbody/tr[1]
# /html/body/div[2]/div/div[2]/table/tbody/tr[3]
