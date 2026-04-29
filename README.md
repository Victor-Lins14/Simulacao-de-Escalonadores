# Simulador de Escalonamento de CPU

Este projeto é um simulador interativo desenvolvido para seminários da disciplina de Sistemas Operacionais. Ele calcula e visualiza o escalonamento de processos na CPU, gerando o **Gráfico de Gantt** e as métricas de tempo de forma automática.

## Algoritmos Implementados
- **Round Robin (RR):** Preemptivo, baseado em um *Quantum* de tempo (fatia de tempo).
- **SRTF (Shortest Remaining Time First):** Preemptivo, prioriza o processo que tem o menor tempo restante de execução.

## Como Executar
O simulador foi desenvolvido em duas versões idênticas visualmente e em funcionalidades:

1. **Versão Python:** Interface desktop construída com `Tkinter`.
   - Para rodar, execute o arquivo `src/PY/main.py` utilizando o Python 3.

2. **Versão Web (JS):** Interface em HTML, CSS e JavaScript puro.
   - Para rodar, basta dar um duplo clique no arquivo `index.html` na raiz do projeto (ou dentro da pasta `src/JS`) para abrir no seu navegador padrão.

## Métricas Calculadas
- Tempo de Conclusão (Completion Time)
- Tempo de Turnaround
- Tempo de Espera (Waiting Time)
- TME (Tempo Médio de Espera) e TMT (Tempo Médio de Turnaround)

## Site : https://victor-lins14.github.io/Simulacao-de-Escalonadores/src/JS/index.html
