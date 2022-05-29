from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import pyotp


class CoopNav:
    PROGRAMS = ('Computer Science', 'Data Science', 'Software Eng.', 'Maths')
    APP_SITE = r'https://uozone2.uottawa.ca/apps'
    PROFILE_DIR = rf'C:/Users/{os.getlogin()}/AppData/Local/Google/Chrome/CoopNav Data'
    PROFILE = 'Profile 99'
    EMAIL_ID = 'i0116'
    NEXT_ID = 'idSIButton9'
    PASSWORD_ID = 'i0118'
    MFA_ID = 'idTxtBx_SAOTCC_OTC'
    SAVED_ACCOUNTS = r'//*[@id="tilesHolder"]/div[1]/div/div[1]'
    STAY_SIGNED_IN = 'idSIButton9'
    NAVIGATOR = r'//*[@id="block-views-application-directory-application-directory-pane"]/section[1]/div/div[3]/ul/li[13]/article/section/h2/a'
    JOBS = r'//*[@id="ctl00_menuContainer_uxMenu"]/nav/ul/li[7]'
    POSTINGS = r'/html/body/div[1]/form/div[2]/div[2]/div/span/nav/ul/li[7]/div/ul/li[1]'
    PROGRAMS_ID = 'ctl00_mainContainer_uxTabs_ctl03_uxAdvSearchPanel_uxSearchProgramsId_uxAvailableText'
    RESULTS_ID = r'ctl00_mainContainer_uxTabs_ctl03_uxAdvSearchPanel_uxSearchProgramsId_uxAvailable'
    RESULT = r'//*[@id="ctl00_mainContainer_uxTabs_ctl03_uxAdvSearchPanel_uxSearchProgramsId_uxAvailable"]/'
    ARROW_ID = 'ctl00_mainContainer_uxTabs_ctl03_uxAdvSearchPanel_uxSearchProgramsId_uxAddItem'
    CHOSEN = r'//*[@id="ctl00_mainContainer_uxTabs_ctl03_uxAdvSearchPanel_uxSearchProgramsId_uxSelected"]/'
    SEARCH_ID = 'ctl00_mainContainer_uxTabs_ctl03_uxBasicSearch'
    ITEMS_ID = 'ctl00_mainContainer_uxTabs_ctl06_ctl00_ctl00_uxPgSz'
    ITEMS_2500 = r'//*[@id="ctl00_mainContainer_uxTabs_ctl06_ctl00_ctl00_uxPgSz"]/option[5]'
    
    def __init__(self):
        options = Options()
        options.add_argument(fr'--user-data-dir={CoopNav.PROFILE_DIR}')
        options.add_argument(fr'--profile-directory={CoopNav.PROFILE}')
        options.add_experimental_option('detach', True)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get(CoopNav.APP_SITE)
        
    def login(self):
        if self.driver.current_url != CoopNav.APP_SITE:
            found_saved_accounts = self.driver.find_elements(By.XPATH, CoopNav.SAVED_ACCOUNTS)
            if len(found_saved_accounts) > 0:
                self.wait.until(EC.visibility_of_element_located((By.XPATH, CoopNav.SAVED_ACCOUNT))).click()
            else:
                email_box = self.wait.until(EC.visibility_of_element_located((By.ID, CoopNav.EMAIL_ID)))
                email_box.send_keys(os.environ.get('UOTTAWA_EMAIL') + '\n')
                
            password_box = self.wait.until(EC.visibility_of_element_located((By.ID, CoopNav.PASSWORD_ID)))
            password_box.send_keys(os.environ.get('UOTTAWA_PASSWORD') + '\n')
            mfa_box = self.wait.until(EC.visibility_of_element_located((By.ID, CoopNav.MFA_ID)))
            mfa_box.send_keys(pyotp.TOTP(os.environ.get('UOTTAWA_MFA_SECRET')).now() + '\n')

            self.wait.until(EC.visibility_of_element_located((By.ID, CoopNav.STAY_SIGNED_IN))).click()

    def open_navigator(self):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, CoopNav.NAVIGATOR))).click()
        self.driver.switch_to.window(self.driver.window_handles[-1])

        actions = ActionChains(self.driver)
        jobs = self.wait.until(EC.visibility_of_element_located((By.XPATH, CoopNav.JOBS)))
        actions.move_to_element(jobs).click().perform()

        postings = self.wait.until(EC.visibility_of_element_located((By.XPATH, CoopNav.POSTINGS)))
        actions.move_to_element(postings).click().perform()

    def search_for_programs(self, *programs):
        for i, program in enumerate(programs):
            search = self.wait.until(EC.visibility_of_element_located((By.ID, CoopNav.PROGRAMS_ID)))
            search.clear()
            search.send_keys(program + '\n')
            time.sleep(1)

            sel = Select(self.wait.until(EC.presence_of_element_located((By.ID, CoopNav.RESULTS_ID))))

            for option in sel.options:
                option.click()

            self.wait.until(EC.element_to_be_clickable((By.ID, CoopNav.ARROW_ID))).click()

            self.wait.until(EC.visibility_of_element_located((By.XPATH, CoopNav.CHOSEN + f'option[{i+1}]')))
            self.wait.until(EC.presence_of_element_located((By.XPATH, CoopNav.CHOSEN + f'option[{i+1}]')))

        self.wait.until(EC.element_to_be_clickable((By.ID, CoopNav.SEARCH_ID))).click()

    def show_all_items(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, CoopNav.ITEMS_ID))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, CoopNav.ITEMS_2500))).click()

def main():        
    cv = CoopNav()
    cv.login()    
    cv.open_navigator()
    cv.search_for_programs(*CoopNav.PROGRAMS)
    cv.show_all_items()


if __name__ == '__main__':
    main()
    #pass
