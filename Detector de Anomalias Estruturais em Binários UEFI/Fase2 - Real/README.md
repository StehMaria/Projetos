<div align=right style=display:inline-block>
<img width=10% src=http://ForTheBadge.com/images/badges/built-with-love.svg>
<img width=8% src=https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white>
<img width=12% src=https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white>
<img width=15% src=https://img.shields.io/badge/Firmware_Security-2E86C1?style=for-the-badge>
</div>

<h1 align=center>Detector de Anomalias Estruturais em Binários UEFI 🛡️</h1>

### Ferramentas:
* Python 3
* numpy
* scikit-learn
* pefile
* pandas

**Tier:** Avançado ⭐⭐⭐

### Objetivo:

Enquanto a Fase 1 focou na simulação matemática para validar a viabilidade do algoritmo Isolation Forest, esta **Fase 2** materializa a pesquisa através da leitura real da estrutura PE/COFF de binários executáveis EFI (`.efi`).

### User Story:

-   [ ] Como analista de segurança, quero submeter um arquivo `.efi` real para que a ferramenta extraia suas características estruturais e o classifique como seguro ou suspeito.
-   [ ] Como desenvolvedor de firmware, quero compilar uma "golden image" a partir do EDK II e usar esses binários para treinar o modelo, criando uma linha de base de normalidade confiável.
-   [ ] Como membro de uma equipe de resposta a incidentes, quero que a ferramenta me forneça um score de anomalia para um binário suspeito, ajudando a priorizar a análise forense em firmwares potencialmente comprometidos.


### Definition of Done:

-   [ ] Utilizar a biblioteca `pefile` para fazer o parsing de binários `.efi` e extrair features como entropia, tamanho de cabeçalhos e número de seções.
-   [ ] O modelo deve ser treinado com um conjunto de dados de binários UEFI reais e íntegros, compilados a partir do EDK II.
-   [ ] Implementar uma função para calcular a entropia de Shannon a partir dos bytes brutos de uma seção do arquivo PE.
-   [ ] O sistema deve ser capaz de receber o caminho de um arquivo `.efi` como entrada e retornar a classificação ("SEGURO" ou "ANOMALIA DETECTADA") e o score de anomalia.
-   [ ] O projeto deve incluir um exemplo prático que demonstre a análise de um binário legítimo (ex: `DxeCore.efi`) e a detecção de uma anomalia em um binário modificado.
 

