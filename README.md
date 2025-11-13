# BAP Marketing Analytics Dashboard

Dashboard corporativo de Business Intelligence para análise de KPIs e performance de marketing.

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.41.1-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📊 Sobre o Projeto

Sistema de análise de indicadores de marketing desenvolvido para BAP, oferecendo visualizações interativas e insights estratégicos sobre:

- Performance de Marketing Digital (Instagram, Ads, Alcance)
- Análise de Leads e Conversão por Canal
- KPIs Financeiros (CAC, MRR, ROI)
- Gestão de Campanhas (Imóveis, Boleto Digital, Seguros)
- Análises Comparativas entre Campanhas

## 🚀 Demo Online

Acesse o dashboard: [BAP Marketing Analytics](https://seu-app.streamlit.app)

## 🎯 Funcionalidades

### Executive Summary
- Visão consolidada dos principais KPIs
- Métricas de completude de dados
- Resumo executivo de performance

### Marketing Performance
- Análise de crescimento Instagram
- Investimento em publicidade
- Visualizações de conteúdo
- Alcance orgânico vs pago

### Lead Analytics
- Distribuição de leads por origem
- Taxa de conversão por canal
- Funil de vendas
- Análise de propostas enviadas

### Financial KPIs
- Customer Acquisition Cost (CAC)
- Monthly Recurring Revenue (MRR)
- Return on Investment (ROI)
- Análise de rentabilidade

### Campaign Management
- Campanha Imóveis (investimento, leads, ROI)
- Campanha Boleto Digital (adoção, economia)
- Campanha Multiseguros (conversões, performance)

### Comparative Analysis
- Comparação de investimentos
- Comparação de ROI
- Análise de custo por lead
- Performance summary

## 🛠️ Tecnologias

- **Python 3.12**
- **Streamlit** - Framework para dashboards interativos
- **Pandas** - Manipulação e análise de dados
- **Plotly** - Visualizações interativas
- **OpenPyXL** - Leitura de arquivos Excel

## 📦 Instalação Local

### Pré-requisitos

- Python 3.12 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/RaulAraujoSilva/BAP_KPI_Marketing.git
cd BAP_KPI_Marketing
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o dashboard:
```bash
streamlit run dashboard_marketing.py
```

4. Acesse no navegador: `http://localhost:8501`

## 📁 Estrutura do Projeto

```
BAP_KPI_Marketing/
├── dashboard_marketing.py          # Dashboard principal
├── preparar_dados_marketing.py     # Script de ETL
├── analise_marketing.ipynb         # Notebook Jupyter com análises
├── KPI - 2025 BAP.xlsx            # Dados fonte (Excel)
├── KPI_Marketing_Preparado.xlsx   # Dados processados
├── requirements.txt                # Dependências Python
├── .gitignore                      # Arquivos ignorados pelo Git
└── README.md                       # Este arquivo
```

## 🔄 Processamento de Dados

### Script de Preparação

Execute o script de ETL para processar os dados brutos:

```bash
python preparar_dados_marketing.py
```

O script realiza:
- Extração de 6 tabelas da aba "Marketing"
- Limpeza e tratamento de erros (#DIV/0!)
- Conversão para formato long/tidy
- Geração de estatísticas descritivas
- Exportação para Excel estruturado

### Estrutura dos Dados

**Tabelas extraídas:**
1. Marketing_Geral (6 métricas)
2. Leads_Condominios (17 métricas)
3. Indices_Condominios (7 KPIs)
4. Campanha_Imoveis (9 métricas)
5. Campanha_Boleto_Digital (5 métricas)
6. Campanha_Multiseguros (9 métricas)

## 📈 Análises Jupyter

O notebook `analise_marketing.ipynb` contém:
- Análises exploratórias detalhadas
- Visualizações estáticas com Matplotlib/Seaborn
- Estatísticas descritivas
- Exportação de dados para CSV

## 🎨 Design Corporativo

O dashboard segue princípios de design corporativo:
- Paleta de cores profissional
- Tipografia Inter (Google Fonts)
- Layout clean e minimalista
- Gráficos interativos com Plotly
- Responsivo para diferentes dispositivos

## 📊 Dados de Exemplo

Os dados cobrem o período de **Janeiro a Outubro de 2025**, incluindo:
- ~53 métricas totais
- 83% de completude média
- 527 registros em formato consolidado

## 🚀 Deploy no Streamlit Cloud

### Passos para Deploy

1. Faça push do código para o GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte sua conta GitHub
4. Selecione o repositório `BAP_KPI_Marketing`
5. Defina o arquivo principal: `dashboard_marketing.py`
6. Clique em "Deploy"

**Importante:** Certifique-se de que o arquivo `KPI_Marketing_Preparado.xlsx` está no repositório.

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autor

**Raul Araujo Silva**
- GitHub: [@RaulAraujoSilva](https://github.com/RaulAraujoSilva)

## 📞 Contato

Para dúvidas ou sugestões sobre o projeto, abra uma issue no GitHub.

---

**BAP Marketing Analytics Platform** | Business Intelligence Dashboard | 2025
