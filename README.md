# Auto-healing de Seletores

Atividade prática sobre **self-healing selectors** (mesma ideia do
[Healenium](https://healenium.io/) e do [Testim](https://www.testim.io/)):
quando a UI muda e um seletor "quebra", o teste tenta se recuperar sozinho,
procurando o elemento mais parecido com o que era esperado, em vez de falhar
na hora.

Tudo acontece dentro do [painel.html](painel.html), direto no navegador — sem
terminal, sem instalar nada.

## Clonar e abrir

```bash
git clone https://github.com/RodriguesClaudiane/AutoHealing.git
cd AutoHealing/demo-auto-healing
```

Depois, abra o `painel.html` direto no navegador com um comando:

```bash
# Padrão
python3 abrir_painel.py

### Se não funcionar, tente:

# Linux (com ambiente gráfico nativo)
xdg-open painel.html

# WSL (Windows Subsystem for Linux) — não tem navegador instalado nele
# mesmo, então precisa chamar o explorer.exe do Windows
explorer.exe "$(wslpath -w painel.html)"

# macOS
open painel.html

# Windows (PowerShell ou CMD)
start painel.html
```

## O painel mostra:

- um **editor** com o `app.html` (é o único trecho que você vai editar);
- uma **pré-visualização ao vivo** da página, à direita/abaixo do editor;
- o toggle **Auto-healing** (Desligado / Ligado) e o botão **▶ Rodar teste**;
- o **passo a passo** da execução: qual seletor foi buscado, se curou ou
  falhou, a tabela de fingerprint com o gauge de confiança, e o log completo.

## Bora testar?

Edite o HTML no editor, ajuste o toggle **Auto-healing**, clique em
**▶ Rodar teste** e veja o resultado no passo a passo. Use o botão
**Restaurar original** pra voltar ao ponto de partida a qualquer momento.

**1. Baseline** — com o HTML original (como o painel já abre), rode o teste
com o toggle em qualquer posição. Os três campos devem aparecer como
"encontrado diretamente" — nenhuma cura necessária.

**2. Refactor de `id`** — troque os três `id`s (ex.: `username` →
`user-email`, `password` → `user-pass`, `btn-login` → `submit-button`), mas
mantenha `name`, `type` e `placeholder` como estão.
- Com **Desligado**: o resolver fica vermelho e o passo mostra
  `ElementNotFound` — o teste aborta no primeiro seletor.
- Com **Ligado**: o resolver mostra a cura (`seletor antigo → novo`), a
  tabela de fingerprint aparece com o gauge de confiança acima do mínimo, e o
  teste passa.

**3. Quebra parcial** — além do `id`, mude também o `placeholder` de um
campo (só o texto, mantendo `name`/`type`). Rode com **Ligado** e observe no
gauge se a confiança ainda passa da marca de 60%.

**4. Quebra sem cura possível** — num campo, troque `id`, `name` e apague o
`placeholder` ao mesmo tempo (ou apague o campo inteiro). Mesmo com
**Ligado**, o teste deve falhar: o gauge fica abaixo da marca de 60% e o
passo mostra que nenhum candidato foi bom o suficiente.

Use os controles **‹ › ▶ ⟲** abaixo do botão de rodar pra andar passo a
passo pela execução e comparar o log completo de cada tentativa.
