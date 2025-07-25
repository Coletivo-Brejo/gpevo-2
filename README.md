# gpevo-2

## Roadmap

### Prova de conceito

- [x] Criar pistas no Godot [2025-07-07]
- [x] Carregar e salvar pistas pela API [2025-07-07]
- [x] Exibir pistas no Streamlit [2025-07-07]
- [x] Streamlit com autenticação [2025-07-07]
- [x] Instanciar pista com colisão [2025-07-13]
- [x] Criar nave com chassi, sensores e propulsores [2025-07-09]
- [x] Carregar e salvar naves pela API [2025-07-09]
- [x] Neurônios e operações básicas (e.g. linear, relu, atan) [2025-07-11]
- [x] Neurônios de input (e.g. sensores, telemetria) [2025-07-14]
- [x] Neurônios de output (propulsores) [2025-07-13]
- [x] Neurônios centrais (e.g. perceptrons) [2025-07-21]
- [x] Corredor persistido (nave + cérebro) [2025-07-13]
- [x] Corredor operacional (input + output) [2025-07-14]
- [x] Visualização do cérebro no Streamlit [2025-07-22]
- [x] Pistas com loop e voltas [2025-07-17]
- [x] Pistas espelhadas [2025-07-17]
- [x] Execução (pista + corredores) com começo e fim [2025-07-16]
- [x] Métricas de desempenho na corrida [2025-07-16]
- [x] Visualização dos resultados da corrida do Streamlit [2025-07-16]
- [x] Encerrar corrida se corredores ficarem presos [2025-07-18]
- [x] Persistir motivo da conclusão da corrida [2025-07-18]
- [x] Mutação: criar/destruir neurônio [2025-07-21]
- [x] Mutação: criar/destruir conexão neuronal [2025-07-21]
- [x] Mutação: alterar pesos de conexão neuronal [2025-07-18]
- [x] Treinamento iterativo (execução, avaliação, mutação) [2025-07-18]
- [ ] Configuração de treinamento no Streamlit
- [x] Visualização dos resultados do treinamento no Streamlit [2025-07-20]
- [ ] Visualização da evolução do cérebro ao longo do treino

### Jogo de fato

- [ ] Decals para naves
- [ ] Linha de partida e de chegada
- [ ] Perfis de acesso (sem login, público, gestor de equipe, administrador)
- [ ] Calendário de eventos
- [ ] Estrutura de equipe (gestores, corredores, verba, pontuação, cor, etc.)
- [ ] Precificação de treinamentos
- [x] Treinamento com avaliação de mais de uma pista ao mesmo tempo (e.g. pista espelhada e não espelhada) [2025-07-25]
- [ ] Fantasmas durante uma execução
- [ ] Equipamentos embaralhadores de sinal
- [ ] Limitação de profundidade do cérebro durante treinamento
- [ ] Limitação de quantidade de neurônios durante treinamento

### Dívida técnica

- [x] Os nodes TrackAPI e ShipAPI são cópia um do outro. Cabe um node genérico. [2025-07-13]
- [x] Os endpoints para ler e escrever pistas e naves são cópia um do outro. Cabe funções genéricas chamadas por ambos. [2025-07-13]
- [ ] O editor de naves reprocessa tudo a cada frame. Cabe uma detecção menos burra de quando há mudanças para processar.
- [x] A nave não tem informação de colisão. Precisa de um novo atributo com os pontos do polígono do chassi. [2025-07-14]
- [ ] O z-index das partes da nave está todo desordenado, com os thrusters aparecendo por trás de outras naves e as partículas aparecendo por cima do thruster.
- [ ] Em curvas acentuadas e arrastando na parede, as partículas dos thrusters parecem sair em uma direção totalmente errada.

### Bugs

## Instruções

Para rodar a API:

```
cd api
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
fastapi dev api.py
```

Caso o VS Code tenha problemas com o ambiente virtual, é possível executar tanto a API quanto a aplicação apontando diretamente para o Python virtualizado. Como ambos são executados de dentro de suas respectivas pastas, convém criar uma variável de ambiente com o caminho relativo até o Python virtualizado:

```
export PYTHON=../.venv/Scripts/python.exe
```

Para executar a API:

```
cd api
$PYTHON -m fastapi dev api.py
```

Para executar a aplicação:

```
cd app
$PYTHON -m streamlit run app.py
```