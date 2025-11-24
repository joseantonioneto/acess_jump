import time
import os
from teste_bb import testar_login_bb

def limpar_processos_presos():
    """Garante que não sobrou nenhum Chrome zumbi antes de começar"""
    try:
        os.system("taskkill /IM chrome.exe /F >nul 2>&1")
        os.system("taskkill /IM undetected_chromedriver.exe /F >nul 2>&1")
    except:
        pass

def iniciar_teste_de_estresse(qtd_execucoes=5):
    print(f"==========================================")
    print(f" INICIANDO TESTE DE ESTRESSE: {qtd_execucoes} TENTATIVAS")
    print(f"==========================================\n")

    sucessos = 0
    falhas = 0

    for i in range(1, qtd_execucoes + 1):
        print(f"🔄 Tentativa {i}/{qtd_execucoes} iniciada...")
        
        # 1. Limpeza preventiva
        limpar_processos_presos()
        time.sleep(2) # Tempo para o Windows liberar os arquivos

        # 2. Executa o teste importado
        # Cronometra o tempo de execução
        inicio = time.time()
        resultado = testar_login_bb()
        fim = time.time()
        duracao = round(fim - inicio, 2)

        # 3. Contabiliza
        if resultado:
            print(f"✅ Tentativa {i}: SUCESSO ({duracao}s)")
            sucessos += 1
        else:
            print(f"❌ Tentativa {i}: FALHA ({duracao}s)")
            falhas += 1

        # 4. Cooldown (MUITO IMPORTANTE)
        # Se você tentar logar 10x em 1 minuto, o Banco do Brasil VAI bloquear seu IP.
        # Coloquei 15 segundos de pausa entre tentativas.
        if i < qtd_execucoes:
            print("⏳ Aguardando 15s para próxima tentativa (evitar bloqueio de IP)...")
            time.sleep(15)
        
        print("-" * 30)

    # RELATÓRIO FINAL
    print("\n" + "="*40)
    print("       RELATÓRIO FINAL DE ESTABILIDADE")
    print("="*40)
    print(f"Total Tentativas: {qtd_execucoes}")
    print(f"✅ Sucessos:      {sucessos}")
    print(f"❌ Falhas:        {falhas}")
    
    taxa_sucesso = (sucessos / qtd_execucoes) * 100
    print(f"📊 Taxa de Êxito: {taxa_sucesso:.1f}%")
    print("="*40)

if __name__ == "__main__":
    # Quantas vezes você quer testar? Recomendo começar com 3 ou 5.
    iniciar_teste_de_estresse(qtd_execucoes=5)