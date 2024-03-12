import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def tester(func, path):
    try:
        func()
        print(f"ui tests for {path} SUCCESS")
    except Exception as e:
        print(e)
        print(f"ui tests for {path} FAIL")


def fill_login_fields(driver):
    element = driver.find_element(by=By.XPATH, value='//*[@id="FIO"]')
    element.send_keys('string')
    element = driver.find_element(by=By.XPATH, value='//*[@id="username"]')
    element.send_keys('string')
    element = driver.find_element(by=By.XPATH, value='//*[@id="password"]')
    element.send_keys('string')
    element = driver.find_element(by=By.XPATH, value='//*[@id="email"]')
    element.send_keys('string')
    element = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/button')
    element.click()
    time.sleep(3)
    if driver.current_url == "http://localhost:3000/login":
        driver.quit()
        raise "user doesn't exists"

def create_test_user():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    options.add_argument('--remote-debugging-port=9222')
    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost:3000")
    time.sleep(3)
    element = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/a[2]')
    element.click()
    element = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/div[2]/div/label[1]/span[2]')
    element.click()
    fill_login_fields(driver)
    time.sleep(3)
    return driver


def login_test_user():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')
    options.add_argument('--remote-debugging-port=9222')
    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost:3000")
    time.sleep(3)
    element = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div/a[1]')
    element.click()
    fill_login_fields(driver)
    time.sleep(3)
    return driver


def test_main_page():
    try:
        driver = login_test_user()
    except:
        driver = create_test_user()
    select_team = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div/select')
    select_team.click()
    time.sleep(3)
    element = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div/select/option[5]')
    element.click()
    time.sleep(3)
    select_team.click()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[1]/div[1]/div[1]/div[1]/p')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[1]/div[1]/div[1]/div[1]/samp[1]')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[1]/div[1]/div[1]/div[1]/samp[2]')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[1]/div[1]/div[1]/div[2]/p[1]')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[1]/div[1]/div[1]/div[2]/p[2]')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[1]/div[1]/div[1]/div[2]/p[3]')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[1]/div[1]/div[1]/div[2]/div')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[1]/div[2]/div')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[1]/div[2]/div/div[1]/b')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[1]/div[2]/div/div[2]/div[2]/canvas')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[1]/div[1]/div[2]/canvas')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[2]/div[1]/div/canvas')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[2]/div[2]/div')
    test_header(driver)


def test_header(driver):
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/b')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/div')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/div/a[1]')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/div/a[2]')
    teams_specialities_tab = driver.find_elements(by=By.CLASS_NAME, value='chakra-button')[2]
    teams_specialities_tab.click()
    time.sleep(3)

    elements = driver.find_elements(by=By.CLASS_NAME, value='chakra-menu__menuitem')
    if len(elements) != 4:
        raise "Должно быть 4 элемента"
    teams_specialities_tab.click()
    time.sleep(3)
    exit_button = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/div/a[3]')
    exit_button.click()
    time.sleep(3)
    driver.quit()


