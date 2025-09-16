# 🔄 Streaming com Apache Beam + Google Dataflow + Pub/Sub

Este repositório contém scripts para processamento de dados em **streaming** usando [Apache Beam](https://beam.apache.org/) com o runner **Google Cloud Dataflow**, recebendo dados em tempo real via **Cloud Pub/Sub**.

## 📦 Componentes

- **Produtor**: Envia dados para um tópico do Pub/Sub.
- **Consumidor**: Pipeline Apache Beam que lê do Pub/Sub e processa os dados.
- **Destino**: Pode ser outro tópico, BigQuery ou armazenamento no GCS.

## 📂 Scripts

| Arquivo                                      | Função                      |
|----------------------------------------------|-----------------------------|
| `gerador_de_dados.py`                        | Simula envio de dados ao Pub/Sub |
| `consumidor_de_dados.py`                     | Lê dados do Pub/Sub e processa via Beam |
| `streaming_ps_of_ps_tumbling_fixed_window.py`| Pipeline com janelas fixas |
| `streaming_ps_of_ps_sliding_window.py`       | Pipeline com janelas deslizantes |
