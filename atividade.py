import os, time, shutil, tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# ===== CONFIG =====
URL_HOME = "https://www.google.com.br"
CIDADE = "São Paulo"  # Altere para a cidade desejada ou obtenha dinamicamente.

HEADLESS = False   # use False se o site bloquear headless
IMPLICIT_WAIT = 5
EXPLICIT_WAIT = 25
PROFILE_DIR = None

# Caminho do seu ChromeDriver local (com .exe no Windows)
CHROMEDRIVER_PATH = r"C:\Users\aluno\Desktop\Selenium-Investidor10-main\Selenium-Investidor10-main\chromedriver\chromedriver.exe"

# Pasta de saída para prints
DOWNLOAD_DIR = r"C:\Users\aluno\Downloads\unieuro_downloads"
SCREENSHOT_NAME = f"previsao_{CIDADE.lower()}.png"

def create_driver(headless: bool = False):
    global PROFILE_DIR
    PROFILE_DIR = tempfile.mkdtemp(prefix="selenium_profile_")

    if not os.path.exists(CHROMEDRIVER_PATH):
        raise FileNotFoundError(f"ChromeDriver não encontrado em: {CHROMEDRIVER_PATH}")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")

    service = ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(IMPLICIT_WAIT)
    return driver

def buscar_previsao_do_tempo(driver, cidade: str):
    """
    Realiza uma busca no Google pela previsão do tempo de uma cidade.
    """
    driver.get(URL_HOME)
    WebDriverWait(driver, EXPLICIT_WAIT).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )

    # Encontrar a barra de busca e fazer a pesquisa
    barra_de_busca = driver.find_element(By.NAME, "q")
    barra_de_busca.clear()
    barra_de_busca.send_keys(f"previsão do tempo {cidade}")
    barra_de_busca.submit()

    # Espera até que o resultado da previsão esteja visível
    WebDriverWait(driver, EXPLICIT_WAIT).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'BNeawe')]"))
    )

def capturar_previsao(driver, out_path: str):
    """
    Captura a previsão do tempo da página do Google e salva uma captura de tela.
    """
    # Encontrar a seção com a previsão
    previsao_secao = driver.find_element(By.XPATH, "//div[contains(@class, 'BNeawe')]")
    
    # Printar as informações da previsão
    previsao = previsao_secao.text
    print(f"Previsão do Tempo: {previsao}")

    # Capturar o screenshot da previsão
    out_full = os.path.join(DOWNLOAD_DIR, out_path)
    try:
        previsao_secao.screenshot(out_full)
        print(f"[OK] Screenshot (Previsão do Tempo) salvo em: {out_full}")
    except WebDriverException:
        driver.save_screenshot(out_full)
        print(f"[WARN] Screenshot do elemento falhou; salvei a janela inteira: {out_full}")

def main():
    driver = None
    try:
        driver = create_driver(HEADLESS)
        
        # Buscar a previsão do tempo para a cidade
        buscar_previsao_do_tempo(driver, CIDADE)

        # Capturar a previsão do tempo
        capturar_previsao(driver, SCREENSHOT_NAME)

        if not HEADLESS:
            print("Deixando o navegador aberto por 6s para inspeção…")
            time.sleep(6)

    finally:
        if driver:
            driver.quit()
        global PROFILE_DIR
        if PROFILE_DIR and os.path.isdir(PROFILE_DIR):
            shutil.rmtree(PROFILE_DIR, ignore_errors=True)

if __name__ == "__main__":
    main()
