"""
Motor de Auto-Healing de seletores.

Ideia central (a mesma usada por ferramentas como Healenium e Testim):
  1. O teste tenta localizar o elemento pelo seletor primário (ex.: #username).
  2. Se o seletor quebrou (a UI mudou), o motor NÃO falha imediatamente:
     ele compara a "impressão digital" (fingerprint) gravada do elemento
     (tag, name, type, placeholder, texto...) com todos os elementos da
     página atual e calcula um score de similaridade.
  3. Se o melhor candidato passa do limiar de confiança, o seletor é
     "curado": o teste segue usando o novo seletor e a cura é registrada
     em healed_selectors.json para auditoria.
"""

import json
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONFIANCA_MINIMA = 0.60  # abaixo disso o healing desiste e o teste falha


# ----------------------------------------------------------------------
# Um "navegador" minúsculo: transforma o HTML numa lista de elementos
# ----------------------------------------------------------------------
@dataclass
class Elemento:
    tag: str
    attrs: dict
    text: str = ""

    @property
    def seletor(self) -> str:
        if "id" in self.attrs:
            return f"#{self.attrs['id']}"
        return self.tag


class _Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elementos: list[Elemento] = []
        self._pilha: list[Elemento] = []

    def handle_starttag(self, tag, attrs):
        el = Elemento(tag=tag, attrs=dict(attrs))
        self.elementos.append(el)
        self._pilha.append(el)

    def handle_endtag(self, tag):
        if self._pilha:
            self._pilha.pop()

    def handle_data(self, data):
        if self._pilha and data.strip():
            self._pilha[-1].text += data.strip()


class Pagina:
    def __init__(self, caminho_html: str):
        html = (BASE_DIR / caminho_html).read_text()
        parser = _Parser()
        parser.feed(html)
        self.elementos = parser.elementos

    def buscar(self, seletor: str) -> Elemento | None:
        """Suporta apenas seletor por id (#algo) — suficiente para a demo."""
        if seletor.startswith("#"):
            alvo = seletor[1:]
            for el in self.elementos:
                if el.attrs.get("id") == alvo:
                    return el
        return None


# ----------------------------------------------------------------------
# O motor de healing propriamente dito
# ----------------------------------------------------------------------
def _similaridade(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _score(fingerprint: dict, el: Elemento) -> float:
    """Compara a impressão digital gravada com um elemento da página atual.
    Pesos: atributos estáveis (name, type) valem mais que texto visível."""
    pesos = {"tag": 1.0, "name": 3.0, "type": 2.0, "placeholder": 2.0, "text": 2.0}
    total, obtido = 0.0, 0.0
    for chave, esperado in fingerprint.items():
        peso = pesos.get(chave, 1.0)
        total += peso
        atual = el.text if chave == "text" else el.attrs.get(chave, "")
        obtido += peso * _similaridade(esperado, atual)
    return obtido / total if total else 0.0


@dataclass
class Driver:
    """Localizador de elementos com auto-healing opcional."""
    pagina: Pagina
    healing_ativo: bool
    seletores: dict = field(default_factory=dict)
    curas: list = field(default_factory=list)

    def __post_init__(self):
        self.seletores = json.loads((BASE_DIR / "selectors.json").read_text())

    def localizar(self, nome_logico: str) -> Elemento:
        info = self.seletores[nome_logico]
        primario = info["primary"]

        el = self.pagina.buscar(primario)
        if el:
            print(f"   ✅ '{nome_logico}': encontrado por {primario}")
            return el

        print(f"   ⚠️  '{nome_logico}': seletor {primario} QUEBROU (elemento não existe)")

        if not self.healing_ativo:
            raise AssertionError(
                f"ElementNotFound: {primario} — auto-healing DESLIGADO, teste falha."
            )

        # --- tentativa de cura: procura o elemento mais parecido na página ---
        candidatos = [
            (_score(info["fingerprint"], el), el) for el in self.pagina.elementos
        ]
        confianca, melhor = max(candidatos, key=lambda c: c[0])

        if confianca < CONFIANCA_MINIMA:
            raise AssertionError(
                f"Healing falhou para '{nome_logico}': melhor candidato "
                f"<{melhor.tag}> com confiança {confianca:.0%} < {CONFIANCA_MINIMA:.0%}"
            )

        novo_seletor = melhor.seletor
        print(f"   🩹 CURADO: {primario} → {novo_seletor} (confiança {confianca:.0%})")
        self.curas.append(
            {"elemento": nome_logico, "de": primario, "para": novo_seletor,
             "confianca": round(confianca, 2)}
        )
        return melhor

    def salvar_relatorio_curas(self):
        if self.curas:
            destino = BASE_DIR / "healed_selectors.json"
            destino.write_text(json.dumps(self.curas, indent=2, ensure_ascii=False))
            print(f"\n📋 Relatório de curas salvo em {destino.name} "
                  f"(use para atualizar os seletores no código!)")
