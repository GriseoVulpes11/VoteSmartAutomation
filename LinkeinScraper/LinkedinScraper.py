from pandas import DataFrame
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time


class LN:
    def __init__(self):
        firefox_options = Options()
        firefox_options.headless = True
        self.driver = webdriver.Firefox(options=firefox_options,
                                        service=Service("C:\\Program Files (x86)\\geckodriver.exe"))
        print("Driver Started")
        with open("LinkeinScraper\\config.txt") as f:
            lines = f.readlines()
        self.email = lines[0]
        self.password = lines[1]

    def login(self):
        self.driver.get("https://www.linkedin.com/uas/login")
        time.sleep(.4)
        self.driver.find_element(By.ID, 'username').send_keys(self.email)
        self.driver.find_element(By.ID, 'password').send_keys(self.password)
        self.driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
        return True

    def scrape(self, link):
        if self.login():
            time.sleep(.4)
            self.driver.get(link)

            start = time.time()

            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                end = time.time()
                if round(end - start) > 10:
                    break
        else:
            print("Unable To Login")
        self.driver.quit
        return self.driver.page_source

    def soup(self, source):
        linkedin_soup = bs(source.encode("utf-8"), "html")
        linkedin_soup.prettify()

        candidate_name = linkedin_soup.find("div", {"id": "ember35"}).text
        raw_exp = linkedin_soup.find_all("span", {"class": "visually-hidden"})

        readable_exp = []
        for x in raw_exp:
            readable_exp.append(x.text)

        professional_exp_list, education_exp_list, licence_exp_list, vol_exp_list, org_exp_list = ([] for _ in range(5))
        add_to_prof, add_to_edu, add_to_licence, add_to_vol, add_to_org = False, False, False, False, False
        # don't worry
        # I hate this part too :(
        for i in readable_exp:
            if len(i) > 100:
                readable_exp.remove(i)
            if i == "Experience":
                add_to_prof = True
                add_to_edu = False
                add_to_licence = False
                add_to_vol = False
                add_to_org = False
            elif i == "Education":
                add_to_prof = False
                add_to_edu = True
                add_to_licence = False
                add_to_vol = False
                add_to_org = False
            elif i == "Licenses & certifications":
                add_to_prof = False
                add_to_edu = False
                add_to_licence = False
                add_to_vol = False
                add_to_org = False
            elif i == "Volunteering":
                add_to_prof = False
                add_to_edu = False
                add_to_licence = False
                add_to_vol = True
                add_to_org = False
            # Kill
            elif i == "Skills":
                add_to_prof = False
                add_to_edu = False
                add_to_licence = False
                add_to_vol = False
                add_to_org = False
            # Kill
            elif i == "Recommendations":
                add_to_prof = False
                add_to_edu = False
                add_to_licence = False
                add_to_vol = False
                add_to_org = False
            # Kill
            elif i == "Languages":
                add_to_prof = False
                add_to_edu = False
                add_to_licence = False
                add_to_vol = False
                add_to_org = False
            elif i == "Organizations":
                add_to_prof = False
                add_to_edu = False
                add_to_licence = False
                add_to_vol = False
                add_to_org = True
            elif i == "Interests":
                break
            if add_to_prof:
                professional_exp_list.append(i)

            if add_to_edu:
                education_exp_list.append(i)

            if add_to_licence:
                licence_exp_list.append(i)

            if add_to_vol:
                vol_exp_list.append(i)

            if add_to_org:
                org_exp_list.append(i)

        full_data = [professional_exp_list, education_exp_list,  vol_exp_list,
                     org_exp_list]
        max_length = max(map(len, full_data))
        for x in full_data:
            x.extend([None] * (max_length - len(x)))

        data = DataFrame({ 'Experience': full_data[0], 'Education': full_data[1],
                          'Volunteering': full_data[2], 'Organizations': full_data[3]})
        print(data)
        data.to_excel(f'LinkeinScraper\\CanidateData\\{candidate_name.strip()}.xlsx')


Link = LN()
link_input = input("Enter Link:")
source = Link.scrape(link_input)
Link.soup(source)
