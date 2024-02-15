from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime

#Armazenar data atual
day_ = datetime.now().date()
today = day_.strftime("%Y-%m-%d")

conta = 0

#Acessos

with open('Password.txt','r') as file:
    pass_ = file.read()

with open('Accounts.txt', 'r') as file:
    user_ = file.read().splitlines()

    #percorrer todas as contas
    for user in user_: 
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(options=options)

        #Open browser
        driver.get("https:flow.polar.com")
        sleep(3)
        driver.maximize_window()
        sleep(1)
        cookies = driver.find_element(By.XPATH,"/html/body/div[5]/div[3]/div/div/div[2]/div/div/button[2]").click()

        #login
        signIn = driver.find_element(By.XPATH,"/html/body/nav/div[2]/div/div/ul[2]/li/a").click()
        sleep(5)
        login = driver.find_element(By.NAME,"email").send_keys(user) 
        password = driver.find_element(By.NAME,"password").send_keys(pass_)
        SignIn = driver.find_element(By.XPATH,"/html/body/nav/div[2]/div/div/ul[2]/li/div/div/form/div/div/div[3]/button").click()
        sleep(2)

        #Entrar day
        day = driver.find_element(By.XPATH,"/html/body/div[4]/div[1]/div/div[2]/div/div[1]/ul[1]/li[1]/a").click()    
        sleep(6)

        #Buscar HTML da página
        soup = BeautifulSoup(driver.page_source,"html")

        exercicio_links = []

        #busca dos itens de execicios do dia
        ed_exercicios = soup.find_all('div',class_='event event-day exercise') 
        for exercicio in ed_exercicios:
            exercicio_links.append(exercicio.find('a').get('href'))

        #Baixar arquivos
        for link in exercicio_links:
            ex_id = link.split('/')[-1]
            driver.get("https://flow.polar.com/api/export/training/csv/" + ex_id)
            sleep(3)

        #Criar .txt evidência 
        notas = []

        for codigo in exercicio_links:
            nota = codigo.split('/')[-1]
            notas.append(nota)

        nome_arquivo = f"{today}.txt"
        
        with open(nome_arquivo,'a') as arquivo:
            conta += 1
            arquivo.write(f'\n{str(conta)}- {str(user)}\n')
            for download in notas:
                arquivo.write(str(download)+'\n') 

        driver.quit()