def test_analyze_kr_page():
    try:
        driver = login_test_user()
    except:
        driver = create_test_user()
    analyze_kr_page = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[1]/div/a[2]')
    analyze_kr_page.click()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[1]')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/h1')
    kr_select_simple = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div/select')
    kr_select_simple.click()
    kr_select_simple2 = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div[1]/div/select/option[2]')
    kr_select_simple2.click()
    time.sleep(3)
    kr_select_simple.click()
    type_select_simple = driver.find_element(by=By.XPATH, value='//*[@id="modeSelectSimple"]')
    type_select_simple.click()
    type_select_simple2 = driver.find_element(by=By.XPATH, value='//*[@id="modeSelectSimple"]/option[2]')
    type_select_simple2.click()
    time.sleep(3)
    type_select_simple.click()
    time.sleep(3)
    xpaths = {
        'kr_select_pro': '//*[@id="root"]/div[3]/div[2]/div[1]/div/select',
        'type_select_pro': '//*[@id="modeSelectFiltr"]',
        'teacher_select_pro': '//*[@id="root"]/div[3]/div[2]/div[3]/div/select',
        'speciality_select_pro': '//*[@id="root"]/div[3]/div[2]/div[4]/div/select',
        'team_select_pro': '//*[@id="root"]/div[3]/div[2]/div[5]/div/select'
    }
    options = {
        'kr_select_pro': '//*[@id="root"]/div[3]/div[2]/div[1]/div/select/option[2]',
        'type_select_pro': '//*[@id="modeSelectFiltr"]/option[2]',
        'teacher_select_pro': '//*[@id="root"]/div[3]/div[2]/div[3]/div/select/option[4]',
        'speciality_select_pro': '//*[@id="root"]/div[3]/div[2]/div[4]/div/select/option[25]',
        'team_select_pro': '//*[@id="root"]/div[3]/div[2]/div[5]/div/select/option[15]'
    }
    for element_name, xpath in xpaths.items():
        element = driver.find_element(by=By.XPATH, value=xpath)
        element.click()
    time.sleep(3)
    for element_name, xpath in options.items():
        element = driver.find_element(by=By.XPATH, value=xpath)
        element.click()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[3]/canvas')
    test_header(driver)


def test_your_groups():
    try:
        driver = login_test_user()
    except:
        driver = create_test_user()
    teams_specialities_tab = driver.find_elements(by=By.CLASS_NAME, value='chakra-button')[2]
    teams_specialities_tab.click()
    time.sleep(3)
    element = driver.find_elements(by=By.CLASS_NAME, value='chakra-menu__menuitem')[0]
    element.click()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/h2')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[1]/canvas')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[2]/canvas')
    test_header(driver)

def comparison_page_check(driver):
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/h2')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div/p')
    team_select_1 = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div/div/div[1]/div/select')
    team_select_2 = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div/div/div[2]/div/select')
    team_select_1.click()
    team_select_2.click()
    time.sleep(3)
    team1 = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div/div/div[1]/div/select/option[2]')
    team2 = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/div/div/div[2]/div/select/option[5]')
    team1.click()
    team2.click()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[1]/canvas')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[2]/canvas')
def test_your_groups_comparison():
    try:
        driver = login_test_user()
    except:
        driver = create_test_user()
    teams_specialities_tab = driver.find_elements(by=By.CLASS_NAME, value='chakra-button')[2]
    teams_specialities_tab.click()
    time.sleep(3)
    element = driver.find_elements(by=By.CLASS_NAME, value='chakra-menu__menuitem')[1]
    element.click()
    comparison_page_check(driver)
    time.sleep(3)
    test_header(driver)


def test_your_specialities():
    try:
        driver = login_test_user()
    except:
        driver = create_test_user()
    teams_specialities_tab = driver.find_elements(by=By.CLASS_NAME, value='chakra-button')[2]
    teams_specialities_tab.click()
    time.sleep(3)
    element = driver.find_elements(by=By.CLASS_NAME, value='chakra-menu__menuitem')[2]
    element.click()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[2]/h2')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[1]/canvas')
    driver.find_element(by=By.XPATH, value='//*[@id="root"]/div[3]/div[2]/canvas')
    test_header(driver)


def test_your_specialities_comparison():
    try:
        driver = login_test_user()
    except:
        driver = create_test_user()
    teams_specialities_tab = driver.find_elements(by=By.CLASS_NAME, value='chakra-button')[2]
    teams_specialities_tab.click()
    time.sleep(3)
    element = driver.find_elements(by=By.CLASS_NAME, value='chakra-menu__menuitem')[3]
    element.click()
    time.sleep(3)
    comparison_page_check(driver)
    test_header(driver)


tester(test_main_page, "http://localhost:3000/main")
tester(test_analyze_kr_page, "http://localhost:3000/analys_kr")
tester(test_your_groups, "http://localhost:3000/your_group")
tester(test_your_groups_comparison, "http://localhost:3000/match2team")
tester(test_your_specialities, "http://localhost:3000/your_vectorstudy")
tester(test_your_specialities_comparison, "http://localhost:3000/match2team_vectorstudy")
