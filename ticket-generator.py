import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_pdf_label(
    filename="label_output.pdf", 
    logo_path="logo.png", 
    operator_name="@vital...", 
    phone="89787770769", 
    time_str="2025-05-16 10:47", 
    description="Пу. Выключается. Михеева приняла"
):
    
    width = 57 * mm
    height = 40 * mm
    c = canvas.Canvas(filename, pagesize=(width, height))
    
    font_name = 'Arial'
    try:
        pdfmetrics.registerFont(TTFont(font_name, 'arial.ttf'))
    except Exception as e:
        print("ОШИБКА: Не найден файл шрифта 'arial.ttf'!")
        return

    # --- КОМПАКТНАЯ ШАПКА ---
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 2*mm, 30*mm, width=8*mm, height=8*mm, mask='auto')

    c.setFont(font_name, 9)
    c.drawString(12*mm, 35.5*mm, "ООО «ВТИ»")
    
    c.setFont(font_name, 6)
    c.drawString(12*mm, 32.5*mm, "ул Советская 26, г. Керчь")
    
    c.setFont(font_name, 5.5)
    c.drawString(12*mm, 29.5*mm, "+7 (978) 762-8967,  +7 (978) 010-4949")

    # Разделительная линия
    c.setLineWidth(0.5)
    c.line(0*mm, 27*mm, width, 27*mm)

    # --- ДАННЫЕ КЛИЕНТА (с уменьшенным межстрочным интервалом) ---

    # Имя оператора (подняли до 24 мм)
    c.setFont(font_name, 6)
    c.drawString(2*mm, 24*mm, f"Принял(а): {operator_name}")
    
    # Телефон клиента (подняли до 19 мм)
    # На твоем скриншоте телефон выглядит очень крупно! Если хочешь такой же огромный,
    # можешь поменять размер шрифта с 9 на 11 или 12 вот здесь:
    c.setFont(font_name, 11) 
    c.drawString(2*mm, 20*mm, f"Телефон: {phone}")
    
    # Время (подтянули до 14.5 мм)
    c.setFont(font_name, 6)
    c.drawString(2*mm, 14.5*mm, f"Время: {time_str}")

    # Описание (подтянули до 10.5 мм)
    c.setFont(font_name, 6)
    c.drawString(2*mm, 10.5*mm, f"Описание: {description}")

    # Сохраняем готовый PDF
    c.save()
    print(f"Готово! Этикетка сохранена как {filename}")

if __name__ == "__main__":
    create_pdf_label()