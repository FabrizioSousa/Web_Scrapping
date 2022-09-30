
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import sys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.select import Select


class PegarEmails:

    def __init__(self):
        self.TIME_SLEEP = 5
        self.PAGINAS_PASSADAS = 0
        self.array_email = []
        self.COMECO =7
        self.FILTRO_INDEX=2
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
                                "xpath": "/html/body/div[2]/div/div[2]/div[4]/span[5]"
                            },
                        "email":
                            {
                                "xpath": "/html/body/div[2]/div/div[2]/table/tbody/tr[18]/td/div/div[1]/div[1]/div[3]/span/a"
                            },
                        "filtro_dropdown":
                            {
                                "xpath": "/html/body/div[1]/form[1]/div/div[2]/div[2]/p[1]/select"
                            }
                    }
            }
        self.driver = webdriver.Chrome(ChromeDriverManager().install())    
        self.driver.maximize_window()
        

    def abrir_site(self):
        self.driver.get(self.SITE_LINK)         
        Site_scrap.filtrar_valor()
        time.sleep(self.TIME_SLEEP)
        
    def clicar_pesquisar(self):        
        self.driver.find_element_by_xpath(self.SITE_MAP["buttons"]["pesquisar"]["xpath"]).click()
        time.sleep(5)
        self.PAGINAS_PASSADAS = self.PAGINAS_PASSADAS+1 
        print(str(self.PAGINAS_PASSADAS) + "º página(s)" )        
        time.sleep(0.5)
        y=1
        while y<self.COMECO:
           Site_scrap.mudar_pagina(0) 
           y=y+1
        self.driver.execute_script("window.scrollBy(0,300)");
        time.sleep(0.5)
        Site_scrap.abrir_tr()
        
    def mudar_pagina(self, opcao):                      
        self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        time.sleep(0.5)        
        self.driver.find_element_by_xpath(self.SITE_MAP["buttons"]["botao_avancar"]["xpath"]).click()     
        self.PAGINAS_PASSADAS = self.PAGINAS_PASSADAS+1 
        print(str(self.PAGINAS_PASSADAS) + "º página(s)" )
        time.sleep(7)    
        self.driver.execute_script("window.scrollBy(0,-300)");
        time.sleep(1) 
        if opcao==1:     
                Site_scrap.abrir_tr()
         
        
    def abrir_tr(self):
        x=1
        try:
            while x<70:
                objeto = self.SITE_MAP["buttons"]["tabletr"]["xpath"].replace("%%NUMBER%%", str(x))
                self.driver.find_element_by_xpath(objeto).click()     
                time.sleep(0.5)
                try:                    
                    email = self.driver.find_element_by_partial_link_text("@").get_attribute('innerHTML')
                    self.array_email.append(email)
                    print(email)
                    time.sleep(1)
                    self.driver.find_element_by_xpath(objeto).click()
                    time.sleep(0.5)                    
                    # self.driver.execute_script("window.scrollBy(0,350)");
                    x = x+2
                except NoSuchElementException:
                    self.driver.find_element_by_xpath(objeto).click()
                    time.sleep(0.5)
                    self.driver.execute_script("window.scrollBy(0,150)");
                    x = x+2
            time.sleep(0.5)  
            self.df = pd.DataFrame({'email': self.array_email})
            self.df.to_csv("Csv_Emails.csv",mode='a', index=False)
            Site_scrap.mudar_pagina(1)
        except NoSuchElementException:
            self.df = pd.DataFrame({'email': self.array_email})
            self.df.to_csv("Csv_Emails.csv",mode='a', index=False)
            time.sleep(0.5)
            Site_scrap.mudar_pagina(1)
        except StaleElementReferenceException:
            z=0
              
    def filtrar_valor(self):        
        objeto_filtro = self.driver.find_element_by_xpath(self.SITE_MAP["buttons"]["filtro_dropdown"]["xpath"])
        dd = Select(objeto_filtro)
        dd.select_by_index(self.FILTRO_INDEX)
        time.sleep(0.5)
        Site_scrap.clicar_pesquisar()
            
Site_scrap = PegarEmails()
Site_scrap.abrir_site()
# get_attribute('innerHTML')
# html = self.driver.page_source
# /html/body/div[2]/div/div[2]/table/tbody/tr[1]
# /html/body/div[2]/div/div[2]/table/tbody/tr[3]
