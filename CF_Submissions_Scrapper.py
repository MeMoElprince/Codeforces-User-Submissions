import os, time, csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from helper.colors import colors
from collections import defaultdict
from dotenv import load_dotenv
load_dotenv()

# Get the cur directory 
directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(directory)

dictionaryCheck = defaultdict()

# make timeout 20 sec for command find element
def find_element(driver, by, value, timeout = 20):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((by, value)), f'{colors.red}Timeout while trying to reach an element ❌{colors.reset}')


# Get Handles from file
def getTrainees(file):
    print(f'{colors.blue}\nGetting Trainees... {colors.reset}')
    trainees = {}
    isHeader = True
    with open(file, 'r') as data:
        csvfile = csv.reader(data)
        for row in csvfile:
            if isHeader:
                isHeader = False
                continue
            solved_problems = 0
            try:
                solved_problems = int(row[2])
            except:
                solved_problems = 0
            trainee = {
                "Name": row[0],
                "Codeforces Handle": row[1],
                "Number of Problems Solved": solved_problems,
                "Number of All Problems": 0,
                "Solved Problems Percentage": 0
            }
            trainees[row[1]] = trainee
    print(f'{colors.green}Trainees data loaded ✅{colors.reset}\n')
    return trainees


# getting links from file
def get_links(file):
    print(f'{colors.blue}\nGetting Links... {colors.reset}')
    f = open(file, "r")
    links = f.read().strip().split('\n')
    print(f'{colors.green}Links loaded ✅{colors.reset}\n')
    return links


# create chrome driver
def createDriver(opeining_message=True):
    if opeining_message:
        print(f'{colors.blue}\nCreating Driver... {colors.reset}')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
    driver.set_page_load_timeout(5)
    if opeining_message:
        print(f'{colors.green}Driver created ✅{colors.reset}\n')
    return driver


# Go to main page
def openCodeforces(driver, opening_message=True):
    if opening_message:
        print(f'{colors.blue}Openning Codeforce... {colors.beige}(Note that might take one minute in the worst case){colors.reset}')
    handle = os.getenv('HANDLE')
    password = os.getenv('PASSWORD')
    envTest = os.path.exists('.env')
    
    if not envTest:
        print(f'{colors.red}Please create env file{colors.reset}')
    if not handle or not password:
        print(f'{colors.red}Please set the env variables (handle or password){colors.reset}')
        return

    try:
        driver.get('https://codeforces.com/enter')
        time.sleep(2)
        find_element(driver, By.XPATH, '//*[@id="handleOrEmail"]').send_keys(handle);
        find_element(driver, By.XPATH, '//*[@id="password"]').send_keys(password);
        time.sleep(1)
        find_element(driver, By.XPATH, '//*[@id="enterForm"]/table/tbody/tr[4]/td/div[1]/input').click();
        time.sleep(2)
        
        
        # check if login is successful or not
        isLogged = False
        try:
            driver.find_element(By.XPATH, '//*[@id="enterForm"]/table/tbody/tr[3]/td[2]/div/span')
            isLogged = False
        except:
            isLogged = True
        
        
        if not isLogged:
            print(f'{colors.red}Login failed... check your handle and password ❌\n{colors.reset}')
            driver.quit()
            exit(0)
        else:
            print(f'{colors.green}Login successful ✅{colors.reset}\n')
    except TimeoutException:
        driver.quit()
        driver = createDriver(False)
        driver = openCodeforces(driver, False)
        
    return driver
    

# main process Getting Data from standings

