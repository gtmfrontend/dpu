from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
import calendar
import random
import holidays

def create_pdf(name, month, year):
    # Nome do arquivo
    filename = f"{name}_timesheet_{month}_{year}.pdf"

    # Cria o canvas
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Adiciona o título
    c.setFont("Helvetica", 16)
    c.drawString(100, height - 40, f"Timesheet - {name}")
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 60, f"Mês de referência: {month} de {year}")

    # Obtém o número de dias no mês
    _, num_days = calendar.monthrange(year, month)

    # Define a posição inicial para a tabela
    start_x = 50
    start_y = height - 100
    line_height = 20

    # Cabeçalhos da tabela
    headers = ["Data", "Entrada", "Almoço Início", "Almoço Fim", "Saída", "Total Horas"]

    # Desenha os cabeçalhos da tabela
    c.setFont("Helvetica-Bold", 10)
    for i, header in enumerate(headers):
        c.drawString(start_x + i * 90, start_y, header)
    start_y -= line_height

    # Feriados no Brasil
    br_holidays = holidays.Brazil(years=year)

    total_horas_trabalhadas = timedelta()

    # Preenche as linhas da tabela
    c.setFont("Helvetica", 10)
    for day in range(1, num_days + 1):
        current_date = datetime(year, month, day)
        date_str = current_date.strftime('%d/%m/%Y')

        if current_date.weekday() >= 5 or current_date in br_holidays:
            entrada = almoco_inicio = almoco_fim = saida = total_horas = "Feriado" if current_date in br_holidays else "-"
        else:
            entrada = (current_date.replace(hour=8) + timedelta(minutes=random.randint(0, 10))).strftime('%H:%M')
            almoco_inicio = (current_date.replace(hour=12) + timedelta(minutes=random.randint(-10, 10))).strftime('%H:%M')
            almoco_fim = (datetime.strptime(almoco_inicio, '%H:%M') + timedelta(hours=1)).strftime('%H:%M')
            saida = (datetime.strptime(entrada, '%H:%M') + timedelta(hours=9)).strftime('%H:%M')
            total_horas = "8:00"
            total_horas_trabalhadas += timedelta(hours=8)

        c.drawString(start_x, start_y, date_str)
        c.drawString(start_x + 90, start_y, entrada)
        c.drawString(start_x + 180, start_y, almoco_inicio)
        c.drawString(start_x + 270, start_y, almoco_fim)
        c.drawString(start_x + 360, start_y, saida)
        c.drawString(start_x + 450, start_y, total_horas)

        start_y -= line_height

    # Adiciona a linha de total
    c.setFont("Helvetica-Bold", 10)
    total_horas_str = str(total_horas_trabalhadas)[:-3]  # Remove os segundos do formato HH:MM:SS
    c.drawString(start_x + 300, start_y, "Total Horas Trabalhadas:")
    c.drawString(start_x + 450, start_y, total_horas_str)

    # Salva o PDF
    c.save()
    print(f"Arquivo PDF criado: {filename}")

# Exemplo de uso
name = "Guilherme Teles da Mota"
month = 5
year = 2024

create_pdf(name, month, year)
