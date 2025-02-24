import time
import numpy as np
import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

"""Verificação de Regras Western Eletric"""
def firstRule(values, lsc, lic):
    i = 0
    for value in values:
        if value > lsc or value < lic:
            return False
    return True

def secondRule(values, cl, sigma):
    for i in range(len(values)-2):
        if values[i] > (cl + 2*sigma) and (values[i+1] > (cl + 2*sigma) or values[i+2] > (cl + 2*sigma)):
            return False
        elif values[i] < (cl - 2*sigma) and (values[i+1] < (cl - 2*sigma) or values[i+2] < (cl - 2*sigma)):
            return False
    return True

def thirdRule(values, cl, sigma):
    for i in range(len(values)-4):
        auxSup = 0
        auxInf = 0
        for n in range(5):
            if values[i+n] > (cl + sigma):
                auxSup += 1
            elif values[i+n] < (cl - sigma):
                auxInf += 1
        if auxSup >= 4 or auxInf >= 4:
            return False
    return True


def fourthRule(values, cl):
    auxSup = 0
    auxInf = 0
    for value in values:
        if value > cl:
            auxInf = 0
            auxSup += 1
            if auxSup >= 9:
                return False
        else:
            auxSup = 0
            if value < cl:
                auxInf += 1
                if auxInf >= 9:
                    return False
    return True

"""Calcular Cp e Cpk"""
def calc_cp(lsc, lic, sigma):
    return (lsc - lic) / (6 * sigma)

def calc_cpk(lsc, lic, avrg, sigma):
    aux1 = (lsc - avrg) / (3 * sigma)
    aux2 = (avrg - lic) / (3 * sigma)
    return min(aux1, aux2)

def calc_sigma(avrg, values):
    sigma = 0
    for value in values:
        sigma += (avrg - value)**2
    return np.sqrt(sigma/(len(values)-1))
    
