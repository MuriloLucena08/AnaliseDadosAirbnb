# 🏠 Previsão de Valor de Imóveis no Airbnb · Streamlit App

[![Made with Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-green?logo=streamlit)](https://deploy-projetoairbnb.streamlit.app/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?logo=scikit-learn)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/deploy-success-brightgreen)](https://deploy-projetoairbnb.streamlit.app/)

Aplicativo interativo para previsão de valores de imóveis anunciados no Airbnb nos anos 2018, 2019 e 2020, utilizando Machine Learning com `ExtraTreesRegressor` e interface em Streamlit.

👉 **Acesse agora:**
🔗 [https://deploy-projetoairbnb.streamlit.app/](https://deploy-projetoairbnb.streamlit.app/)

---

## 📋 Sobre o Projeto

Este projeto foi desenvolvido como parte dos estudos em **Ciência de Dados e Machine Learning** com **Python** e **Streamlit**, dentro do curso da **Hashtag Treinamentos**.

O objetivo é criar uma ferramenta simples e intuitiva que permita prever o preço de imóveis com base em suas características, como localização, tipo, número de quartos, banheiros, entre outros.

---

## 🧪 Tecnologias utilizadas

* Python 3.10+
* Streamlit
* scikit-learn
* pandas
* numpy
* joblib
* requests

---

## 🏗️ Como funciona

1. O usuário preenche os campos com os dados do imóvel
2. O app monta um `DataFrame` com os dados de entrada
3. O modelo de Machine Learning é carregado do disco
4. A previsão é exibida em tempo real

---

## 🧪 Modelo de Machine Learning

* Algoritmo: `ExtraTreesRegressor`
* Modelo treinado localmente com os dados do Airbnb
* Exportado com `joblib.dump(..., compress=9)` para otimizar o tamanho
* Versão reduzida (menos estimadores) foi usada para possibilitar o deploy

---

## 📁 Estrutura do projeto

```
📁 AnaliseDadosAirbnb/
├──Solução Airbnb Rio.ipynb       # Arquivo que roda a análise dos dados com o dataset, faz o machine learning e gera os arquivos dados.csv e modelo.joblib
├── DeployProjetoAirbnb.py        # Código principal do app Streamlit
├── dados.csv                     # Base de apoio para entrada dos dados
├── modelo.joblib                 # Modelo de ML treinado e comprimido
├── requirements.txt              # Dependências
└── README.md                     # Este arquivo
```

---

## 🪠 Como executar localmente

```bash
# Clone o repositório
git clone https://github.com/MuriloLucena08/AnaliseDadosAirbnb.git
cd AnaliseDadosAirbnb

# Instale as dependências
pip install -r requirements.txt

# Execute o app
streamlit run DeployProjetoAirbnb.py
```

---

## 📝 Observações

> Este projeto utiliza uma **versão simplificada do modelo** para garantir compatibilidade com os limites de memória da nuvem. A versão original, com mais estimadores, é mais precisa, mas inviável para deploy gratuito.
> O dataset não está disponivel no repositório, pois é um arquivo muito grande. Caso queira rodar o código posso disponibilizar URL do meu S3 AWS com o arquivo para baixar [Link](https://meu-bucketdatasetcsv.s3.us-east-2.amazonaws.com/dataset+/dataset.zip)
> Fique a vontade de rodar e atualizar os dados do dataset para os dias atuais e usar outros algoritmos de inteligencia artificial

---

## ✍️ Autor

Desenvolvido por **Murilo Lucena**
📘 [LinkedIn](https://www.linkedin.com/in/seu-perfil)
💻 [GitHub](https://github.com/MuriloLucena08)

---

## 📣 Agradecimentos

Este projeto foi desenvolvido como parte dos estudos com a [Hashtag Treinamentos](https://www.hashtagtreinamentos.com/), referência em formação prática em Python e Dados.

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar, estudar e modificar.
