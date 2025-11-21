import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

def testar_login_bb():
    print(">>> INICIANDO AUTOMACAO BB (FLUXO COMPLETO) <<<")
    
    # Recupera as credenciais
    usuario_env = os.getenv("BB_USUARIO")
    senha_env = os.getenv("BB_SENHA")

    if not usuario_env or not senha_env:
        print("ERRO: Verifique seu arquivo .env")
        return

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = uc.Chrome(
        options=options,
        use_subprocess=True,
        version_main=142
    )

    try:
        print("[1] Acessando página de login...")
        driver.get('https://loginweb.bb.com.br/sso/XUI/?realm=/paj&goto=https://juridico.bb.com.br/wfj#login')
        
        # --- PASSO 1: INSERIR USUÁRIO ---
        print("[2] Inserindo usuário (idToken1)...")
        campo_usuario = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "idToken1"))
        )
        campo_usuario.clear()
        campo_usuario.send_keys(usuario_env)
        
        time.sleep(0.5)

        # --- PASSO 2: PRIMEIRO CLIQUE (AUTENTICAR) ---
        print("[3] Primeiro clique em 'AUTENTICAR'...")
        botao_1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "loginButton_0"))
        )
        botao_1.click()
        print("--> Aguardando transição de tela...")

        # --- PASSO 3: INSERIR SENHA ---
        print("[4] Aguardando campo de SENHA (idToken3)...")
        # A espera aqui é maior (60s) por causa do possível Cloudflare no meio
        campo_senha = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "idToken3"))
        )
        
        print("--> Inserindo senha...")
        campo_senha.clear()
        campo_senha.send_keys(senha_env)
        
        time.sleep(0.5) # Pausa técnica para o site processar o input

        # --- PASSO 4: SEGUNDO CLIQUE (AUTENTICAR FINAL) ---
        print("[5] Segundo clique em 'AUTENTICAR' (callback_4)...")
        
        # Usamos um seletor CSS específico que combina o ID com o NAME 'callback_4'
        # Isso garante que clicamos no botão novo e não numa "memória" do botão antigo
        botao_final = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#loginButton_0[name='callback_4']"))
        )
        botao_final.click()
        
        print(">>> LOGIN ENVIADO COM SUCESSO! <<<")

        time.sleep(10) # Mantém aberto para você ver o resultado final

    except Exception as e:
        print(f">>> FALHA: {e}")
        driver.save_screenshot("erro_final.png")
        print("Print do erro salvo como 'erro_final.png'")

    finally:
        driver.quit()

if __name__ == "__main__":
    testar_login_bb()