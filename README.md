# Projeto de Campo.

## Objetivos

Melhorar as estatísticas de atendimento de um hospital através de **Healthy Analytics**.

---

## Progresso

Esta seção abordará os progressos feitos pela equipe ao longo do projeto.

### Entendimento do universo de Healthy Analytics.

Artigos e explicação sobre eles:

- Artigo 1:
- Artigo 2:
- Artigo 3:
- Artigo 4:

...

### Cálculo das probabilidades das quantidades de pessoas acamadas.

Em primeiro momento, é nos dado este pequeno problema: 
* Dado um conjunto de **$n$** pacientes com probabilidades **$a_i$** de precisarem de uma cama de leito, como computar de forma eficiente as probabilidades **$\set{P(X = j)}_{j=1}^n$**, onde **$X$** representa a quantidade de pacientes acamados?

#### Solução

Primeiramente, consideramos um algoritmo com complexidade **$O(n!)$**, que realizava todas as permutações possiveis para cada valor de **$j$**.

Após esta tentativa, percebemos que o cálculo demoraria muito para uma aplicabilidade real, então partimos para outra alternativa, uma convolução, reduzindo para uma complexidade de **$O(n^2)$**.

Ao final, uma solução com aproximação Normal foi também considerada, reduzindo ainda mais a complexidade. Agora ela está em **$O(n)$**.

#### Código

O código se encontra nos arquivo *****nome_dos_arquivos*.****


---

## Equipe

- Adriel
- Alex
- Matheus