def getData(driver, trainees):
    contest_title = find_element(driver, By.XPATH, '//*[@id="pageContent"]/div[3]/div/a').text
    print(f'{colors.blue}Getting Data from {contest_title}... {colors.reset}')
    dict = defaultdict(set)
    dictAccepted = defaultdict(set)
    all_problems = 0
    try:
        for pages in range(1, 500):
            print(f'{colors.magenta}\nPage #{pages}{colors.reset}\n')
            is_many_pages = True
            try:
                find_element(driver, By.XPATH, f'//*[@id="pageContent"]/div[10]/nobr[{pages}]', 5).click()
            except:
                is_many_pages = False
            try:
                for i in range(2, 400):
                    is_handle_availabe = True
                    try:
                        handle = find_element(driver, By.XPATH, f'//*[@id="pageContent"]/div[5]/div[6]/table/tbody/tr[{i}]/td[2]/a', 0).text
                    except:
                        try:
                            handle = find_element(driver, By.XPATH, f'//*[@id="pageContent"]/div[5]/div[6]/table/tbody/tr[{i}]/td[2]/span', 0).text
                        except:
                            try:
                                handle = find_element(driver, By.XPATH, f'//*[@id="pageContent"]/div[5]/div[6]/table/tbody/tr[{i}]/td[2]', 0).text
                            except:
                                is_handle_availabe = False
                    if is_handle_availabe == False:
                        break

                    if not handle in trainees:
                        continue
                    cnt = 0
                    print(handle + ' : ', end = ' ')
                    try:
                        for j in range(5, 40):
                            try:
                                problems = find_element(driver, By.XPATH, f'//*[@id="pageContent"]/div[5]/div[6]/table/tbody/tr[{i}]/td[{j}]', 0).text
                                all_problems = max(all_problems, j - 4)
                                try:
                                    problemID = find_element(driver, By.XPATH, f'//*[@id="pageContent"]/div[5]/div[6]/table/tbody/tr[1]/th[{j}]/a', 0).text
                                    all_problems = max(all_problems, j - 4)
                                except:
                                    try:
                                        problemID = find_element(driver, By.XPATH, f'//*[@id="pageContent"]/div[5]/div[6]/table/tbody/tr[1]/th[{j}]/span', 0).text
                                        all_problems = max(all_problems, j - 4)
                                    except:  
                                        try:
                                            problemID = find_element(driver, By.XPATH, f'//*[@id="pageContent"]/div[5]/div[6]/table/tbody/tr[1]/th[{j}]', 0).text
                                            all_problems = max(all_problems, j - 4)
                                        except:                                        
                                            print(f'{colors.red}Error getting problem Id with j = {j} {colors.reset}', end = ' ')
                                            break
                                try:
                                    test = str(problems)
                                    if test.find('+') != -1:
                                        cnt += 1
                                        dictAccepted[handle].add(problemID)
                                    dict[handle].add(problemID)
                                except:
                                    print(f'{colors.red}Error in checking + {colors.reset}', end = ' ')
                            except:
                                print(f'{colors.gold}{cnt} {colors.green}Accepted  ✅{colors.reset}')
                                break
                    except:
                        print(f'{colors.red}Error getting problems{colors.reset}')
            except:
                print(f'{colors.red}No more Handles in this page{colors.reset}')
            if is_many_pages == False:
                print(f'{colors.red}No more pages in the standings{colors.reset}')
                break
    except:
        print(f'{colors.red}No more pages in the standings{colors.reset}')
    
        
    # update the data
    for trainee in trainees:
        trainees[trainee]['Number of Problems Solved'] += len(dictAccepted[trainee])
        trainees[trainee]['Number of All Problems'] += all_problems
        trainees[trainee]['Solved Problems Percentage'] = 0 if trainees[trainee]['Number of All Problems'] == 0 else trainees[trainee]['Number of Problems Solved'] / trainees[trainee]['Number of All Problems'] * 100
        
    return [trainees, contest_title]


def save_to_csv(trainees):
    with open('data/trainees.csv', 'w', newline='') as file:
        fieldnames = ['Name', 'Codeforces Handle', 'Number of Problems Solved', 'Number of All Problems', 'Solved Problems Percentage']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for trainee in trainees:
            writer.writerow({'Name':trainees[trainee]['Name'], 'Codeforces Handle':trainees[trainee]['Codeforces Handle'], 'Number of Problems Solved':trainees[trainee]['Number of Problems Solved'], 'Number of All Problems':trainees[trainee]['Number of All Problems'], 'Solved Problems Percentage':f"{trainees[trainee]['Solved Problems Percentage']:.2f}%"})
    print(f'{colors.gold}\nData saved to trainees.csv ✅{colors.reset}\n')
    

# main function
def main():
    
    #Get the directory of current folder
    directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(directory)
    
    print(f'{colors.magenta}Starting the program... {colors.reset}')
    
    # getting trainees data
    trainees = getTrainees('data/Data.csv')
    
    # getting links of standings
    links = get_links('data/links.txt')
    
    # create driver 
    driver = createDriver()
    
    # open the login codeforces page
    driver = openCodeforces(driver)
    
    # scraping the data from the standings
    for link in links:
        driver.get(link)
        time.sleep(2)
        [trainees, title] = getData(driver, trainees)
        print(f'\n{colors.gold}Done with {title} {colors.reset} ✅\n')
    
    # save the data to csv file
    save_to_csv(trainees)
    

# Run the main function
if __name__ == "__main__":
    main()
