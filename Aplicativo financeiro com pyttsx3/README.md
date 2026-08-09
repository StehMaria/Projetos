<div align=right style=display:inline-block>
<img width=10% src=http://ForTheBadge.com/images/badges/built-with-love.svg>
<img width=15% src=http://ForTheBadge.com/images/badges/made-with-python.svg>
<img width=15% src=https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter>
</div>

<h1 align=center>Aplicativo financeiro em Python 💰</h1>

### Ferramentas:
* Python 3
* Anaconda
* Jupyter Notebook

**Tier:** Intermediário ⭐⭐

### Objetivo:
Uma empresa especializada em softwares para deficientes visuais está desenvolvendo um aplicativo financeiro em Python, que permitirá um maior controle financeiro do usuário.

### User Story:

-   [ ] Como usuário, quero digitar um valor e ouvir em voz alta, para controle financeiro.
-   [ ] Como empresa, quero que a entrada do usuário seja modulável, deve permitir futuramente expandir para números maiores do que mil.
-   [ ] Como empresa, quero validar se o valor de entrada está dentro do limite estabelecido.

### Definition of Done:

-   [ ] O software precisa ler as informações que aparecem na tela em voz alta.
-   [ ] O software precisa ser modulável e expandir para números maiores que mil.
-   [ ] O software tem que receber um valor numérico em reais, entre 0,01 e 999,99 (sem "R$").
-   [ ] O software precisa ter essas respostas:
 

## 📋 Sumário
-   [Sobre](#sobre)
-   [Como instalar](#como-instalar)
-   [Como usar](#como-usar)
-   [Links úteis](#links-uteis)


### Sobre

Este projeto apresenta um protótipo de aplicativo financeiro desenvolvido em Python, focado em acessibilidade para usuários com deficiência visual. O objetivo principal é permitir que o usuário digite um valor monetário e o ouça em voz alta, proporcionando um controle financeiro mais autônomo e inclusivo.

A funcionalidade central do aplicativo envolve a conversão de valores numéricos em reais (com um limite inicial de 0,01 a 999,99) para sua representação por extenso, que é então vocalizada. Para isso, utilizamos a biblioteca `pyttsx3`, que transforma texto em fala.

Um aspecto crucial do desenvolvimento é a modularidade da entrada de dados. Embora a versão inicial opere dentro de um limite específico, o design do software prevê a fácil expansão para lidar com números maiores que mil no futuro, garantindo a adaptabilidade e escalabilidade do sistema.

O projeto foi desenvolvido utilizando Python 3, Anaconda e Jupyter Notebook, e simula as seguintes interações:

- 1,01 = "um real e um centavo"  
- 50,23 = "cinquenta reais e vinte e três centavos"  
- 873,00 = "oitocentos e setenta e três reais" 

### Como instalar

Para que o notebook funcione, é necessário que tenha instalado a plataforma Anaconda. Depois de instalar, baixe o código no github.  

1. Abra o prompt de comando do Anaconda.
2. Vá até a pasta onde o arquivo do github foi salvo:
```bash
cd Nome_da_pasta
```
3. Digite no terminal o comando:
```bash
jupyter notebook
```
4. Aguarde um pouco e no seu navegador irá abrir a plataforma Jupyter Notebook na pasta onde está o arquivo. Abra o arquivo e clique em run ▶ para executar as células.

### Como usar

Após executar as células, irá aparecer um *input* para digitar o valor desejado, que deve ser de 0,01 até 999,99. Para deixar a função modulável, descomente as linhas comentadas, comente as que estão informadas e execute novamente.


### Links úteis

[Anaconda](https://www.anaconda.com/products/distribution)  
[Pyttsx3](https://pypi.org/project/pyttsx3/)
