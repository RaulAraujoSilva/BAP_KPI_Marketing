"""
Script para preparação e limpeza dos dados de Marketing
Arquivo: KPI - 2025 BAP.xlsx - Aba Marketing

Autor: Preparado para análises de tendências, campanhas e ROI
Data: 2025-11-12
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class MarketingDataProcessor:
    """Classe para processar e limpar dados de marketing do Excel"""

    def __init__(self, file_path):
        self.file_path = file_path
        self.df_raw = None
        self.tables = {}
        self.meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                      'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    def load_data(self):
        """Carrega a aba Marketing do arquivo Excel"""
        print(f"Carregando arquivo: {self.file_path}")
        self.df_raw = pd.read_excel(self.file_path, sheet_name='Marketing', header=None)
        print(f"[OK] Dados carregados: {self.df_raw.shape[0]} linhas x {self.df_raw.shape[1]} colunas")

    def extract_table(self, start_row, end_row, table_name, metric_col=0, data_start_col=1):
        """
        Extrai uma tabela específica da planilha

        Args:
            start_row: Linha inicial (0-indexed)
            end_row: Linha final (0-indexed, exclusive)
            table_name: Nome da tabela
            metric_col: Coluna com nomes das métricas
            data_start_col: Primeira coluna com dados
        """
        print(f"\nExtraindo: {table_name} (linhas {start_row+1}-{end_row})")

        # Extrair dados
        table_data = self.df_raw.iloc[start_row:end_row, :].copy()

        # Primeira linha como header se for cabeçalho
        if pd.notna(table_data.iloc[0, 1]) and isinstance(table_data.iloc[0, 1], str):
            # Verificar se primeira linha é header (contém nomes de meses)
            if any(mes in str(table_data.iloc[0, 1]) for mes in ['Janeiro', 'Jan']):
                header_row = table_data.iloc[0, data_start_col:data_start_col+12].values
                metrics = table_data.iloc[1:, metric_col].values
                data = table_data.iloc[1:, data_start_col:data_start_col+12].values
            else:
                header_row = self.meses
                metrics = table_data.iloc[0:, metric_col].values
                data = table_data.iloc[0:, data_start_col:data_start_col+12].values
        else:
            header_row = self.meses
            metrics = table_data.iloc[0:, metric_col].values
            data = table_data.iloc[0:, data_start_col:data_start_col+12].values

        # Criar DataFrame
        df = pd.DataFrame(data, columns=header_row)
        df.insert(0, 'Métrica', metrics)

        # Limpar dados
        df = self._clean_dataframe(df, table_name)

        print(f"  [OK] {len(df)} metricas extraidas")
        print(f"  [OK] Colunas: {list(df.columns)}")

        self.tables[table_name] = df
        return df

    def _clean_dataframe(self, df, table_name):
        """Limpa e formata o DataFrame"""
        # Remover linhas completamente vazias
        df = df.dropna(how='all', subset=df.columns[1:])

        # Limpar nomes de métricas
        df['Métrica'] = df['Métrica'].astype(str).str.strip()
        df = df[df['Métrica'] != 'nan']
        df = df[df['Métrica'] != '']

        # Converter valores numéricos e tratar erros #DIV/0!
        for col in df.columns[1:]:  # Pular coluna de Métrica
            df[col] = df[col].apply(self._convert_value)

        # Adicionar coluna de identificação
        df.insert(0, 'Tabela', table_name)

        # Reset index
        df = df.reset_index(drop=True)

        return df

    def _convert_value(self, val):
        """Converte valor para numérico, tratando erros #DIV/0!"""
        if pd.isna(val):
            return np.nan

        # Verificar se é erro do Excel
        if isinstance(val, str):
            val_clean = val.strip().upper()
            if '#DIV/0!' in val_clean or '#VALOR!' in val_clean or '#REF!' in val_clean:
                return np.nan

            # Tentar converter string para número
            try:
                # Remover símbolos de moeda e espaços
                val_clean = val_clean.replace('R$', '').replace('%', '').replace(',', '').strip()
                return pd.to_numeric(val_clean)
            except:
                return np.nan

        # Tentar converter diretamente
        try:
            return pd.to_numeric(val)
        except:
            return np.nan

    def extract_all_tables(self):
        """Extrai todas as 6 tabelas identificadas"""
        print("\n" + "="*70)
        print("EXTRAINDO TODAS AS TABELAS")
        print("="*70)

        # Tabela 1: Marketing Geral (linhas 4-10, 0-indexed: 3-10)
        self.extract_table(3, 10, 'Marketing_Geral')

        # Tabela 2: Leads Condominios (linhas 12-30, 0-indexed: 11-30)
        self.extract_table(11, 30, 'Leads_Condominios')

        # Tabela 3: Índices Condominios (linhas 33-40, 0-indexed: 32-40)
        self.extract_table(32, 40, 'Indices_Condominios')

        # Tabela 4: Campanha Imóveis (linhas 43-52, 0-indexed: 42-52)
        self.extract_table(42, 52, 'Campanha_Imoveis')

        # Tabela 5: Campanha Boleto Digital (linhas 54-59, 0-indexed: 53-59)
        self.extract_table(53, 59, 'Campanha_Boleto_Digital')

        # Tabela 6: Campanha Multiseguros (linhas 61-70, 0-indexed: 60-70)
        self.extract_table(60, 70, 'Campanha_Multiseguros')

        print("\n" + "="*70)
        print(f"[OK] TOTAL: {len(self.tables)} tabelas extraidas com sucesso!")
        print("="*70)

    def create_long_format(self, table_name):
        """Converte uma tabela para formato long (tidy data)"""
        if table_name not in self.tables:
            print(f"Erro: Tabela '{table_name}' não encontrada")
            return None

        df = self.tables[table_name].copy()

        # Colunas de identificação
        id_cols = ['Tabela', 'Métrica']

        # Melt para formato long
        df_long = df.melt(
            id_vars=id_cols,
            var_name='Mês',
            value_name='Valor'
        )

        # Adicionar número do mês
        mes_to_num = {mes: i+1 for i, mes in enumerate(self.meses)}
        # Também mapear versões com caracteres especiais (encoding do Windows)
        mes_to_num_lower = {mes.lower(): i+1 for i, mes in enumerate(self.meses)}

        def get_month_number(month_name):
            if pd.isna(month_name):
                return np.nan
            month_str = str(month_name).strip()
            # Tentar busca direta
            if month_str in mes_to_num:
                return mes_to_num[month_str]
            # Tentar case-insensitive
            month_lower = month_str.lower()
            if month_lower in mes_to_num_lower:
                return mes_to_num_lower[month_lower]
            # Mapear manualmente se necessário
            month_map = {
                'janeiro': 1, 'fevereiro': 2, 'março': 3, 'marco': 3, 'mar�o': 3,
                'abril': 4, 'maio': 5, 'junho': 6,
                'julho': 7, 'agosto': 8, 'setembro': 9,
                'outubro': 10, 'novembro': 11, 'dezembro': 12
            }
            return month_map.get(month_lower, np.nan)

        df_long['Mês_Num'] = df_long['Mês'].apply(get_month_number)

        # Remover linhas onde não conseguimos determinar o mês
        df_long = df_long.dropna(subset=['Mês_Num'])

        # Adicionar ano (assumindo 2025)
        df_long['Ano'] = 2025

        # Criar coluna de data
        df_long['Data'] = pd.to_datetime(
            df_long['Ano'].astype(int).astype(str) + '-' +
            df_long['Mês_Num'].astype(int).astype(str) + '-01'
        )

        # Reordenar colunas
        df_long = df_long[['Tabela', 'Métrica', 'Ano', 'Mês', 'Mês_Num', 'Data', 'Valor']]

        # Remover valores nulos
        df_long = df_long.dropna(subset=['Valor'])

        return df_long

    def generate_summary_statistics(self):
        """Gera estatísticas resumidas de todas as tabelas"""
        print("\n" + "="*70)
        print("GERANDO ESTATÍSTICAS RESUMIDAS")
        print("="*70)

        summary_data = []

        for table_name, df in self.tables.items():
            # Estatísticas básicas
            num_metrics = len(df)
            num_months = len([col for col in df.columns if col not in ['Tabela', 'Métrica']])

            # Contar valores
            data_cols = [col for col in df.columns if col not in ['Tabela', 'Métrica']]
            total_cells = num_metrics * num_months
            non_null_cells = df[data_cols].notna().sum().sum()
            null_cells = total_cells - non_null_cells
            pct_preenchimento = (non_null_cells / total_cells * 100) if total_cells > 0 else 0

            summary_data.append({
                'Tabela': table_name,
                'Num_Métricas': num_metrics,
                'Num_Meses': num_months,
                'Total_Células': total_cells,
                'Células_Preenchidas': non_null_cells,
                'Células_Vazias': null_cells,
                'Pct_Preenchimento': round(pct_preenchimento, 1)
            })

            print(f"\n{table_name}:")
            print(f"  - {num_metrics} metricas")
            print(f"  - {pct_preenchimento:.1f}% de preenchimento")

        df_summary = pd.DataFrame(summary_data)

        print("\n" + "="*70)
        print("[OK] Estatisticas geradas com sucesso!")
        print("="*70)

        return df_summary

    def save_to_excel(self, output_path):
        """Salva todos os dados em um arquivo Excel limpo"""
        print("\n" + "="*70)
        print("SALVANDO DADOS EM EXCEL")
        print("="*70)
        print(f"Arquivo de saída: {output_path}")

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Salvar cada tabela em uma aba
            for i, (table_name, df) in enumerate(self.tables.items(), 1):
                # Remover coluna 'Tabela' antes de salvar (redundante no contexto da aba)
                df_to_save = df.drop(columns=['Tabela'])
                df_to_save.to_excel(writer, sheet_name=table_name, index=False)
                print(f"  [OK] Aba {i}: {table_name} ({len(df_to_save)} metricas)")

            # Gerar e salvar estatísticas
            df_stats = self.generate_summary_statistics()
            df_stats.to_excel(writer, sheet_name='Resumo_Analitico', index=False)
            print(f"  [OK] Aba 7: Resumo_Analitico")

            # Criar aba com dados consolidados em formato long
            print("\n  Gerando formato long para analises...")
            all_long_data = []
            for table_name in self.tables.keys():
                df_long = self.create_long_format(table_name)
                if df_long is not None:
                    all_long_data.append(df_long)

            if all_long_data:
                df_consolidated = pd.concat(all_long_data, ignore_index=True)
                df_consolidated.to_excel(writer, sheet_name='Dados_Consolidados_Long', index=False)
                print(f"  [OK] Aba 8: Dados_Consolidados_Long ({len(df_consolidated)} registros)")

        print("\n" + "="*70)
        print(f"[OK] ARQUIVO SALVO COM SUCESSO!")
        print(f"  Local: {output_path}")
        print("="*70)

    def get_table(self, table_name):
        """Retorna uma tabela específica"""
        return self.tables.get(table_name)

    def list_tables(self):
        """Lista todas as tabelas disponíveis"""
        return list(self.tables.keys())


