# Chromy

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

Easy-to-use Selenium Chromedriver. *Requires chromedriver.exe* in the same
folder of the script importing Chromy.

## Usage

**Initialize**
```python
from chromy import Chromy

chrome = Chromy()
```

**Get URL**
```python
chrome.get('https://github.com/')
```

**Click on links**
```python
chrome.click_element_by_link_text('login')
```

**Send keys to form inputs and submitting**
```python
chrome.send_keys_to_xpath('username', '//input[@name="login"]')
chrome.send_keys_to_xpath('password', '//input[@name="password"]')
chrome.click_element_by_xpath('//input[type="submit"]')
```

**Clicking on radio buttons with JavaScript**
```python
chrome.js_click_radio('Apples')
```