## 📋 Sumário
-   [Fundamentos Teóricos](#fundamentos-teóricos)
-   [Projeto](#projeto)
  -   [Sobre](#sobre) 
  -   [Como instalar](#como-instalar) 
  -   [Resultados](#resultados) 
  -   [Links úteis](#links-úteis)

## 🧠 Fundamentos Teóricos

### Estrutura de Arquivos PE/COFF

Nesta fase, a análise deixa de ser uma simulação e passa a interagir com a estrutura real dos binários. Os arquivos executáveis UEFI (`.efi`) seguem o formato **Portable Executable (PE)**, o mesmo padrão utilizado por executáveis e DLLs no Windows.

Compreender essa estrutura é fundamental, pois é dela que extraímos as características (*features*) que alimentarão o modelo de Machine Learning. Em vez de olhar o código em si, analisamos os metadados e a organização do arquivo, como:
*   **Cabeçalhos (Headers):** Contêm informações vitais como o tamanho do código, o tamanho dos dados inicializados e o endereço de início da execução. Anomalias em seus tamanhos podem indicar manipulação.
*   **Tabela de Seções (Section Table):** Descreve as diferentes seções do arquivo (ex: `.text` para código, `.data` para dados). Um número incomum de seções ou seções com nomes suspeitos são fortes indicadores de anomalia.
*   **Tabela de Exportação (Export Table):** A presença ou ausência de funções exportadas é uma característica importante, especialmente em drivers UEFI.

### Entropia de Shannon
O principal indicador utilizado é a entropia das seções executáveis. Códigos nativos não-criptografados possuem previsibilidade. Payloads maliciosos tendem à aleatoriedade quase total. A entropia é calculada pela equação de Shannon:

$$H(X)=-\sum_{i=1}^{n}P(x_i)\log_2P(x_i)$$

Onde $P(x_i)$ representa a probabilidade de ocorrência de um determinado byte $x_i$ na seção analisada. Ao combinarmos a entropia com outras *features* (como proporção do cabeçalho PE e tabela de exportações), podemos modelar o formato exato de um binário "saudável".

### Isolation Forest

O Isolation Forest é um algoritmo de *machine learning* não-supervisionado, projetado especificamente para a detecção de anomalias (*outliers*). Sua lógica é surpreendentemente simples e eficaz: **anomalias são mais fáceis de isolar do que pontos normais**.

O algoritmo funciona da seguinte maneira:
1.  Ele constrói várias "árvores de decisão" aleatórias. Em cada nó da árvore, ele seleciona um atributo (como a entropia) e um valor de corte aleatório.
2.  Ele repete esse processo, dividindo o conjunto de dados até que cada ponto (cada binário, no nosso caso) esteja isolado em seu próprio galho.
3.  A "pontuação de anomalia" de um ponto é baseada no quão rápido ele é isolado. Pontos normais, que são muitos e parecidos, exigem muitos cortes para serem separados. Anomalias, por serem "poucas e diferentes", são isoladas com poucos cortes, resultando em um caminho mais curto na árvore.


**Como isso se aplica ao projeto?**

*   **Firmwares Adulterados são Anomalias:** Um binário UEFI legítimo, compilado a partir do código-fonte, possui características estruturais previsíveis. Quando um ator malicioso injeta um *payload*, ofusca código ou usa um *packer*, ele altera drasticamente essas características (como a entropia). Esse binário modificado se torna uma anomalia estatística em relação ao conjunto de firmwares "saudáveis".
*   **Não Precisamos de Amostras de Malware:** A grande vantagem é que não precisamos de um vasto banco de dados de firmwares maliciosos para treinar o modelo. Basta alimentá-lo com exemplos de binários íntegros (a *golden image*). O algoritmo aprende o que é "normal" e, a partir disso, consegue identificar qualquer coisa que se desvie desse padrão.
*   **Detecção de Ameaças Desconhecidas (Zero-Day):** Como o modelo não se baseia em assinaturas de ameaças conhecidas, ele é capaz de detectar modificações suspeitas nunca antes vistas, oferecendo uma camada de proteção proativa contra ataques novos e sofisticados.


## 💻 Projeto

### Sobre

Nesta etapa, abandonamos os dados estocásticos gerados via Numpy e passamos a extrair *features* puras diretamente de módulos compilados.

1. **Dataset Genuíno:** Utilização do **EDK II (EFI Development Kit)** para compilar módulos legítimos (ex: `DxeCore.efi`, drivers de rede e armazenamento) que servirão como *Golden Image* para o treinamento do modelo.
2. **Engenharia Reversa Automatizada:** Utilização da biblioteca `pefile` para realizar o *parsing* do cabeçalho executável.
3. **Cálculo de Entropia Nativo:** O script varre o *raw data* da seção `.text` (onde reside o código executável) calculando a frequência de bytes reais (0x00 a 0xFF) para obter a pontuação exata de entropia de Shannon.

O coração desta fase é a função de extração. O script entra no nível de bytes do arquivo, identificando:
* O nível de aleatoriedade do código (indicador forte de empacotadores como UPX ou *shellcodes* ofuscados).
* Anomalias estruturais no tamanho do *Optional Header*.
* Variações anormais na contagem de seções PE.

### Como usar

Para esta etapa, deve ter o Python 3 instalado. Para instalar acesse o [link](https://python.org.br/instalacao-windows/).


- Clone o repositório:
``` bash
$ git clone https://github.com/StehMaria/Projetos
```
- Entre no diretório:
``` bash
$ cd Detector de Anomalias Estruturais em Binários UEFI/Fase2 - Real
```

- Para instalar dependências:
``` bash
$ pip install -r requirements.txt
```

- Execute a aplicação:
``` bash
python src/feature_extractor.py
python src/train_model.py
python scr/evaluation.py
```

### Resultados

Em construção ... 

### Links úteis
[Scikit Learn](https://scikit-learn.org/stable/)  
[Numpy](https://numpy.org)  
[Pandas](https://pandas.pydata.org)  
[Isolation Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