"""Função para enviar mensagens pelo telegram"""
def send_telegram_alert(message):
    """Envia uma mensagem de alerta via Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    if message:
        try:
            response = requests.get(url, params=payload, timeout=30)
            if response.status_code == 200:
                print("Mensagem enviada com sucesso.")
                print(f"{message}")
            else:
                print(f"Erro ao enviar mensagem: {response.status_code}")
                print(response.json())
            
            time.sleep(1)
        except requests.RequestException as e:
            print(f"Erro na requisição: {e}")

"""Modelos dos gráficos"""
class XBarChart:
    def __init__(self, samples, ranges, A2):
        self.samples = np.array(samples)
        self.ranges = np.array(ranges)
        self.A2 = A2
        self.center_line = np.mean(self.samples)
        self.amplitude_amplitudes = np.mean(self.ranges)
        self.lsc = round((self.center_line + self.A2 * self.amplitude_amplitudes), 3)
        self.lic = round((self.center_line - self.A2 * self.amplitude_amplitudes), 3)
        self.sigma = round(calc_sigma(self.center_line, self.samples), 3)
        self.cp = round(calc_cp(self.lsc, self.lic, self.sigma), 3)
        self.cpk = round(calc_cpk(self.lsc, self.lic, self.center_line, self.sigma), 3)

    def check_rules(self):
        self.ruleOne = firstRule(self.samples, self.lsc, self.lic)
        self.ruleTwo = secondRule(self.samples, self.center_line, self.sigma)
        self.ruleThree = thirdRule(self.samples, self.center_line, self.sigma)
        self.ruleFour = fourthRule(self.samples, self.center_line)

        messages = []

        if not self.ruleOne:
            messages.append("🟡 ALERTA AMARELO - Gráfico X-barra! Regra 1 não satisfeita")
        if not self.ruleTwo:
            messages.append("🟡 ALERTA AMARELO - Gráfico X-barra! Regra 2 não satisfeita")
        if not self.ruleThree:
            messages.append("🟡 ALERTA AMARELO - Gráfico X-barra! Regra 3 não satisfeita")
        if not self.ruleFour:
            messages.append("🟡 ALERTA AMARELO - Gráfico X-barra! Regra 4 não satisfeita")

        if self.ruleOne and self.ruleTwo and self.ruleThree and self.ruleFour:
            messages.append("🟢 Todas as regras atendidas")

        message = "\n".join(messages)
        if messages:
            send_telegram_alert(message)
        return
    
    def plot_and_alert(self):
        """Plota o gráfico X-barra com pontos fora do limite destacados e envia alertas se necessário."""
        if self.center_line == 0 or self.lsc == 0 or self.lic == 0:
            raise ValueError("É necessário calcular os limites antes de plotar.")
        
        plt.figure(figsize=(10, 6))
        
        x = np.arange(1, len(self.samples) + 1)

        out_of_control = (self.samples > self.lsc) | (self.samples < self.lic)
        in_control = ~out_of_control

        plt.scatter(x[in_control], self.samples[in_control], color='blue', label='Médias das Amostras', marker='o')

        plt.scatter(x[out_of_control], self.samples[out_of_control], color='red', label='Fora dos Limites', marker='o')

        plt.axhline(self.center_line + self.sigma, color='gray', linestyle='--')
        plt.axhline(self.center_line + 2*self.sigma, color='gray', linestyle='--')
        plt.axhline(self.center_line - self.sigma, color='gray', linestyle='--')
        plt.axhline(self.center_line - 2*self.sigma, color='gray', linestyle='--')
        plt.axhline(self.center_line, color='green', linestyle='--', label='Linha Central (CL)')
        plt.axhline(self.lsc, color='red', linestyle='--', label='Limite Superior de Controle (LSC)')
        plt.axhline(self.lic, color='red', linestyle='--', label='Limite Inferior de Controle (LIC)')

        plt.xticks(x)
        plt.xlabel("Amostra")
        plt.ylabel("Média")
        plt.title("Gráfico X-barra")
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)

        plt.grid(True, linestyle="--", linewidth=0.5)

        if np.any(out_of_control):
            out_samples = x[out_of_control]
            # text_info = f"Pontos fora dos limites: {', '.join(map(str, out_samples))}"
            # plt.figtext(0.1, 0.02, wrap=True, horizontalalignment='left', fontsize=10, color="black")

            message = f"🔴 ALERTA VERMELHO - Gráfico X-barra! Pontos fora dos limites: {', '.join(map(str, out_samples))}"
            send_telegram_alert(message)

        self.check_rules()

        plt.tight_layout()

        plt.show()
        return

class RChart:
    def __init__(self, ranges, D3, D4):
        self.ranges = np.array(ranges)
        self.D3 = D3
        self.D4 = D4
        self.amplitude_amplitudes = np.mean(self.ranges)
        self.lsc = round(self.D4 * self.amplitude_amplitudes, 3)
        self.lic = round(self.D3 * self.amplitude_amplitudes, 3)
        self.messages = []
        self.sigma = round(calc_sigma(self.amplitude_amplitudes, self.ranges), 3)
        self.cp = round(calc_cp(self.lsc, self.lic, self.sigma), 3)
        self.cpk = round(calc_cpk(self.lsc, self.lic, self.amplitude_amplitudes, self.sigma), 3)

    def check_rules(self):
        self.ruleOne = firstRule(self.ranges, self.lsc, self.lic)
        self.ruleTwo = secondRule(self.ranges, self.amplitude_amplitudes, self.sigma)
        self.ruleThree = thirdRule(self.ranges, self.amplitude_amplitudes, self.sigma)
        self.ruleFour = fourthRule(self.ranges, self.amplitude_amplitudes)

        messages = []

        if not self.ruleOne:
            messages.append("🟡 ALERTA AMARELO - Gráfico R! Regra 1 não satisfeita")
        if not self.ruleTwo:
            messages.append("🟡 ALERTA AMARELO - Gráfico R! Regra 2 não satisfeita")
        if not self.ruleThree:
            messages.append("🟡 ALERTA AMARELO - Gráfico R! Regra 3 não satisfeita")
        if not self.ruleFour:
            messages.append("🟡 ALERTA AMARELO - Gráfico R! Regra 4 não satisfeita")

        if self.ruleOne and self.ruleTwo and self.ruleThree and self.ruleFour:
            messages.append("🟢 Todas as regras atendidas")

        message = "\n".join(messages)
        if messages:
            send_telegram_alert(message)
        return
    
    def plot_and_alert(self):
        """Plota o gráfico R com pontos fora do controle destacados e envia alertas se necessário."""
        if self.amplitude_amplitudes is None or self.lsc is None or self.lic is None:
            raise ValueError("É necessário calcular os limites antes de plotar.")

        plt.figure(figsize=(12, 6))
        
        x = np.arange(1, len(self.ranges) + 1)

        out_of_control = (self.ranges > self.lsc) | (self.ranges < self.lic)
        in_control = ~out_of_control 

        plt.scatter(x[in_control], self.ranges[in_control], color='blue', label='Médias das Amplitudes', marker='o')

        plt.scatter(x[out_of_control], self.ranges[out_of_control], color='red', label='Fora dos Limites', marker='o')

        plt.axhline(self.amplitude_amplitudes + self.sigma, color='gray', linestyle='--')
        plt.axhline(self.amplitude_amplitudes + 2*self.sigma, color='gray', linestyle='--')
        plt.axhline(self.amplitude_amplitudes - self.sigma, color='gray', linestyle='--')
        plt.axhline(self.amplitude_amplitudes - 2*self.sigma, color='gray', linestyle='--')
        plt.axhline(self.amplitude_amplitudes, color='green', linestyle='--', label='Linha Central (CL)')
        plt.axhline(self.lsc, color='red', linestyle='--', label='Limite Superior de Controle (LSC)')
        plt.axhline(self.lic, color='red', linestyle='--', label='Limite Inferior de Controle (LIC)')

        plt.xticks(x)
        plt.xlabel("Amostra")
        plt.ylabel("Amplitude")
        plt.title("Gráfico R")
        plt.grid(True, linestyle="--", linewidth=0.5)

        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)

        if np.any(out_of_control):
            out_samples = x[out_of_control]
            # text_info = f"Pontos fora dos limites: {', '.join(map(str, out_samples))}"
            # plt.figtext(0.1, -0.1, wrap=True, horizontalalignment='left', fontsize=10, color="black")

            message = f"🔴 ALERTA VERMELHO - Gráfico R! Pontos fora dos limites: {', '.join(map(str, out_samples))}"
            send_telegram_alert(message)

        self.check_rules()

        plt.tight_layout()

        plt.show()
        return