import csv
from graficos import XBarChart, RChart
import config

def load_data_from_csv(file_path):
    """Carrega os dados do CSV para amostras e amplitudes."""
    samples = []
    ranges = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            samples.append(float(row[0]))
            ranges.append(float(row[1]))
    return samples, ranges

def display_menu():
    """Exibe o menu de opções no terminal."""
    print("================================================================")
    print("Menu de monitoramento - Gráficos")
    print("1. Visualizar dados")
    print("2. Calcular limites de controle")
    print("3. Gerar gráfico X-barra e identificar os outliers")
    print("4. Gerar gráfico R e identificar os outliers")
    print("5. Calcular Cp e Cpk")
    print("6. Sair")


def main():
    """Função principal que controla o fluxo do programa."""
    file_path = f'data/data_lista.csv'
    samples, ranges = load_data_from_csv(file_path)

    """Cria o gráfico X-barra"""
    x_bar_chart = XBarChart(samples, ranges, config.A2)

    """Cria o gráfico R"""
    r_chart = RChart(ranges, config.D3, config.D4)

    while True:
        display_menu()
        choice = input("Escolha uma opção: ")

        if choice == '1':
            print("********************************")
            print(f'QUANTIDADE DE AMOSTRAS: {len(samples)}')
            print("--------------------------------")
            print('Amostras:')
            print(samples)
            print("--------------------------------")
            print('Amplitudes:')
            print(ranges)

        elif choice == '2':
            print("********************************")
            print(f'LIMITES DE CONTROLE')
            print("--------------------------------")
            print(f'Gráfico X-barra')
            print(f'- Limite Superior: {x_bar_chart.lsc}')
            print(f'- Limite Inferior: {x_bar_chart.lic}')
            print("--------------------------------")
            print(f'Gráfico R')
            print(f'- Limite Superior: {r_chart.lsc}')
            print(f'- Limite Inferior: {r_chart.lic}')
            
        elif choice == '3':
            x_bar_chart.plot_and_alert()


        elif choice == '4':
            r_chart.plot_and_alert()

        elif choice == '5':
            print("********************************")
            print(f'ANÁLISE DE CAPACIDADE')
            print("--------------------------------")
            print(f'Gráfico X-barra')
            print(f'- Cp: {x_bar_chart.cp}')
            print(f'- Cpk: {x_bar_chart.cpk}')
            print("--------------------------------")
            print(f'Gráfico R')
            print(f'- Cp: {r_chart.cp}')
            print(f'- Cpk: {r_chart.cpk}')

        elif choice == '6':
            print("Saindo...")
            break

        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
