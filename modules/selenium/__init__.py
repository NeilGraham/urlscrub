def add_domain_cookies(driver, domain, cookies=[]):
    for cookie in cookies:
        if domain.endswith(cookie['domain']) or (domain+'.').endswith(cookie['domain']):
            driver.add_cookie(cookie)