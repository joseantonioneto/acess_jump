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
    # print(">>> INICIANDO AUTOMACAO BB (FLUXO COMPLETO) <<<") 
    
    # Recupera as credenciais
    usuario_env = os.getenv("BB_USUARIO")
    senha_env = os.getenv("BB_SENHA")

    if not usuario_env or not senha_env:
        print("ERRO: Verifique seu arquivo .env")
        return False

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    
    
    # options.add_argument("--headless=new") 

    driver = uc.Chrome(
        #options=options,
        use_subprocess=True,
        version_main=142
    )

    try:
        # print("[1] Acessando página de login...")
        driver.get('https://loginweb.bb.com.br/sso/XUI/?realm=/paj&goto=https://juridico.bb.com.br/wfj#login')
        
        # --- PASSO 1: INSERIR USUÁRIO ---
        # print("[2] Inserindo usuário...")
        campo_usuario = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "idToken1"))
        )
        campo_usuario.clear()
        campo_usuario.send_keys(usuario_env)
        time.sleep(0.5)

        # --- PASSO 2: PRIMEIRO CLIQUE ---
        # print("[3] Primeiro clique em 'AUTENTICAR'...")
        botao_1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "loginButton_0"))
        )
        botao_1.click()
        
        # --- PASSO 3: INSERIR SENHA ---
        # print("[4] Aguardando campo de SENHA...")
        campo_senha = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.ID, "idToken3"))
        )
        campo_senha.clear()
        campo_senha.send_keys(senha_env)
        time.sleep(0.5)

        # --- PASSO 4: SEGUNDO CLIQUE ---
        # print("[5] Segundo clique em 'AUTENTICAR'...")
        botao_final = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#loginButton_0[name='callback_4']"))
        )
        botao_final.click()
        
        # Se chegou até aqui sem erro, consideramos sucesso no envio
        # print(">>> LOGIN ENVIADO COM SUCESSO! <<<")
        
        # Retorna True para o loop saber que deu certo
        return True

    except Exception as e:
        print(f">>> FALHA NO SCRIPT: {e}")
        driver.save_screenshot(f"erro_{int(time.time())}.png") # Nome único para não sobrescrever
        return False

    finally:
        driver.quit()

if __name__ == "__main__":
    # Se rodar direto este arquivo, ele executa uma vez e imprime o resultado
    resultado = testar_login_bb()
    print(f"Resultado da execução única: {'SUCESSO' if resultado else 'FALHA'}")