"""
:Date: 2017-02-17
:Version: 1.1
:Authors:
    - Marco Cieno
"""
import os
import time
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class Chromy(Chrome):
    """This class adds feautures to selenium.webdriver.Chrome."""

    def __init__(self, download_path=False, implicit_wait=0.1):
        """Create Chromy object and starts chromedriver.exe.

        Keyword arguments:
        download_path -- relative path to chromedriver.exe download folder (default False).
        implicit_wait -- implicit time wait for each operation (default 0.1).
        """
        co = ChromeOptions()
        co.add_argument('--log-level=3')
        co.add_argument('--disable-application-cache')
        co.add_argument('disable-infobars')
        if download_path is not False:
            if download_path is None:
                download_path = os.getcwd() + '\\downloads\\'
            if not os.path.exists(download_path):
                os.makedirs(download_path)
            co.add_experimental_option('prefs', {
                'plugins.plugins_list': [{
                    'enabled': False,
                    'name': 'Chrome PDF Viewer'
                    }],
                'download.default_directory': download_path,
                'download.extensions_to_open': ''
                })
        super().__init__(chrome_options=co)
        self.download_path = download_path
        self.implicit_wait = max(0, implicit_wait)
        self.rest()


    def click_element_by_xpath(self, xpath):
        """Click on the element with specified xpath.

        Positional arguments:
        xpath -- xpath representing the element to click.
        """
        try:
            self.find_element_by_xpath(xpath).click()
        except:
            return False
        self.rest()
        return True


    def click_element_by_link_text(self, link_text, new_tab=False):
        """Click on hyperlink by its text.

        Positional arguments:
        link_text -- text of the hyperlink to click.

        Keyword arguments:
        new_tab -- open the link in a new tab (default False).
        """
        try:
            if new_tab is True:
                self.new_tab()
                self.get(self.find_element_by_link_text(link_text).get_attribute('href'))
            else:
                self.find_element_by_link_text(link_text).click()
        except:
            return False
        self.rest()
        return True


    def click_element_by_class_name(self, class_name):
        """Click on element with specified class name.

        Positional arguments:
        class_name - class name of the element to click.
        """
        try:
            self.find_element_by_class_name(class_name).click()
        except:
            return False
        self.rest()
        return True


    def js_click_radio(self, value):
        """Safely click on radio buttons with JavaScript.

        Positional arguments:
        value -- value of radio button to click.
        """
        try:
            radio = self.find_element_by_xpath('//input[@type="radio" and @value="{}"]'.format(value))
            self.execute_script('arguments[0].click();', radio)
        except:
            return False
            self.rest()
            return True


    def send_keys_to_xpath(self, keys, xpath):
        """Send keys to element specified by xpath.

        Positional arguments:
        keys -- keys to be sent.
        xpath -- xpath representing the element.
        """
        try:
            self.find_element_by_xpath(xpath).send_keys(keys)
            self.press_esc()
        except:
            return False
        self.rest()
        return True


    def send_keys_to_link_text(self, keys, link_text):
        """Send keys to hyperlink by its text.

        Positional arguments:
        keys -- keys to be sent.
        link_text -- text of the hyperlink to click.
        """
        try:
            self.find_element_by_link_text(link_text).send_keys(keys)
            self.press_esc()
        except:
            return False
        self.rest()
        return True


    def send_keys_to_class_name(self, keys, class_name):
        """Send keys to element with specified class name.

        Positional arguments:
        keys -- keys to be sent.
        class_name -- class name of the element to click.
        """
        try:
            self.find_element_by_class_name(class_name).send_keys(keys)
            self.press_esc()
        except:
            return False
        self.rest()
        return True


    def accept_alert(self):
        """Accept alert pop up."""
        try:
            self.switch_to_alert().accept();
            self.rest()
        except:
            return False
        return True


    def dismiss_alert(self):
        """Dismiss alert pop up."""
        try:
            self.switch_to_alert().dismiss();
            self.rest()
        except:
            return False
        return True


    def rest(self, rest_time=0):
        """Freeze execution for at least self.implicit_wait seconds.

        Keyword arguments:
        rest_time -- time to freeze execution (default 0).
        """
        time.sleep(max(rest_time, self.implicit_wait))


    def switch_to_window(self, window):
        """Switch to another tab by its index or handle.

        Positional arguments:
        window -- index of desired window handle or window handle.
        """
        try:
            if isinstance(window, int):
                if window < 0 or window >= len(self.window_handles):
                    raise Exception()
                self.switch_to_window(self.window_handles[window])
            else:
                super().switch_to_window(window)
        except:
            return False
        self.rest()
        return True

    def new_tab(self, switch=True):
        """Open new window.

        Keyword arguments:
        switch -- set focus to newly opened tab.
        """
        try:
            wh_before = set(self.window_handles)
            self.execute_script('window.open("");')
            new_window = list(set(self.window_handles) - wh_before)
            if switch is True:
                self.switch_to_window(new_window[0])
        except:
            return False
        self.rest()
        return True


    def close_tab(self):
        """Close tab if at least 2 tabs exists and focus
        on previous tab, if any; on next tab otherwise.
        """
        try:
            if len(self.window_handles) > 1:
                current_window = sum(i for i, v in enumerate(self.window_handles) if v == self.current_window_handle)
                self.close()
                self.switch_to_window(max(0, current_window - 1))
                self.rest()
                return True
        except:
            pass
        return False


    def next_tab(self):
        """Switch to next tab, if any."""
        current_window = sum(i for i, v in enumerate(self.window_handles) if v == self.current_window_handle)
        return self.switch_to_window(current_window + 1)


    def prev_tab(self):
        """Switch to previous tab, if any."""
        current_window = sum(i for i, v in enumerate(self.window_handles) if v == self.current_window_handle)
        return self.switch_to_window(current_window - 1)


    def press_esc(self):
        """Simulate ESC keypress."""
        ActionChains(self).key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()

    def list_radios(include_disabled=False):
        """Create a list of all radio elements in the page.

        Keyword arguments:
        include_disabled -- include disabled radios in the list.
        """
        try:
            t = self.find_elements_by_xpath('//input[@type="radio"]')
        except:
            t = []
        return [x for x in t if include_disabled is True or x.is_enabled()]


    def list_tables(self):
        """Return a list of all tables in the page as pandas DataFrame."""
        try:
            t = pd.read_html(self.page_source)
        except:
            t = []
        return t
