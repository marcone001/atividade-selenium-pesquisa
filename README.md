Projeto: Previsão do Tempo com Selenium

Este projeto utiliza Python + Selenium WebDriver para buscar automaticamente a previsão do tempo de uma cidade no Google e salvar um screenshot com o resultado.

🚀 Funcionalidades

Abre o navegador Google Chrome usando Selenium.

Faz a busca pela previsão do tempo da cidade configurada.

Captura o texto da previsão e exibe no terminal.

Salva um screenshot da seção de previsão do tempo em uma pasta local.

Funciona tanto em modo visível quanto em headless (sem abrir janela do navegador).

🛠️ Tecnologias utilizadas

Python 3.8+

Selenium 4.x

Google Chrome (instalado no sistema)

ChromeDriver (compatível com a versão do seu Chrome)

📂 Estrutura do Projeto
projeto_previsao_tempo/
│── chromedriver/               # Pasta contendo o ChromeDriver
│── main.py                     # Código principal (fornecido acima)
│── README.md                   # Este arquivo
│── unieuro_downloads/          # Pasta onde os prints serão salvos
⚙️ Configuração
1. Clonar o repositório
 git clone https://github.com/seuusuario/projeto_previsao_tempo.git
cd projeto_previsao_tempo
2. Criar e ativar um ambiente virtual (opcional, mas recomendado)
   python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac
3. Instalar dependências
pip install selenium

4. Configurar variáveis no código (main.py)

CIDADE → Nome da cidade que deseja pesquisar.

CHROMEDRIVER_PATH → Caminho do chromedriver.exe no seu computador.

DOWNLOAD_DIR → Pasta onde os screenshots serão salvos.

HEADLESS → True para rodar sem abrir o navegador, False para visualizar.

Exemplo:

CIDADE = "São Paulo"
HEADLESS = False
CHROMEDRIVER_PATH = r"C:\Users\aluno\Desktop\Selenium-Investidor10-main\Selenium-Investidor10-main\chromedriver\chromedriver.exe"
DOWNLOAD_DIR = r"C:\Users\aluno\Downloads\unieuro_downloads"

▶️ Como executar

No terminal, rode:

python main.py

Saídas:

No terminal: texto da previsão do tempo.

No diretório unieuro_downloads/: screenshot salvo com o nome previsao_são paulo.png (ou o nome da cidade definida).

📸 Exemplo de execução
Previsão do Tempo: 23°C Parcialmente nublado
[OK] Screenshot (Previsão do Tempo) salvo em: C:\Users\aluno\Downloads\unieuro_downloads\previsao_são paulo.png
Deixando o navegador aberto por 6s para inspeção…

⚠️ Observações

O ChromeDriver deve ser da mesma versão do Google Chrome instalado.

Caso o Google bloqueie automação, usar HEADLESS = False.

A pasta de perfil temporário do Chrome é criada automaticamente e apagada ao final.

