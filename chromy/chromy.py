# -*- coding: utf-8 -*-
import os
import pandas
import sys
import time

from selenium.common.exceptions import *
from selenium.webdriver import *
from selenium.webdriver.common.action_chains import *
from selenium.webdriver.common.by import *
from selenium.webdriver.common.keys import *
from selenium.webdriver.support import *
from selenium.webdriver.support.expected_conditions import *
from selenium.webdriver.support.ui import *


class Chromy(Chrome):
    """A better selenium.webdriver.Chrome to waste less time."""

    def __init__(self, *args, **kwargs):
        """Create Chromy and start chromedriver.exe.

        Args:
            download_path: Relative path to chromedriver.exe download folder (default False).
            rest_between: Implicit time, in seconds, wait after each operation (default 0.1).
        """
        if 'download_path' in kwargs.keys():
            download_path = kwargs['download_path']
            del kwargs['download_path']
        else:
            download_path = False

        if 'implicitly_wait' in kwargs.keys():
            implicitly_wait = kwargs['implicitly_wait']
            del kwargs['implicitly_wait']

        if 'chrome_options' not in kwargs.keys():
            co = ChromeOptions()
            
            co.add_argument('--log-level=3')
            co.add_argument('--disable-application-cache')
            co.add_argument('disable-infobars')
            
            if download_path is not False:
                if download_path is None:
                    download_path = os.getcwd() + '/downloads/'
                if not os.path.exists(download_path):
                    os.makedirs(download_path)

                co.add_experimental_option('prefs', {
                    'plugins.plugins_list': [{
                        'enabled': False,
                        'name': 'Chrome PDF Viewer'}],
                    'download.default_directory': download_path,
                    'download.extensions_to_open': ''})

            kwargs['chrome_options'] = co
        
        super().__init__(*args, **kwargs)

        self.implicitly_wait(implicitly_wait)

    def click_element_by_id(self, id):
        """Click on the element with specified ID.

        Args:
            id: ID of the element to click.
        """
        self.find_element_by_id(id).click()

    def click_element_by_name(self, name):
        """Click on the element with specified name.

        Args:
            name: Name of the element to click.
        """
        self.find_element_by_name(name).click()

    def click_element_by_xpath(self, xpath):
        """Click on the element with specified XPATH.

        Args:
            xpath: XPATH representing the element to click.
        """
        self.find_element_by_xpath(xpath).click()
        
    def click_element_by_link_text(self, link_text, new_tab=False):
        """Click on hyperlink by its text.

        Args:
            link_text: Text of the hyperlink to click.
            new_tab: If True open the link in a new tab (default False).
        """
        e = self.find_element_by_link_text(link_text)
        if new_tab:
            href = e.get_attribute('href')
            self.new_tab()
            self.get(href)
        else:
            e.click()

    def click_element_by_partial_link_text(self, partial_link_text, new_tab=False):
        """Click on hyperlink by its text.

        Args:
            link_text: Text of the hyperlink to click.
            new_tab: If True open the link in a new tab (default False).
        """
        e = self.find_element_by_partial_link_text(partial_link_text)
        if new_tab:
            href = e.get_attribute('href')
            self.new_tab()
            self.get(href)
        else:
            e.click()
        
    def click_element_by_tag_name(self, tag_name):
        """Click on element with specified tag name.

        Args:
            tag_name: Tag name of the element to click.
        """
        self.find_element_by_tag_name(tag_name).click()

    def click_element_by_class_name(self, class_name):
        """Click on element with specified class name.

        Args:
            class_name: Class name of the element to click.
        """
        self.find_element_by_class_name(class_name).click()

    def click_element_by_css_selector(self, css_selector):
        """Click on element with specified CSS selector.

        Args:
            css_selector: CSS selector of the element to click.
        """
        self.find_element_by_css_selector(css_selector).click()

    def send_keys_to_id(self, keys, id, escape=True):
        """Send keys to element specified by ID.

        Args:
            keys: Keys to be sent.
            id: ID of the element.
            escape: If True press ESCAPE after sending keys. This is useful to avoid form autocompletion popups which may interfere with upcoming webdriver events (default True).
        """
        self.find_element_by_id(id).send_keys(keys)
        
        if escape is True:
            self.press_escape()

    def send_keys_to_name(self, keys, name, escape=True):
        """Send keys to element specified by Name.

        Args:
            keys: Keys to be sent.
            name: Name of the element.
            escape: If True press ESCAPE after sending keys. This is useful to avoid form autocompletion popups which may interfere with upcoming webdriver events (default True).
        """
        self.find_element_by_name(name).send_keys(keys)
        
        if escape is True:
            self.press_escape()

    def send_keys_to_xpath(self, keys, xpath, escape=True):
        """Send keys to element specified by XPATH.

        Args:
            keys: Keys to be sent.
            xpath: XPATH of the element.
            escape: If True press ESCAPE after sending keys. This is useful to avoid form autocompletion popups which may interfere with upcoming webdriver events (default True).
        """
        self.find_element_by_xpath(xpath).send_keys(keys)
        
        if escape is True:
            self.press_escape()
        
    def send_keys_to_link_text(self, keys, link_text, escape=True):
        """Send keys to hyperlink by its text.

        Args:
            keys: Keys to be sent.
            link_text: Text of the hyperlink.
            escape: If True press ESCAPE after sending keys (default True).
        """
        self.find_element_by_link_text(link_text).send_keys(keys)

        if escape is True:
            self.press_escape()

    def send_keys_to_partial_link_text(self, keys, partial_link_text, escape=True):
        """Send keys to hyperlink by partial link text.

        Args:
            keys: Keys to be sent.
            partial_link_text: Partial text of the hyperlink.
            escape: If True press ESCAPE after sending keys (default True).
        """
        self.find_element_by_link_text(partial_link_text).send_keys(keys)

        if escape is True:
            self.press_escape()
    
    def send_keys_to_tag_name(self, keys, tag_name, escape=True):
        """Send keys to element with specified tag name.

        Args:
            keys: Keys to be sent.
            tag_name: Tag name of the element.
            escape: If True press ESCAPE after sending keys (default True).
        """
        self.find_element_by_tag_name(tag_name).send_keys(keys)

        if escape is True:
            self.press_escape()

    def send_keys_to_class_name(self, keys, class_name, escape=True):
        """Send keys to element with specified class name.

        Args:
            keys: Keys to be sent.
            class_name: Class name of the element.
            escape: If True press ESCAPE after sending keys (default True).
        """
        self.find_element_by_class_name(class_name).send_keys(keys)

        if escape is True:
            self.press_escape()

    def send_keys_to_css_selector(self, keys, css_selector, escape=True):
        """Send keys to element with specified CSS selector.

        Args:
            keys: Keys to be sent.
            css_selector: CSS selector of the element.
            escape: If True press ESCAPE after sending keys (default True).
        """
        self.find_element_by_class_name(css_selector).send_keys(keys)

        if escape is True:
            self.press_escape()

    def accept_alert(self):
        """Accept alert pop up.

        Returns:
            True on success, False on fail.
        """
        try:
            self.switch_to.alert.accept()
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
        return True

    def new_tab(self, switch=True):
        """Open new tab in current window.

        Args:
            switch: If True change focus to newly opened tab (default True).

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
        return True

    def close_tab(self):
        """Close tab if at least 2 tabs exists and focus on previous tab, if any; on next tab otherwise.

        Returns:
            True on success, False on fail.
        """
        try:
            if len(self.window_handles) > 1:
                current_window = self.window_handles.index(self.current_window_handle)
                self.close()
                self.switch_to_window(max(0, current_window - 1))
                return True
        except NoSuchWindowException:
            return False

    def next_tab(self):
        """Switch to next tab, if any.

        Returns:
            True on success, False on fail.
        """
        current_window = self.window_handles.index(self.current_window_handle)
        return self.switch_to_window(current_window + 1)

    def prev_tab(self):
        """Switch to previous tab, if any.

        Returns:
            True on success, False on fail.
        """
        current_window = self.window_handles.index(self.current_window_handle)
        return self.switch_to_window(current_window - 1)

    def list_radios(self, include_disabled=False):
        """Create a list of all radio elements in the page.

        Args:
            include_disabled: If True include disabled radios in the list (default False).

        Returns:
            A list of radio elements.
        """
        radios = self.find_elements_by_xpath('//input[@type="radio"]')
        return [r for r in radios if include_disabled or r.is_enabled()]


    def js_click_radio(self, value):
        """JavaScript snippet to click on radio buttons. This is safer than clicking by the simple WebDriver ``click()`` method, since it may fail if the radio is out of the actual viewable region of the page.

        Args:
            value: Value of radio button to click.
        """
        radio = self.find_element_by_xpath('//input[@type="radio" and @value="{}"]'.format(value))
        self.execute_script('arguments[0].click();', radio)

    def list_tables(self, **kwargs):
        """Create a list of all the tables in the page.

        Returns:
            A list of all tables in the page as pandas DataFrame objects.
        """
        try:
            tbs = pandas.read_html(self.page_source, **kwargs)
        except ValueError:
            tbs = []
        return tbs

    def press_escape(self):
        """Simulate ESCAPE keypress."""
        ActionChains(self).\
            key_down(Keys.ESCAPE).\
            key_up(Keys.ESCAPE).perform()
