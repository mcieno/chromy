import sys
from chromy import Chromy

try:
    chrome = Chromy(implicit_wait=3)
    sys.stdout.write('Successfully started Chromy driver.\n')
except:
    sys.stderr.write('Unable to start Chromy driver.\n')
    chrome.quit()
    raise RuntimeError('Unable to start Chromy driver.')
try:
    chrome.get('https://google.com/')
    sys.stdout.write('Successfully navigated to `https://google.com/`.\n')
except:
    sys.stderr.write('Unable to navigate to `https://google.com/`.\n')
    chrome.quit()
    raise RuntimeError('Unable to navigate to `https://google.com/`.')
if chrome.send_keys_to_xpath('chromy github', '//input[@name="q"]'):
    sys.stdout.write('Successfully sent keys to input form.\n')
else:
    sys.stderr.write('Unable to send keys to input form.\n')
    chrome.quit()
    raise RuntimeError('Unable to send keys to input form.')
if chrome.click_element_by_xpath('//input[@name="btnK"]'):
    sys.stdout.write('Successfully clicked on search button.\n')
else:
    sys.stderr.write('Unable to click on search button.\n')
    chrome.quit()
    raise RuntimeError('Unable to click on search button.')

sys.stdout.write('\nTest successfully completed.\n')
chrome.quit()
