from time import sleep
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class BrowserClient():
    def __init__(self, browser: str = "Firefox", url: str = "https://sachsen.impfterminvergabe.de/civ.public/start.html?oe=00.00.IM&mode=cc&cc_key=IOAktion") -> None:
        self._browser = browser
        self._url = url
        self._first_search = True
        self._last_date = ""
    
    def start_browser(self) -> None:
        if self._browser == "Chrome":
            self._driver = webdriver.Chrome()
        elif self._browser == "Firefox":
            self._driver = webdriver.Firefox()
        else:
            raise Exception(f"Browser {self._browser} is not supported. || Der Browser {self._browser} wird nicht unterstützt.")
    
    def close_browser(self) -> None:
        self._driver.close()
    
    def login(self, username: str, password: str) -> None:
        if self._driver.current_url != self._url:
            self._driver.get(self._url)
        
        try:
            input_username = self._driver.find_element_by_id("gwt-uid-3")
            input_password = self._driver.find_element_by_id("gwt-uid-5")
            btn_login = self._driver.find_element_by_id("WorkflowButton-4212")

            input_username.send_keys(Keys.CONTROL + "a")
            input_username.send_keys(Keys.BACKSPACE)
            input_username.send_keys(username)
            input_password.send_keys(Keys.CONTROL + "a")
            input_password.send_keys(Keys.BACKSPACE)
            input_password.send_keys(password)
            btn_login.click()
            
            self._first_search = True
            self._last_date = ""
        except Exception:
            pass
        
    def is_logged_in(self) -> bool:
        ret = True
        try:
            self._driver.find_element_by_xpath("//div[@class='title'][text()='Aktionsauswahl']")
        except Exception:
            ret = False
        return ret
    
    def choose_action(self) -> None:
        try:
            radio_make_appointment = self._driver.find_element_by_xpath("(//span[contains(@class,'gwt-RadioButton col')])[1]")
            radio_make_appointment.click()
            btn_next = self._driver.find_element_by_xpath("//button[@class='right btn']")
            btn_next.click()
        except Exception:
            pass
    
    def is_at_choose_action(self) -> bool:
        ret = True
        try:
            self._driver.find_element_by_xpath("//label[text()='(1) Termin zur Coronaschutzimpfung vereinbaren oder ändern ']")
            ret = True
        except Exception:
            ret = False
        return ret

    def find_appointment(self, center: str, date: str, pref_day: str, day_time: str) -> None:
        date = datetime.strptime(date, "%d.%m.%Y").date()
        today = datetime.today().date()
        one_day = timedelta(days=1)
        if date - today < one_day:
            date = today + one_day
        date = datetime.strftime(date, "%d.%m.%Y")

        try:
            if date != self._last_date:
                # Enter date
                input_date = self._driver.find_element_by_class_name("gwt-DateBox")
                coordinates = input_date.location_once_scrolled_into_view
                self._driver.execute_script(f"window.scrollTo({coordinates['x']}, {coordinates['y']});")
                input_date.click()
                input_date.send_keys(Keys.CONTROL + "a")
                input_date.send_keys(Keys.BACKSPACE)
                input_date.send_keys(date)
                input_date.send_keys(Keys.ENTER)
                
                self._last_date = date
            
            if self._first_search:
                # Enter vaccination center
                input_center = self._driver.find_element_by_xpath("//span[@data-select2-id='2']")
                coordinates = input_center.location_once_scrolled_into_view
                self._driver.execute_script(f"window.scrollTo({coordinates['x']}, {coordinates['y']});")
                input_center.click()
                search_field = self._driver.find_element_by_class_name("select2-search__field")
                search_field.send_keys(Keys.CONTROL + "a")
                search_field.send_keys(Keys.BACKSPACE)
                search_field.send_keys(center)
                search_field.send_keys(Keys.ENTER)

                # Enter preferred day
                dropdown_day = self._driver.find_element_by_xpath("(//span[@role='textbox'])[2]")
                dropdown_day.click()
                self._driver.find_element_by_xpath(f"(//ul[@class='select2-results__options']//li)[{pref_day}]").click()
                
                # Enter preferred time
                dropdown_time = self._driver.find_element_by_xpath("(//span[@role='textbox'])[3]")
                coordinates = dropdown_time.location_once_scrolled_into_view
                self._driver.execute_script(f"window.scrollTo({coordinates['x']}, {coordinates['y']});")
                dropdown_time.click()
                self._driver.find_element_by_xpath(f"(//ul[@class='select2-results__options']//li)[{day_time}]").click()
                
                self._first_search = False

            self._driver.find_element_by_xpath("//button[@class='right btn']").click()
        except Exception:
            pass

    def is_at_find_appointment(self) -> bool:
        ret = False
        try:
            self._driver.find_element_by_xpath("//span[text()='Bitte geben Sie an, nach welchen Wünschen das System nach einem freien Termin suchen soll. ']")
            ret = True
        except Exception:
            pass
        return ret
    
    def is_no_appointment(self) -> bool:
        ret = False
        try:
            self._driver.find_element_by_xpath("//div[text()='Aufgrund der aktuellen Auslastung der Impfzentren und der verfügbaren Impfstoffmenge können wir Ihnen leider keinen Termin anbieten. Bitte versuchen Sie es in ein paar Tagen erneut.']")
            ret = True
        except Exception:
            pass
        return ret
    
    def go_back(self) -> None:
        try:
            self._driver.find_element_by_tag_name("button").click()
        except Exception:
            pass
    
    def maximize(self) -> None:
        try:
            self._driver.maximize_window()
            self._driver.switch_to.window(self._driver.current_window_handle) 
        except Exception:
            pass
    
    def is_at_appointment_result(self) -> bool:
        ret = False
        try:
            self._driver.find_element_by_xpath("//div[text()='Terminvergabe']")
            ret = True
        except Exception:
            pass
        return ret
