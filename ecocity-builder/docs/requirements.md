# MODELO PARA O DOCUMENTO DE REQUISITOS DO PROJETO

## Requisitos Funcionais

### RF001
**Nome:** Navegação pela Tela Inicial

**Descrição:** O sistema deve apresentar uma tela inicial com opções para iniciar um novo jogo, carregar um jogo existente, acessar configurações e sair do jogo.

**Atores:** Jogador

**Prioridade:** Alta

**Entradas e pré-condições:** O jogo foi iniciado pelo usuário.

**Saídas e pós-condições:** O jogador é redirecionado para a tela escolhida.

**Fluxos de eventos**  
**Fluxo principal:**  
1. O sistema exibe a tela inicial com o título do jogo e um menu com as opções: "Novo Jogo", "Carregar Jogo", "Configurações", "Sair".  
2. O jogador navega pelas opções usando o mouse ou teclado.  
3. O jogador seleciona uma das opções.  
4. O sistema inicia o fluxo correspondente à opção selecionada.

**Fluxo secundário 1 - Novo jogo:**  
4.1. O sistema inicia o fluxo de criação de novo mundo (RF 002).

**Fluxo secundário 2 - Carregar jogo:**  
4.2. O sistema exibe a tela de seleção de save (RF 003).

**Fluxo secundário 3 - Configurações:**  
4.3. O sistema exibe o menu de configurações de áudio e vídeo.

**Fluxo secundário 4 - Sair:**  
4.4. O sistema finaliza a aplicação.

### RF002
**Nome:** Criação de um Novo Mundo

**Descrição:** O sistema deve guiar o jogador na criação de um novo mundo (nova partida), permitindo que ele dê um nome à sua cidade e escolha dificuldade.

**Atores:** Jogador

**Prioridade:** Alta

**Entradas e pré-condições:** O jogador selecionou "Novo Jogo" na tela inicial.

**Saídas e pós-condições:** Um novo arquivo de save é criado e o jogo é iniciado com os parâmetros padrão ou escolhidos pelo jogador.

**Fluxos de eventos**  
**Fluxo principal:**  
1. O sistema exibe uma tela de criação, com um campo para inserir o nome da cidade e opções de dificuldade (ex.: Fácil, Médio, Difícil).  
2. O jogador insere um nome para a cidade.  
3. O jogador seleciona um nível de dificuldade (a seleção padrão é "Médio").  
4. O jogador clica no botão "Iniciar".  
5. O sistema cria um novo arquivo de save com um ID único, armazenando o nome da cidade, a dificuldade e os valores iniciais padrão para todos os recursos e construções.  
6. O sistema inicia a simulação do mundo e exibe a tela principal do jogo (interface de cidade e recursos).

**Fluxo secundário 1 - Nome inválido:**  
2.1. Se o jogador tentar prosseguir sem inserir um nome, o sistema exibe uma mensagem: "Por favor, dê um nome à sua cidade."  
2.2. O fluxo retorna ao passo 2.

### RF003
**Nome:** Carregamento de um Jogo Existente

**Descrição:** O sistema deve permitir que o jogador visualize e selecione um save game anterior para continuar sua partida.

**Atores:** Jogador

**Prioridade:** Alta

**Entradas e pré-condições:** O jogador selecionou "Carregar Jogo" na tela inicial. Deve existir pelo menos um arquivo de save válido.

**Saídas e pós-condições:** O save selecionado é carregado e o jogo é iniciado do ponto exato onde foi salvo.

**Fluxos de eventos**  
**Fluxo principal:**  
1. O sistema verifica a pasta de saves padrão por arquivos de save válidos.  
2. O sistema exibe uma lista vertical de saves disponíveis. Cada entrada na lista mostra: Nome da Cidade, Data/Hora do último salvamento, e um screenshot em miniatura do mundo.  
3. O jogador navega pela lista e seleciona o save que deseja carregar.  
4. O jogador clica no botão "Carregar".  
5. O sistema lê os dados do arquivo de save selecionado.  
6. O sistema popula o estado do jogo (recursos, construções, tecnologias, etc.) com os dados carregados.  
7. O sistema inicia a simulação do mundo e exibe a tela principal do jogo.

**Fluxo secundário 1 - Nenhum save encontrado:**  
1.1. Se não forem encontrados arquivos de save, o sistema exibe a mensagem: "Nenhum jogo salvo encontrado."  
1.2. O sistema oferece um botão "Voltar" que, quando clicado, retorna o jogador à tela inicial (RF 001).

**Fluxo de exceção 2 - Save corrompido:**  
5.1. Se o arquivo de save estiver corrompido ou for inválido, o sistema exibe uma mensagem de erro: "Não foi possível carregar o jogo selecionado. O arquivo pode estar corrompido."  
5.2. O sistema oferece um botão "OK" que, quando clicado, retorna o jogador para a lista de saves (passo 2).

### RF004
**Nome:** Salvamento Automático e Manual do Progresso

**Descrição:** O sistema deve salvar o progresso do jogador automaticamente em intervalos regulares e permitir um salvamento manual a qualquer momento a partir do menu de pausa.

