import os, time, shutil, tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# ===== CONFIGURAÇÕES =====
URL_HOME = "https://www.google.com.br"
CIDADE = "Rio de Janeiro"

HEADLESS = False  # Coloque True para não abrir o navegador
IMPLICIT_WAIT = 5
EXPLICIT_WAIT = 25
PROFILE_DIR = None

# Caminho para o ChromeDriver (.exe no Windows)
CHROMEDRIVER_PATH = r"C:\Users\aluno\Desktop\atividade-previsao-main\atividade-previsao-main\chromedriver\chromedriver.exe"

# Pasta para salvar screenshots
DOWNLOAD_DIR = r"C:\Users\aluno\Downloads\unieuro_downloads"
SCREENSHOT_NAME = f"previsao_{CIDADE.lower().replace(' ', '_')}.png"

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
    Acessa o Google e busca pela previsão do tempo da cidade.
    Aguarda a caixa de previsão com ID 'wob_wc'.
    """
    driver.get(URL_HOME)

    # Espera a barra de busca carregar
    WebDriverWait(driver, EXPLICIT_WAIT).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )

    # Digita a busca
    barra_de_busca = driver.find_element(By.NAME, "q")
    barra_de_busca.clear()
    barra_de_busca.send_keys(f"previsão do tempo {cidade}")
    barra_de_busca.submit()

    # Aguarda o carregamento da caixa de previsão do tempo
    try:
        WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.presence_of_element_located((By.ID, "wob_wc"))
        )
    except TimeoutException:
        print("[ERRO] A caixa de previsão do tempo não foi encontrada.")
        raise

def capturar_previsao(driver, out_path: str):
    """
    Captura a temperatura e condição do clima da cidade e salva um screenshot.
    """
    try:
        container = WebDriverWait(driver, EXPLICIT_WAIT).until(
            EC.presence_of_element_located((By.ID, "wob_wc"))
        )

        # Extrai informações
        local = container.find_element(By.ID, "wob_loc").text
        data_hora = container.find_element(By.ID, "wob_dts").text
        temperatura = container.find_element(By.ID, "wob_tm").text
        clima = container.find_element(By.ID, "wob_dc").text

        print("\n===== PREVISÃO DO TEMPO =====")
        print(f"Cidade: {local}")
        print(f"Data e Hora: {data_hora}")
        print(f"Temperatura atual: {temperatura}°C")
        print(f"Condição climática: {clima}")
        print("==============================\n")

        # Screenshot
        out_full = os.path.join(DOWNLOAD_DIR, out_path)
        container.screenshot(out_full)
        print(f"[OK] Screenshot salvo em: {out_full}")

    except (TimeoutException, NoSuchElementException) as e:
        print("[ERRO] Não foi possível capturar a previsão.")
        print(f"Motivo: {e}")
        driver.save_screenshot(os.path.join(DOWNLOAD_DIR, out_path))

def main():
    driver = None
    try:
        driver = create_driver(HEADLESS)

        # Buscar e capturar previsão
        buscar_previsao_do_tempo(driver, CIDADE)
        capturar_previsao(driver, SCREENSHOT_NAME)

        if not HEADLESS:
            print("Deixando o navegador aberto por 6 segundos...")
            time.sleep(6)

    finally:
        if driver:
            driver.quit()
        global PROFILE_DIR
        if PROFILE_DIR and os.path.isdir(PROFILE_DIR):
            shutil.rmtree(PROFILE_DIR, ignore_errors=True)

if __name__ == "__main__":
    main()
