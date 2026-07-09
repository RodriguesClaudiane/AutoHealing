import argparse

from auto_healing import Driver, Pagina


def teste_de_login(driver: Driver):
    """O script de teste NÃO muda: sempre usa os mesmos nomes lógicos."""
    usuario = driver.localizar("campo_usuario")
    senha = driver.localizar("campo_senha")
    botao = driver.localizar("botao_entrar")

    # simulação das ações do teste
    print(f"\n   ⌨️  Digitando usuário em <{usuario.tag} {usuario.seletor}>")
    print(f"   ⌨️  Digitando senha   em <{senha.tag} {senha.seletor}>")
    print(f"   🖱️  Clicando          em <{botao.tag} {botao.seletor}> ('{botao.text}')")


def rodar(auto_healing: bool):
    print("=" * 62)
    print(f"  Teste de Login  |  "
          f"Auto-healing: {'LIGADO 🩹' if auto_healing else 'DESLIGADO'}")
    print("=" * 62)

    pagina = Pagina("app.html")
    driver = Driver(pagina=pagina, healing_ativo=auto_healing)

    try:
        teste_de_login(driver)
        driver.salvar_relatorio_curas()
        print("\n" + "=" * 62)
        curadas = len(driver.curas)
        extra = f" ({curadas} seletor(es) curado(s) em tempo de execução)" if curadas else ""
        print(f"  ✅ TESTE PASSOU{extra}")
    except AssertionError as erro:
        print(f"\n   💥 {erro}")
        print("\n" + "=" * 62)
        print("  ❌ TESTE FALHOU")
    print("=" * 62)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Roda o teste de login contra app.html, com ou sem auto-healing."
    )
    parser.add_argument(
        "--healing", choices=["ligado", "desligado", "ambos"], default="ambos",
        help="ligado: só com healing | desligado: só sem healing | "
             "ambos: roda os dois em sequência para comparar (padrão)",
    )
    args = parser.parse_args()

    modos = {"ligado": [True], "desligado": [False], "ambos": [True, False]}[args.healing]
    for auto_healing in modos:
        rodar(auto_healing)
