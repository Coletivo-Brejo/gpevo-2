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
- [ ] Decals para naves
- [x] Neurônios e operações básicas (e.g. linear, relu, atan) [2025-07-11]
- [ ] Neurônios de input (e.g. sensores, telemetria)
- [ ] Neurônios de output (propulsores)
- [ ] Neurônios centrais (e.g. perceptrons)
- [ ] Corredor persistido (nave + cérebro)
- [ ] Corredor operacional (input + output)
- [ ] Visualização do cérebro (Streamlit + Godot)
- [ ] Pistas com loop e voltas
- [ ] Pistas espelhadas
- [ ] Métricas de desempenho na corrida
- [ ] Treinamento iterativo (execução, avaliação, mutação)
- [ ] Configuração de treinamento no Streamlit

### Dívida técnica

- [ ] Os nodes TrackAPI e ShipAPI são cópia um do outro. Cabe um node genérico.
- [ ] Os endpoints para ler e escrever pistas e naves são cópia um do outro. Cabe funções genéricas chamadas por ambos.
- [ ] O editor de naves reprocessa tudo a cada frame. Cabe uma detecção menos burra de quando há mudanças para processar.
- [ ] A nave não tem informação de colisão. Precisa de um novo atributo com os pontos do polígono do chassi.

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