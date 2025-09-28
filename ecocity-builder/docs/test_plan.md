# Plano de Testes - EcoCity Builder

## 1. Introdução

### 1.1 Objetivo
Este documento define a estratégia de teste para o jogo **EcoCity Builder**, descrevendo abordagens, recursos, cronograma e critérios de avaliação para garantir a qualidade do software.

### 1.2 Escopo
O plano cobre testes para todos os Requisitos Funcionais (RF001-RF010) e Não-Funcionais (RNF001-RNF008), incluindo:

- Testes de Unidade  
- Testes de Integração  
- Testes de Sistema  
- Testes de Aceitação  

---

## 2. Estratégia de Teste

### 2.1 Abordagens
- **Teste Caixa-Branca**: Para componentes internos (classes Cidade, Jogador, etc.)  
- **Teste Caixa-Preta**: Para funcionalidades do usuário final  
- **Teste Baseado em Risco**: Foco em RFs de Alta Prioridade primeiro  

### 2.2 Critérios de Aceitação
- 95% de cobertura de código para classes críticas  
- 0 bugs críticos ou bloqueantes  
- Todos os RFs devem passar nos testes de aceitação  

---

## 3. Casos de Teste Detalhados

### 3.1 Testes para RF001 - Navegação pela Tela Inicial

**TST-RF001-001: Exibição da Tela Inicial**  
- Pré-condições: Jogo instalado e executado  
- Dados de Teste: Nenhum  
- Procedimentos:  
  1. Iniciar o jogo  
  2. Verificar se a tela inicial é exibida  
  3. Validar presença dos botões: "Novo Jogo", "Carregar Jogo", "Configurações", "Sair"  
  4. Verificar se o título do jogo está visível  
- Resultado Esperado: Tela inicial exibida corretamente com todos os elementos  
- Critério de Aceitação: Todos os elementos visíveis e funcionais  
- Prioridade: Alta  

**TST-RF001-002: Navegação por Teclado**  
- Pré-condições: Tela inicial exibida  
- Dados de Teste: Teclas seta para cima/baixo, Enter  
- Procedimentos:  
  1. Pressionar seta para baixo  
  2. Pressionar seta para cima  
  3. Pressionar Enter na opção "Novo Jogo"  
- Resultado Esperado: Navegação entre opções funciona corretamente  
- Critério de Aceitação: Foco muda entre opções e Enter executa ação  
- Prioridade: Alta  

---

### 3.2 Testes para RF002 - Criação de Novo Mundo

**TST-RF002-001: Criação com Dados Válidos**  
- Pré-condições: Tela de criação de mundo aberta  
- Dados de Teste: Nome: "EcoVille", Dificuldade: "Médio"  
- Procedimentos:  
  1. Inserir "EcoVille" no campo nome  
  2. Selecionar "Médio" na dificuldade  
  3. Clicar em "Iniciar"  
- Resultado Esperado: Jogo inicia com cidade "EcoVille" em dificuldade média  
- Critério de Aceitação: Save criado, recursos iniciais configurados  
- Prioridade: Alta  

**TST-RF002-002: Validação de Nome Vazio**  
- Pré-condições: Tela de criação de mundo aberta  
- Dados de Teste: Nome: "", Dificuldade: "Médio"  
- Procedimentos:  
  1. Deixar campo nome vazio  
  2. Clicar em "Iniciar"  
- Resultado Esperado: Mensagem "Por favor, dê um nome à sua cidade" exibida  
- Critério de Aceitação: Sistema não avança e mostra mensagem de erro  
- Prioridade: Alta  

---

### 3.3 Testes para RF005 - Gerenciamento de Recursos

**TST-RF005-001: Atualização Automática de Recursos**  
- Pré-condições: Partida em andamento  
- Dados de Teste: Valores iniciais: Dinheiro=1000, Emissão=50, Satisfação=70  
- Procedimentos:  
  1. Iniciar partida  
  2. Aguardar 60 segundos  
  3. Verificar valores de recursos  
- Resultado Esperado: Recursos atualizados conforme construções/tecnologias  
- Critério de Aceitação: Valores mudam automaticamente  
- Prioridade: Alta  

**TST-RF005-002: Alerta de Recurso Crítico**  
- Pré-condições: Partida em andamento  
- Dados de Teste: Satisfação populacional = 15 (valor crítico)  
- Procedimentos:  
  1. Forçar satisfação para 15  
  2. Verificar alertas visuais  
  3. Verificar alertas sonoros  
- Resultado Esperado: Indicador pisca em vermelho e som de alerta é reproduzido  
- Critério de Aceitação: Alertas ativados corretamente  
- Prioridade: Média  

---

### 3.4 Testes para RF006 - Construção de Infraestruturas

