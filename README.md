# Chromy

![](https://img.shields.io/badge/version-2-blue.svg)
![](https://img.shields.io/badge/status-stable-brightgreen.svg)
![](https://img.shields.io/badge/requirements-up%20to%20date-brightgreen.svg)

Easy-to-use Selenium Chromedriver.


## Getting started

### Cloning and installing requirements

```sh
$ git clone https://github.com/mcieno/chromy.git
$ cd chromy
$ pip3 install -r requirements.txt
```

Optionally install [`console_logging`](https://github.com/pshah123/console-logging) to print fancy logs.

```sh
$ pip3 install console-logging
```

### Adding chromedriver to PATH

Selenium requires chromedriver binary to be in `PATH` variable.

Depending on your operating system unpack the correct ZIP file and add chromedriver binary to your `PATH`.

In linux this may look like:
```sh
$ 7z x chromedriver_linux64.zip
$ PATH=$(pwd):$PATH
```
**Note:** the above changes to `PATH` are not persistent.

### Importing Chromy and getting started

Starting Chrome WebDriver is as simple as:

```python
>>> from chromy import *
>>>
>>> chrome = Chromy()
```


## Usage

**Get URL**
```python
chrome.get('https://github.com/')
```

**Click on elements**
```python
chrome.click_element_by_link_text('login')
```

**Send keys to elements**
```python
chrome.send_keys_to_xpath('username', '//input[@name="login"]')
chrome.send_keys_to_xpath('password', '//input[@name="password"]')
chrome.click_element_by_xpath('//input[type="submit"]')
```

**Click on radio buttons with JavaScript**
```python
chrome.js_click_radio('Apples')
```

