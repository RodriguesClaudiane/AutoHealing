# Auto-healing de Seletores

Atividade prática sobre **self-healing selectors** (mesma ideia do
[Healenium](https://healenium.io/) e do [Testim](https://www.testim.io/)):
quando a UI muda e um seletor "quebra", o teste tenta se recuperar sozinho,
procurando o elemento mais parecido com o que era esperado, em vez de falhar
na hora.

- [main.py](main.py) roda o teste de login contra [app.html](app.html).
- [selectors.json](selectors.json) guarda o seletor original de cada campo
  (não mexa nele).
- O único arquivo que você vai editar é o [app.html](app.html).

## Preparar o ambiente

Só precisa de **Python 3.10+**, sem dependências externas.

```bash
python3 --version      # confirme que o Python está instalado
cd demo-auto-healing
python3 main.py         # deve rodar 2x e terminar em ✅ TESTE PASSOU
```

Se os dois passos acima passaram, o ambiente está pronto.

Se preferir uma versão visual, sem terminal, abra `python3 abrir_painel.py`
(ou dê duplo clique em [painel.html](painel.html)) — mesma atividade, rodando
no navegador.

## Desafio

Faça cada etapa editando o `app.html`, depois rode o comando indicado.

| Comando | O que faz |
|---|---|
| `python3 main.py` | Roda ligado **e** desligado, em sequência |
| `python3 main.py --healing ligado` | Roda só com auto-healing |
| `python3 main.py --healing desligado` | Roda só sem auto-healing |

**1. Baseline** — rode `python3 main.py` sem mexer em nada. As duas rodadas
devem passar sem nenhuma cura (os ids ainda batem com `selectors.json`).

**2. Refactor de `id`** — troque os três ids (ex.: `username` →
`user-email`, `password` → `user-pass`, `btn-login` → `submit-button`), mas
mantenha `name`, `type` e `placeholder` como estão.
- `--healing desligado` → falha com `ElementNotFound` no primeiro seletor.
- `--healing ligado` → passa: o motor acha os elementos pela fingerprint e
  gera um `healed_selectors.json` com o "de → para" de cada cura.

**3. Quebra parcial** — além do `id`, mude também o `placeholder` de um
campo (ex. só o texto, mantendo `name`/`type`). Rode com healing ligado e
observe no terminal se a confiança ainda passa dos 60% (`CONFIANCA_MINIMA`).

**4. Quebra sem cura possível** — num campo, troque `id`, `name` e apague o
`placeholder` ao mesmo tempo (ou apague o campo inteiro). Mesmo com
`--healing ligado`, o teste deve falhar: nenhum candidato chega perto o
suficiente do esperado.

**5. Ambiguidade** — duplique um `<input>` parecido com outro (mesmo `type`,
`placeholder` parecido). Rode com healing ligado e veja qual dos dois o
motor escolhe como melhor candidato.

**6. Fronteira do limiar** — ajuste os atributos de um campo até a confiança
impressa ficar bem perto de 60%, pra ver o exato ponto em que ele vira cura
válida ou falha.

Depois de cada etapa, use `python3 main.py` (sem argumento) pra comparar
ligado vs. desligado lado a lado contra o mesmo `app.html` quebrado.
