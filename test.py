def main():
    import sys
    from chromy import Chromy

    try:
        chrome = Chromy(implicit_wait=3)
        sys.stdout.write('Successfully created Chromy.\n')
    except:
        err = 'Unable to instantiate Chromy driver.\n'
        sys.stderr.write(err)
        chrome.quit()
        raise RuntimeError(err)

    try:
        chrome.get('https://google.com/')
        sys.stdout.write('Successfully navigated to `https://google.com/`.\n')
    except:
        err = 'Unable to navigate to `https://google.com/`.\n'
        sys.stderr.write(err)
        chrome.quit()
        raise RuntimeError(err)

    if chrome.send_keys_to_xpath('chromy github', '//input[@name="q"]'):
        sys.stdout.write('Successfully sent keys to input form.\n')
    else:
        err = 'Unable to send keys to input form.\n'
        sys.stderr.write(err)
        chrome.quit()
        raise RuntimeError(err)

    if chrome.click_element_by_xpath('//input[@name="btnK"]'):
        sys.stdout.write('Successfully clicked on search button.\n')
    else:
        err = 'Unable to click on search button.\n'
        sys.stderr.write(err)
        chrome.quit()
        raise RuntimeError(err)

    sys.stdout.write('\nTest successfully completed.\n')
    chrome.quit()


if __name__ == '__main__':
    main()
