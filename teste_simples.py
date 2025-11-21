import undetected_chromedriver as uc
import time

def teste_simples():
    print(">>> Iniciando teste mínimo...")
    
    # SUBSTITUA 131 PELA SUA VERSÃO DO CHROME (ex: 130, 131, 132)
    MINHA_VERSAO = 142 
    
    try:
        # Vamos rodar sem perfil e sem subprocesso inicialmente para ver o erro real se houver
        driver = uc.Chrome(
            version_main=MINHA_VERSAO,
            use_subprocess=False 
        )
        
        print(">>> Navegador abriu! Acessando Google...")
        driver.get("https://www.google.com")
        time.sleep(5)
        print(">>> Sucesso total.")
        driver.quit()
        
    except Exception as e:
        print(f"\n>>> ERRO FATAL: {e}")

if __name__ == "__main__":
    teste_simples()