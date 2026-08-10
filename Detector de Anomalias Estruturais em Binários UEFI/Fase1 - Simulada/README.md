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

Uma Prova de Conceito (PoC) para detecção de anomalias e adulterações em binários de firmware (UEFI/BIOS) utilizando **Machine Learning (Isolation Forest)** baseado puramente na estrutura matemática dos arquivos PE/COFF, sem a necessidade de varredura de assinaturas estáticas.

### User Story:

-   [ ] Como analista de segurança de firmware, quero avaliar um binário UEFI para identificar se ele possui anomalias estruturais que indiquem adulteração.
-   [ ] Como desenvolvedor de sistemas, quero treinar um modelo de machine learning com uma base de firmwares confiáveis (*golden image*) para estabelecer uma linha de base de normalidade.
-   [ ] Como profissional de cibersegurança, quero que a ferramenta classifique um módulo como "normal" ou "anômalo" e forneça um *score* de confiança para priorizar a análise.

### Definition of Done:

-   [ ] Utilizar o algoritmo **Isolation Forest** para a detecção de anomalias.
-   [ ] O modelo deve ser treinado com um conjunto de dados que simula as características de binários UEFI íntegros.
-   [ ] O sistema deve ser capaz de analisar um novo binário e classificá-lo como "SEGURO" ou "ANOMALIA DETECTADA".
-   [ ] A análise deve retornar um *score* de anomalia que justifique a classificação.
-   [ ] O projeto deve incluir uma simulação que demonstre a detecção de um módulo suspeito e a aceitação de um módulo íntegro.
 

## 📋 Sumário
-   [Fundamentos Teóricos](#fundamentos-teóricos)
-   [Projeto](#projeto)
  -   [Sobre](#sobre) 
  -   [Como instalar](#como-instalar) 
  -   [Resultados](#resultados) 
  -   [Links úteis](#links-úteis)

## 🧠 Fundamentos Teóricos

### Entropia de Shannon
O principal indicador utilizado é a entropia das seções executáveis. Códigos nativos não-criptografados possuem previsibilidade. Payloads maliciosos tendem à aleatoriedade quase total. A entropia é calculada pela equação de Shannon:

$$H(X)=-\sum_{i=1}^{n}P(x_i)\log_2P(x_i)$$

Onde $P(x_i)$ representa a probabilidade de ocorrência de um determinado byte $x_i$ na seção analisada. Ao combinarmos a entropia com outras *features* (como proporção do cabeçalho PE e tabela de exportações), podemos modelar o formato exato de um binário "saudável".

### Isolation Forest

O Isolation Forest é um algoritmo de *machine learning* não-supervisionado, projetado especificamente para a detecção de anomalias (*outliers*). Sua lógica é simples e eficaz: **anomalias são mais fáceis de isolar do que pontos normais**.

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

Rootkits de nível de firmware (ex: *BlackLotus*, *LoJax*) operam injetando código malicioso em módulos legítimos da BIOS. Antivírus tradicionais possuem visibilidade quase nula nesse nível (Ring -2). A análise estática baseada em hashes é ineficaz contra ataques *fileless* ou mutantes.

Em vez de analisar o código-fonte ou buscar strings específicas, este projeto extrai **metadados estruturais** do binário `.efi`. Módulos infectados ou que contêm payloads ofuscados/criptografados apresentam anomalias matemáticas detectáveis em sua estrutura.

Esta PoC utiliza o algoritmo **Isolation Forest**, que é não-supervisionado. 
1. **Treinamento (Golden Image):** O modelo é alimentado com as características matemáticas de dezenas de módulos UEFI íntegros. Ele aprende a "fronteira de normalidade".
2. **Inferência:** Ao receber um novo binário, o modelo calcula a distância estrutural. Se o arquivo possuir entropia artificialmente alta ou uma estrutura PE deformada, ele é isolado como uma anomalia (Score negativo).

### Como usar

Para esta etapa, deve ter o Python 3 instalado. Para instalar acesse o [link](https://python.org.br/instalacao-windows/).


- Clone o repositório:
``` bash
$ git clone https://github.com/StehMaria/Projetos
```
- Entre no diretório:
``` bash
$ cd Detector de Anomalias Estruturais em Binários UEFI/Fase1 - Simulado
```

- Para instalar dependências:
``` bash
$ pip install -r requirements.txt
```

- Execute a aplicação:
``` bash
python src/anomaly_model.py
```

### Resultados

Em construção ... 

### Links úteis
[Scikit Learn](https://scikit-learn.org/stable/)  
[Numpy](https://numpy.org)  
[Pandas](https://pandas.pydata.org)  
[Isolation Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)