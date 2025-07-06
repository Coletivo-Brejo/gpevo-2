# gpevo-2

## Roadmap

### Prova de conceito

- [ ] Criar pistas no Godot
- [ ] Carregar e salvar pistas pela API
- [ ] Exibir pistas no Streamlit

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
PYTHON -m fastapi dev api.py
```

Para executar a aplicação:

```
cd app
PYTHON -m streamlit run app.py
```