**Atores:** Sistema, Jogador

**Prioridade:** Média

**Entradas e pré-condições:** Uma partida deve estar em andamento.

**Saídas e pós-condições:** O estado atual do jogo é persistido em um arquivo de save.

**Fluxos de eventos**  
**Fluxo principal:**  
1. Durante a partida, o sistema inicia um temporizador para salvamento automático (ex.: a cada 5 minutos).  
2. Quando o temporizador expira, o sistema cria um backup do save anterior e sobrescreve o arquivo de save atual com o estado do jogo no momento.  
3. O sistema exibe brevemente uma notificação discreta na tela: "Jogo Salvo Automaticamente."

**Fluxo secundário 1 - Salvamento Manual:**  
1. O jogador abre o menu de pausa clicando em um botão dedicado ou pressionando a tecla "ESC".  
2. O jogador seleciona a opção "Salvar Jogo".  
3. O sistema sobrescreve o arquivo de save atual com o estado do jogo no momento.  
4. O sistema exibe uma mensagem de confirmação: "Progresso salvo com sucesso!"  
5. O menu de pausa permanece aberto.

### RF005
**Nome:** Gerenciamento de Recursos Básicos

**Descrição:** O sistema deve permitir ao jogador gerenciar três recursos principais: dinheiro, emissão de carbono e satisfação populacional.

**Atores:** Jogador

**Prioridade:** Alta

**Entradas e pré-condições:** O jogador deve ter iniciado uma partida.

**Saídas e pós-condições:** Os recursos são atualizados em tempo real conforme as ações do jogador.

**Fluxos de eventos**  
**Fluxo principal:**  
1. O sistema exibe os níveis atuais de dinheiro, emissão de carbono e satisfação populacional.  
2. O jogador visualiza as mudanças nos recursos conforme o tempo passa.  
3. O sistema atualiza os valores automaticamente baseado nas construções e tecnologias implementadas.

**Fluxo secundário 1 - Recurso crítico:**  
1. Se o nível de satisfação populacional atingir um valor crítico (muito baixo), o sistema exibe um alerta visual (ex: o indicador pisca em vermelho) e sonoro.  
2. Se a emissão de carbono atingir um nível crítico (muito alto), o sistema desencadeia efeitos negativos mais severos (ex: multas, desastres ambientais mais frequentes).

### RF006
**Nome:** Construção de Infraestruturas Verdes

**Descrição:** O sistema deve permitir ao jogador construir e melhorar infraestruturas sustentáveis.

**Atores:** Jogador

**Prioridade:** Alta

**Entradas e pré-condições:** O jogador deve ter recursos suficientes para construir ou melhorar.

**Saídas e pós-condições:** A infraestrutura é adicionada ou melhorada, com impactos nos recursos.

**Fluxos de eventos**  
**Fluxo principal:**  
1. O jogador acessa o menu de construções.  
2. O sistema exibe as opções disponíveis com seus custos e benefícios.  
3. O jogador seleciona uma construção para adicionar ou melhorar.  
4. O sistema deduz os recursos necessários.  
5. A construção é adicionada ao mapa da cidade.  
6. Os recursos são ajustados conforme os benefícios da construção.

**Fluxo secundário 1 - Recursos insuficientes:**  
3.1. Se o jogador selecionar uma construção mas não tiver recursos suficientes, o sistema:  
   - Escurece o botão de confirmação.  
   - Exibe uma mensagem de feedback: "Recursos insuficientes para construir isto."  
   - O fluxo retorna ao passo 2 (menu de construções ainda aberto).

**Fluxo secundário 2 - Cancelamento:**  
3.2. O jogador pode clicar no botão "Voltar" ou "Cancelar" a qualquer momento durante a seleção.  
3.3. O sistema fecha o menu de construções e retorna à visualização normal da cidade sem fazer nenhuma dedução de recursos.

### RF007
**Nome:** Pesquisa de Tecnologias Limpas

**Descrição:** O sistema deve permitir ao jogador investir em pesquisa de tecnologias sustentáveis.

**Atores:** Jogador

**Prioridade:** Média

**Entradas e pré-condições:** O jogador deve ter recursos suficientes e pré-requisitos necessários.

**Saídas e pós-condições:** A tecnologia é pesquisada, desbloqueando novos benefícios.

**Fluxos de eventos**  
**Fluxo principal:**  
1. O jogador acessa a árvore de tecnologias.  
2. O sistema exibe as tecnologias disponíveis para pesquisa.  
3. O jogador seleciona uma tecnologia para pesquisar.  
4. O sistema inicia um contador de tempo para conclusão da pesquisa.  
5. Após conclusão, a tecnologia é desbloqueada e seus benefícios aplicados.

**Fluxo secundário 1 - Pré-requisitos não atendidos:**  
3.1. Se o jogador selecionar uma tecnologia que requer outra tecnologia não pesquisada:  
   - O sistema exibe uma mensagem: "Pré-requisito necessário: [Nome da Tecnologia Requerida]".  
   - O jogador não pode iniciar a pesquisa.  
   - O fluxo retorna ao passo 2.