def main():
    """Função principal para execução do script"""
    # Definir caminhos
    input_file = Path("KPI - 2025 BAP.xlsx")
    output_file = Path("KPI_Marketing_Preparado.xlsx")

    # Verificar se arquivo existe
    if not input_file.exists():
        print(f"ERRO: Arquivo não encontrado: {input_file}")
        return

    # Processar dados
    processor = MarketingDataProcessor(input_file)

    # 1. Carregar dados
    processor.load_data()

    # 2. Extrair todas as tabelas
    processor.extract_all_tables()

    # 3. Salvar em Excel limpo
    processor.save_to_excel(output_file)

    # 4. Exibir preview de cada tabela
    print("\n" + "="*70)
    print("PREVIEW DAS TABELAS EXTRAÍDAS")
    print("="*70)

    for table_name in processor.list_tables():
        df = processor.get_table(table_name)
        print(f"\n### {table_name} ###")
        print(df.head(3).to_string())

    print("\n" + "="*70)
    print("PROCESSAMENTO CONCLUIDO!")
    print("="*70)
    print(f"\n[ARQUIVO] {output_file}")
    print(f"[TABELAS] {len(processor.list_tables())}")
    print("\nProximos passos:")
    print("  1. Abrir o arquivo Excel gerado para verificar os dados")
    print("  2. Usar o notebook 'analise_marketing.ipynb' para analises")
    print("  3. Criar dashboards com os dados consolidados")


if __name__ == "__main__":
    main()
