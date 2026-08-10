# 📋 Detector de Anomalias Estruturais em Binários UEFI

## 🎯 Objetivo da Pesquisa
Desenvolver um motor de inferência não-supervisionado capaz de detectar anomalias estruturais em módulos executáveis UEFI (`.efi`) sem depender de assinaturas estáticas ou análise comportamental em tempo de execução.

## 🔬 Fases do Projeto
Este projeto foi estruturado em três fases incrementais, evoluindo de uma prova de conceito teórica para uma ferramenta de análise funcional.

### Fase 1: Prova de Conceito (Simulada)
O ponto de partida foi validar a hipótese central: é possível usar o Isolation Forest para distinguir binários normais de anômalos com base em características estruturais? Nesta fase, em vez de usar arquivos reais, foram gerados dados sintéticos com `numpy` para simular as *features* (como entropia e tamanho de cabeçalho) de módulos UEFI. O objetivo foi confirmar, em um ambiente controlado, que o modelo matemático era capaz de aprender a "fronteira" da normalidade e isolar os pontos de dados que representavam anomalias.


### Fase 2: Análise de Binários Reais (Engenharia de Dados)
Com a validação teórica concluída, a Fase 2 materializou o projeto. Aqui, o foco foi abandonar os dados sintéticos e interagir com arquivos `.efi` reais. Foi desenvolvido um pipeline de engenharia de dados que utiliza a biblioteca `pefile` para fazer o parsing de binários UEFI compilados a partir do EDK II (a nossa *golden image*). A principal tarefa foi criar um extrator de *features* capaz de ler um arquivo e traduzir sua estrutura — entropia da seção de código, tamanho dos cabeçalhos, número de seções — em um vetor numérico que o modelo de Machine Learning pudesse entender.


### Avaliação
A fase de avaliação integra as duas anteriores. O modelo Isolation Forest é treinado com as características extraídas dos binários legítimos (a *golden image* da Fase 2). Em seguida, seu desempenho é rigorosamente avaliado. O modelo é desafiado a classificar um conjunto de teste que inclui tanto módulos seguros quanto módulos deliberadamente modificados (simulando uma infecção). O sucesso desta fase é medido por meio de um relatório estatístico completo, incluindo a matriz de confusão, acurácia, precisão e, mais importante, o *recall* — a métrica que nos diz quantos dos binários maliciosos foram efetivamente detectados.

## ✅ Definition of Done (DoD)
O projeto será considerado "Concluído" e pronto para apresentação acadêmica quando atender aos seguintes critérios de aceite:

- [ ] **Fase 1 (PoC Teórica):** Lógica matemática do Isolation Forest implementada e validada em dados sintéticos com separação clara de *inliers* (seguros) e *outliers* (anômalos).
- [ ] **Fase 2 (Engenharia de Dados):** Pipeline automatizado construído para extrair, via `pefile`, metadados (Entropia, SizeOfHeaders, NumberOfSections) de binários compilados pelo EDK II.
- [ ] **Fase 3 (Validação):** Modelo avaliado contra um *dataset* de teste (módulos legítimos vs. injetados/ofuscados) com coleta de métricas estatísticas.
- [ ] **Documentação:** README principal redigido com fundamentação teórica (Cálculo de Shannon) e instruções claras de reprodução.
- [ ] **Performance:** O modelo deve atingir um *Recall* mínimo de 90% na detecção de módulos anômalos (priorizando a redução de Falsos Negativos, crítico em cibersegurança).
