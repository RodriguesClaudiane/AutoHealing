"""Abre o painel visual (painel.html) no navegador padrão."""
import subprocess
import webbrowser
from pathlib import Path

CAMINHO = Path(__file__).parent / "painel.html"


def eh_wsl() -> bool:
    """WSL não tem navegador instalado nele mesmo — o navegador é o do Windows."""
    try:
        return "microsoft" in Path("/proc/version").read_text().lower()
    except OSError:
        return False


def abrir_via_windows(caminho: Path) -> bool:
    try:
        caminho_windows = subprocess.run(
            ["wslpath", "-w", str(caminho.resolve())],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        # explorer.exe costuma "falhar" com exit code 1 mesmo quando funciona — ignora o código.
        subprocess.run(["explorer.exe", caminho_windows])
        return True
    except (OSError, subprocess.CalledProcessError):
        return False


if __name__ == "__main__":
    aberto = abrir_via_windows(CAMINHO) if eh_wsl() else False
    if not aberto:
        aberto = webbrowser.open(CAMINHO.resolve().as_uri())

    if aberto:
        print(f"Abrindo {CAMINHO.name} no navegador...")
    else:
        print("Não consegui abrir o navegador automaticamente.")
        print(f"Abra manualmente: {CAMINHO.resolve()}")
