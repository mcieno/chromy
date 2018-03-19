import os
import time
import pandas as pd
import logging
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.WARNING)


class Chromy(Chrome):
    """Extend selenium.webdriver.Chrome feautures."""

    def __init__(self, download_path=False, implicit_wait=0.1):
        """Create Chromy and start chromedriver.exe.

        Args:
            download_path: Relative path to chromedriver.exe download folder
                (default False).
            implicit_wait: Implicit time, in seconds, wait after each operation
                (default 0.1).
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
        self.implicit_wait = max(.0, implicit_wait)
        self.rest()

    def click_element_by_xpath(self, xpath):
        """Click on the element with specified XPATH.

        Args:
            xpath: XPATH representing the element to click.
        """
        self.find_element_by_xpath(xpath).click()
        self.rest()

    def click_element_by_link_text(self, link_text, new_tab=False):
        """Click on hyperlink by its text.

        Args:
            link_text: Text of the hyperlink to click.
            new_tab: If True open the link in a new tab (default False).
        """
        if new_tab is True:
            href = self.find_element_by_link_text(link_text)\
                .get_attribute('href')
            self.new_tab()
            self.get(href)
        else:
            self.find_element_by_link_text(link_text).click()
        self.rest()

    def click_element_by_class_name(self, class_name):
        """Click on element with specified class name.

        Args:
            class_name: Class name of the element to click.
        """
        self.find_element_by_class_name(class_name).click()
        self.rest()

    def js_click_radio(self, value):
        """Safely click on radio buttons with JavaScript.

        Args:
            value: Value of radio button to click.
        """
        radio = self.find_element_by_xpath(
            '//input[@type="radio" and @value="{}"]'.format(value)
        )
        self.execute_script('arguments[0].click();', radio)
        self.rest()

    def send_keys_to_xpath(self, keys, xpath, escape=True):
        """Send keys to element specified by XPATH.

        Args:
            keys: Keys to be sent.
            xpath: XPATH representing the element.
            escape: If True press ESCAPE after sending keys (default True).
        """
        self.find_element_by_xpath(xpath).send_keys(keys)
        if escape is True:
            self.press_escape()
        self.rest()

    def send_keys_to_link_text(self, keys, link_text, escape=True):
        """Send keys to hyperlink by its text.

        Args:
            keys: Keys to be sent.
            link_text: Text of the hyperlink to click.
            escape: If True press ESCAPE after sending keys (default True).
        """
        self.find_element_by_link_text(link_text).send_keys(keys)
        if escape is True:
            self.press_escape()
        self.rest()

    def send_keys_to_class_name(self, keys, class_name, escape=True):
        """Send keys to element with specified class name.

        Args:
            keys: Keys to be sent.
            class_name: Class name of the element to click.
            escape: If True press ESCAPE after sending keys (default True).
        """
        self.find_element_by_class_name(class_name).send_keys(keys)
        if escape is True:
            self.press_escape()
        self.rest()

    def accept_alert(self):
        """Accept alert pop up.

        Returns:
            True on success, False on fail.
        """
        try:
            self.switch_to.alert.accept()
            self.rest()
        except NoAlertPresentException:
            return False
        return True

    def dismiss_alert(self):
        """Dismiss alert pop up.

        Returns:
            True on success, False on fail.
        """
        try:
            self.switch_to.alert.dismiss()
            self.rest()
        except NoAlertPresentException:
            return False
        return True

    def switch_to_window(self, window):
        """Switch to another tab by its index or handle.

        Args:
            window: Index of desired window handle or window handle name.

        Returns:
            True on success, False on fail.
        """
        try:
            if isinstance(window, int):
                if window < 0 or window >= len(self.window_handles):
                    return False
                self.switch_to.window(self.window_handles[window])
            else:
                super().switch_to.window(window)
        except NoSuchWindowException:
            return False
        self.rest()
        return True

    def new_tab(self, switch=True):
        """Open new window.

        Args:
            switch: If True set focus to newly opened tab (default True).

        Returns:
            True on success, False on fail.
        """
        try:
            wh_before = set(self.window_handles)
            self.execute_script('window.open("");')
            new_window = list(set(self.window_handles) - wh_before)
            if switch is True:
                self.switch_to_window(new_window[0])
        except NoSuchWindowException:
            return False
        self.rest()
        return True

    def close_tab(self):
        """Close tab if at least 2 tabs exists and focus
        on previous tab, if any; on next tab otherwise.

        Returns:
            True on success, False on fail.
        """
        try:
            if len(self.window_handles) > 1:
                current_window = self.window_handles.index(
                    self.current_window_handle
                )
                self.close()
                self.switch_to_window(max(0, current_window - 1))
                self.rest()
                return True
        except NoSuchWindowException:
            return False
        self.rest()
        return True

    def next_tab(self):
        """Switch to next tab, if any.

        Returns:
            True on success, False on fail.
        """
        current_window = self.window_handles.index(
            self.current_window_handle
        )
        return self.switch_to_window(current_window + 1)

    def prev_tab(self):
        """Switch to previous tab, if any.

        Returns:
            True on success, False on fail.
        """
        current_window = self.window_handles.index(
            self.current_window_handle
        )
        return self.switch_to_window(current_window - 1)

    def press_escape(self):
        """Simulate ESCAPE keypress."""
        ActionChains(self).key_down(Keys.ESCAPE).key_up(Keys.ESCAPE).perform()

    def list_radios(self, include_disabled=False):
        """Create a list of all radio elements in the page.

        Args:
            include_disabled: If True include disabled radios in the list (default
                False).

        Returns:
            A list of radio elements.
        """
        t = self.find_elements_by_xpath('//input[@type="radio"]')
        return [x for x in t if include_disabled is True or x.is_enabled()]

    def list_tables(self):
        """Create a list all the tables in the page.

        Returns:
            A list of all tables in the page as pandas DataFrame objects.
        """
        try:
            t = pd.read_html(self.page_source)
        except ValueError:
            t = []
        return t

    def rest(self, rest_time=.1):
        """Freeze execution for at least self.implicit_wait seconds.

        Args:
            rest_time: time to freeze execution (default 0.1).
        """
        time.sleep(max(rest_time, self.implicit_wait))
