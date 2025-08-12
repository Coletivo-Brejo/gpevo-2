# gpevo-2

## Instruções

Para criar o ambiente virtual:

```
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Caso o VS Code tenha problemas para identificar o Python do ambiente virtual, ainda é possível executar os serviços apontando diretamente para o Python virtualizado. Como eles são executados de dentro de suas respectivas pastas, convém criar uma variável de ambiente com o caminho relativo até o Python virtualizado:

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

Para servir o jogo via web:
```
cd build
$PYTHON -m http.server 5000
```

## Roadmap

- [x] Criar pistas no Godot [2025-07-07]
- [x] Carregar e salvar pistas pela API [2025-07-07]
- [x] Exibir pistas no Streamlit [2025-07-07]
- [x] Streamlit com autenticação [2025-07-07]
- [x] Criar nave com chassi, sensores e propulsores [2025-07-09]
- [x] Carregar e salvar naves pela API [2025-07-09]
- [x] Neurônios e operações básicas (e.g. linear, relu, atan) [2025-07-11]
- [x] Instanciar pista com colisão [2025-07-13]
- [x] Neurônios de output (propulsores) [2025-07-13]
- [x] Corredor persistido (nave + cérebro) [2025-07-13]
- [x] [D] Os nodes TrackAPI e ShipAPI são cópia um do outro. Cabe um node genérico. [2025-07-13]
- [x] [D] Os endpoints para ler e escrever pistas e naves são cópia um do outro. Cabe funções genéricas chamadas por ambos. [2025-07-13]
- [x] Neurônios de input (e.g. sensores, telemetria) [2025-07-14]
- [x] Corredor operacional (input + output) [2025-07-14]
- [x] [D] A nave não tem informação de colisão. Precisa de um novo atributo com os pontos do polígono do chassi. [2025-07-14]
- [x] Execução (pista + corredores) com começo e fim [2025-07-16]
- [x] Métricas de desempenho na corrida [2025-07-16]
- [x] Visualização dos resultados da corrida do Streamlit [2025-07-16]
- [x] Pistas com loop e voltas [2025-07-17]
- [x] Pistas espelhadas [2025-07-17]
- [x] Encerrar corrida se corredores ficarem presos [2025-07-18]
- [x] Persistir motivo da conclusão da corrida [2025-07-18]
- [x] Mutação: alterar pesos de conexão neuronal [2025-07-18]
- [x] Treinamento iterativo (execução, avaliação, mutação) [2025-07-18]
- [x] Visualização dos resultados do treinamento no Streamlit [2025-07-20]
- [x] Neurônios centrais (e.g. perceptrons) [2025-07-21]
- [x] Mutação: criar/destruir neurônio [2025-07-21]
- [x] Mutação: criar/destruir conexão neuronal [2025-07-21]
- [x] Visualização do cérebro no Streamlit [2025-07-22]
- [x] Treinamento com avaliação de mais de uma pista ao mesmo tempo (e.g. pista espelhada e não espelhada) [2025-07-25]
- [x] Limitação de profundidade do cérebro durante treinamento [2025-07-27]
- [x] Limitação de quantidade de neurônios durante treinamento [2025-07-27]
- [x] [D] Quando um neurônio é totalmente desconectado dos demais, ele continua registrado no cérebro e é contabilizado para os limites de neurônios. Convém excluí-lo. [2025-07-28]
- [x] Visualização da evolução do cérebro ao longo do treino [2025-07-28]
- [x] Embedding do jogo no Streamlit para executar treinamentos (loucura) [2025-07-29]
- [x] Configuração de treinamento no Streamlit [2025-08-04]
- [x] Persistência de resultados do treinamento a cada iteração [2025-08-05]
- [x] Continuação de treinamento interrompido [2025-08-05]
- [x] Execução de treinamento dentro do Streamlit [2025-08-05]
- [x] Rota para deletar treinamentos (treinamento + entry + runs) [2025-08-06]
- [x] Visualização do histórico de ativações dos neurônios ao longo de uma corrida (eletroencefalograma) [2025-08-06]
- [X] [B] Os neurônios do treino normal e espelhado estão com o mesmo padrão de ativação, provavelmente por algum compartilhamento de dados e recursos entre os cérebros do mesmo clone. Definir cada NeuronData como `local_to_scene` não resolveu o problema, assim como clonar o cérebro também não. [2025-08-06]
- [x] Página de corredor na aplicação [2025-08-07]
- [x] Remoção manual de neurônios e conexões [2025-08-07]
- [x] Atualização indepotente do treinamento [2025-08-12]
- [x] Aviso de treinamento encerrado/interrompido no jogo [2025-08-12]
- [ ] *Registro de "versão" do cérebro do corredor
- [ ] *Continuação do treinamento até a conclusão de todos os clones sem alterar a lógica de aprendizado
- [ ] *Corrida de sondagem
- [ ] *Leaderboard das pistas
- [ ] *Visualização do corredor com indicação de propulsores e sensores
- [ ] Perfis de acesso (sem login, público, gestor de equipe, administrador)
- [ ] Decals para naves
- [ ] Linha de partida e de chegada
- [ ] Calendário de eventos
- [ ] Estrutura de equipe (gestores, corredores, verba, pontuação, cor, etc.)
- [ ] Precificação de treinamentos
- [ ] Fantasmas durante uma execução
- [ ] Equipamentos embaralhadores de sinal
- [ ] Visualização do histórico de colisões ao longo de uma corrida
- [ ] [D] O editor de naves reprocessa tudo a cada frame. Cabe uma detecção menos burra de quando há mudanças para processar.
- [ ] [D] O z-index das partes da nave está todo desordenado, com os thrusters aparecendo por trás de outras naves e as partículas aparecendo por cima do thruster.
- [ ] [D] Em curvas acentuadas e arrastando na parede, as partículas dos thrusters parecem sair em uma direção totalmente errada.
- [ ] [D] Em runs com `finish_on_first_win = True`, a câmera pula para o segundo colocado por um frame quando o primeiro conclui a pista, antes da run ser finalizada. É um efeito visual esquisito.