**Fluxo secundário 2 - Recursos insuficientes:**  
3.2. Se o jogador selecionar uma tecnologia mas não tiver recursos suficientes, o sistema exibe a mensagem: "Recursos insuficientes para pesquisar." O fluxo retorna ao passo 2.

### RF008
**Nome:** Eventos Climáticos Aleatórios

**Descrição:** O sistema deve gerar eventos climáticos aleatórios que afetam a cidade.

**Atores:** Sistema, Jogador

**Prioridade:** Média

**Entradas e pré-condições:** Partida em andamento.

**Saídas e pós-condições:** O evento é resolvido, com consequências positivas ou negativas.

**Fluxos de eventos**  
**Fluxo principal:**  
1. O sistema gera aleatoriamente um evento climático.  
2. O sistema notifica o jogador sobre o evento e suas possíveis consequências.  
3. O jogador escolhe como responder ao evento.  
4. O sistema aplica as consequências da escolha do jogador.

**Fluxo secundário 1 - Sem resposta:**  
3.1. Se o jogador não selecionar uma opção dentro de um tempo limite (ex: 30 segundos):  
   - O sistema interpreta como "Nenhuma ação foi tomada".  
   - O sistema aplica as consequências padrão (geralmente as piores) do evento por inação.  
   - O sistema exibe uma mensagem: "O tempo para agir se esgotou! [Consequência]."

### RF009
**Nome:** Sistema de Achievements Educativos

**Descrição:** O sistema deve oferecer conquistas relacionadas a ações sustentáveis.

**Atores:** Jogador

**Prioridade:** Baixa

**Entradas e pré-condições:** O jogador realiza ações no jogo.

**Saídas e pós-condições:** Conquista é desbloqueada e exibida para o jogador.

**Fluxos de eventos**  
**Fluxo principal:**  
1. O jogador realiza uma ação que corresponde a um critério de conquista.  
2. O sistema verifica se os critérios foram atendidos.  
3. A conquista é desbloqueada e uma notificação é exibida.  
4. Informações educativas relacionadas à conquista são mostradas.

**Fluxo secundário 1 - Visualizar conquistas:**  
1. O jogador acessa o menu principal e seleciona "Conquistas".  
2. O sistema exibe uma lista com todas as conquistas, separadas por "Desbloqueadas" e "Bloqueadas".  
3. Para as conquistas bloqueadas, o sistema mostra uma dica ou o progresso atual em direção ao seu desbloqueio (ex: "5/10 Usinas Solares construídas").  
4. O jogador pode selecionar qualquer conquista desbloqueada para reler sua informação educativa.

### RF010
**Nome:** Painel de Estatísticas e Impacto

**Descrição:** O sistema deve exibir estatísticas detalhadas sobre o impacto ambiental das ações do jogador.

**Atores:** Jogador

**Prioridade:** Média

**Entradas e pré-condições:** Partida em andamento.

**Saídas e pós-condições:** Painel com informações detalhadas é exibido.

**Fluxos de eventos**  
**Fluxo principal:**  
1. O jogador acessa o painel de estatísticas.  
2. O sistema exibe métricas detalhadas sobre emissões reduzidas, energia limpa gerada, etc.  
3. O sistema mostra comparações com cenários do mundo real.  
4. O jogador pode visualizar gráficos evolutivos do progresso.

**Fluxo secundário 1 - Saída:**  
4.1. O jogador clica no botão "Voltar" ou "X".  
4.2. O sistema fecha o painel de estatísticas e retorna à visualização normal da cidade.

## Requisitos Não Funcionais

### RNF001
**Nome:** Performance e Responsividade

**Descrição:** O jogo deve manter uma taxa de atualização constante mesmo com muitas construções e eventos.

**Prioridade:** Alta

### RNF002
**Nome:** Usabilidade e Interface Intuitiva

**Descrição:** A interface deve ser fácil de usar e entender, com informações claras e acessíveis.

**Prioridade:** Alta

### RNF003
**Nome:** Precisão das Informações Científicas

**Descrição:** Os dados e informações sobre mudança climática devem ser precisos e baseados em fontes confiáveis.

**Prioridade:** Alta

### RNF004
**Nome:** Compatibilidade com Múltiplas Plataformas

**Descrição:** O jogo deve ser executado em pelo menos Windows, macOS e Linux.

**Prioridade:** Média

### RNF005
**Nome:** Progressão Balanceada

**Descrição:** A curva de progressão do jogo deve ser bem balanceada, mantendo o jogador engajado.

**Prioridade:** Média

### RNF006
**Nome:** Baixo Consumo de Recursos

**Descrição:** O jogo deve consumir poucos recursos do sistema para permitir execução em máquinas menos potentes.

**Prioridade:** Média

### RNF007
**Nome:** Salvamento Automático

**Descrição:** O progresso do jogador deve ser salvo automaticamente em intervalos regulares.

**Prioridade:** Média

### RNF008
**Nome:** Acessibilidade

**Descrição:** O jogo deve incluir opções de acessibilidade como ajuste de tamanho de texto e opções de daltonismo.

**Prioridade:** Baixa