**TST-RF006-001: Construção com Recursos Suficientes**  
- Pré-condições: Recursos suficientes, menu construções aberto  
- Dados de Teste: Custo construção: 500, Dinheiro disponível: 1000  
- Procedimentos:  
  1. Selecionar construção  
  2. Confirmar construção  
  3. Verificar dedução de recursos  
  4. Verificar construção no mapa  
- Resultado Esperado: Construção adicionada, recursos deduzidos, benefícios aplicados  
- Critério de Aceitação: Todos os passos executados corretamente  
- Prioridade: Alta  

**TST-RF006-002: Construção com Recursos Insuficientes**  
- Pré-condições: Recursos insuficientes, menu construções aberto  
- Dados de Teste: Custo construção: 500, Dinheiro disponível: 300  
- Procedimentos:  
  1. Selecionar construção  
  2. Tentar confirmar  
- Resultado Esperado: Botão escurecido, mensagem "Recursos insuficientes"  
- Critério de Aceitação: Sistema impede construção e informa usuário  
- Prioridade: Alta  

---

### 3.5 Testes para RF008 - Eventos Climáticos

**TST-RF008-001: Geração de Evento Aleatório**  
- Pré-condições: Partida em andamento por 10 minutos  
- Dados de Teste: Probabilidade de evento: 20%  
- Procedimentos:  
  1. Aguardar tempo suficiente  
  2. Verificar se evento é gerado  
  3. Validar notificação ao jogador  
- Resultado Esperado: Evento gerado aleatoriamente, jogador notificado  
- Critério de Aceitação: Evento aparece conforme probabilidade  
- Prioridade: Média  

**TST-RF008-002: Timeout de Resposta**  
- Pré-condições: Evento climático ativo  
- Dados de Teste: Timeout: 30 segundos  
- Procedimentos:  
  1. Iniciar evento  
  2. Aguardar 31 segundos sem resposta  
  3. Verificar consequências  
- Resultado Esperado: Sistema aplica consequências padrão, mensagem exibida  
- Critério de Aceitação: Tratamento de timeout funciona corretamente  
- Prioridade: Média  

---

## 4. Testes de Integração

**TST-INT-001: Fluxo Completo Novo Jogo**  
- Componentes: RF001 + RF002 + RF004 + RF005  
- Procedimentos:  
  1. Tela inicial → Novo Jogo → Criar cidade → Jogo principal  
  2. Verificar se salvamento automático ocorre  
  3. Verificar se recursos são gerenciados  
- Resultado Esperado: Fluxo completo sem erros  
- Prioridade: Alta  

**TST-INT-002: Construção + Pesquisa**  
- Componentes: RF006 + RF007  
- Procedimentos:  
  1. Construir infraestrutura  
  2. Pesquisar tecnologia relacionada  
  3. Verificar sinergia entre sistemas  
- Resultado Esperado: Benefícios se complementam  
- Prioridade: Média  

---

## 5. Testes Não-Funcionais

**TST-RNF001-001: Performance com Múltiplas Construções**  
- Requisito: RNF001  
- Procedimentos:  
  1. Adicionar 50 construções  
  2. Medir FPS  
  3. Verificar responsividade  
- Resultado Esperado: FPS mantido acima de 30  
- Critério: Performance não degrada significativamente  
- Prioridade: Alta  

**TST-RNF002-001: Usabilidade da Interface**  
- Requisito: RNF002  
- Procedimentos:  
  1. Teste com usuários novatos  
  2. Medir tempo para realizar tarefas básicas  
  3. Coletar feedback de usabilidade  
- Resultado Esperado: Interface intuitiva e fácil de aprender  
- Critério: Usuários completam tarefas em tempo razoável  
- Prioridade: Alta  

---

## 6. Ambiente de Teste

### 6.1 Configurações
- OS: Windows 10, macOS, Linux  
- Python: 3.8+  
- Hardware Mínimo: 4GB RAM, 2GB espaço  
- Hardware Recomendado: 8GB RAM, GPU básica  

### 6.2 Ferramentas
- Test Runner: pytest  
- Cobertura: coverage.py  
- Mock: unittest.mock  
- UI Testing: pytest-qt  

---

## 7. Cronograma

| Fase   | Data   | Atividades                      |
|--------|-----------|---------------------------------|
| Fase 1 | 00/09/2025  | Testes RF001-RF003              |
| Fase 2 | 00/09/2025 | Testes RF004-RF007              |
| Fase 3 | 00/09/2025  | Testes RF008-RF010 + RNFs       |
| Fase 4 | 00/09/2025  | Testes de Integração            |
| Fase 5 | 00/09/2025  | Testes de Aceitação             |

---

## 8. Critérios de Saída
- Todos os testes de Alta Prioridade passaram  
- Cobertura de código ≥ 80%  
- 0 bugs críticos abertos  
- Documentação de testes atualizada  

---


