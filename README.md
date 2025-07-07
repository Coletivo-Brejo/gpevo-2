# gpevo-2

## Roadmap

### Prova de conceito

- [x] Criar pistas no Godot [2025-07-07]
- [x] Carregar e salvar pistas pela API [2025-07-07]
- [x] Exibir pistas no Streamlit [2025-07-07]
- [ ] Instanciar pista com colisão
- [ ] Criar nave com propulsores
- [ ] Criar cérebro e neurônios básicos
- [ ] Persistir corredor (nave + cérebro)
- [x] Adicionar autenticação ao Streamlit [2025-07-07]

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