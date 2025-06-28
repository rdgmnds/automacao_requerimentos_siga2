from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

def executar_automacao(usuario, senha, perfil):
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page()

        pagina.goto("https://siga-hub.fgv.br/app/main/home", wait_until="load")

        #LOGIN
        pagina.fill('#user', os.getenv("usuario"))
        pagina.fill('#password', os.getenv("senha"))
        pagina.click('xpath=//*[@id="content"]/div[2]/form/div[5]/button')

        #SELECIONAR PERFIL
        pagina.locator("span.name", has_text="Controladoria").wait_for(timeout=60000)
        pagina.locator("span.name", has_text="Controladoria").click()
        pagina.fill('xpath=//*[@id="kt_app_header_wrapper"]/div[2]/app-topbar/div/paper/div/div[2]/ul/li[86]/a/span[2]', perfil)
        
        #ACESSAR REQUERIMENTOS
        pagina.get_by_text("Requerimento", exact=True).click()
        pagina.get_by_text("Certificação", exact=True).click()
        pagina.get_by_text("1. Analisar ", exact=True).last.click()

        #ACESSAR IFRAME DE REQUERIMENTOS
        iframe_requerimentos = pagina.frame_locator('#frameSiga2')
        iframe_requerimentos.locator('xpath=//*[@id="SistemaContentPlaceHolder_UC_FiltroCertificacao_LtbSituacaoRequerimento"]/option[2]').click()
        iframe_requerimentos.locator('xpath=//*[@id="SistemaContentPlaceHolder_BtnBuscar"]').click()

        #PERCORRER LISTA DE REQUERIMENTOS
        requerimentos = iframe_requerimentos.locator('#SistemaContentPlaceHolder_UserControlListaAlunoCertificado_gdwListaRequerimentoAluno tr')

        for i in range(1, requerimentos.count()):
            requerimento = requerimentos.nth(i)
            requerimento.click()

            label = iframe_requerimentos.locator('xpath=//*[@id="SistemaContentPlaceHolder_UserControlPlanoFinanceiroAluno_LblQtdeInadiplente"]')
            valor = label.text_content().strip()

            if valor != "0":
                iframe_requerimentos.locator('#SistemaContentPlaceHolder_TxtIndeferido').fill('O cliente possui débitos em aberto')
                iframe_requerimentos.locator('#SistemaContentPlaceHolder_BtnEmEspera').click()
            else:
                iframe_requerimentos.locator('#SistemaContentPlaceHolder_TxtIndeferido').fill('O cliente não possui débitos em aberto')
                iframe_requerimentos.locator('#SistemaContentPlaceHolder_BtnDeferirRequerimento').click()

            requerimentos = iframe_requerimentos.locator('#SistemaContentPlaceHolder_UserControlListaAlunoCertificado_gdwListaRequerimentoAluno tr')

if __name__ == "__main__":
    executar_automacao()

