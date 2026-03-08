import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_pdf_label(
    filename="label_output.pdf", 
    logo_path="logo.png", 
    operator_name="@vital...", 
    phone="8 (978) 895-47-13", 
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
        c.drawImage(logo_path, 2*mm, 31*mm, width=8*mm, height=8*mm, mask='auto')

    c.setFont(font_name, 9)
    c.drawString(12*mm, 35.5*mm, "ООО «ВТИ»")
    
    c.setFont(font_name, 4)
    c.drawString(12*mm, 33.5*mm, "ул Советская 26, г. Керчь")
    
    c.setFont(font_name, 4)
    c.drawString(12*mm, 31.5*mm, "8 (978) 762-89-67  8 (978) 010-49-49")

    # Разделительная линия
    c.setLineWidth(0.5)
    c.line(0*mm, 29*mm, width, 29*mm)

    # --- ДАННЫЕ КЛИЕНТА ---

    # 1. Телефон клиента (Самый первый, по центру, крупный)
    c.setFont(font_name, 18) # Я сделал размер 12, чтобы он бросался в глаза
    # Центр этикетки по X = 28.5 мм
    c.drawCentredString(28.5*mm, 21.5*mm, f"{phone}")
    
    # --- НАСТРОЙКА ИНТЕРВАЛОВ ---
    start_y = 17 * mm        # Высота, с которой начинаем писать данные оператора
    line_spacing = 3 * mm  # Межстрочный интервал (уменьши это число, чтобы сжать строки)
    
    # Возвращаем мелкий шрифт для остального текста
    c.setFont(font_name, 6) 
    
    # 2. Имя оператора (с левого края)
    c.drawString(2*mm, start_y, f"Принял(а): {operator_name}")
    
    # 3. Время
    c.drawString(2*mm, start_y - line_spacing, f"Время: {time_str}")

    # 4. Описание
    c.drawString(2*mm, start_y - 2 * line_spacing, f"Описание: {description}")

    # Сохраняем готовый PDF
    c.save()
    print(f"Готово! Этикетка сохранена как {filename}")

if __name__ == "__main__":
    create_pdf_label()