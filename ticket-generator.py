import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame, Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER # Импортируем выравнивание по центру

def create_pdf_label(
    filename="label_output.pdf", 
    logo_path="logo.png", 
    operator_name="@vital...", 
    phone="8 (978) 895-47-13", 
    time_str="2025-05-16 10:47", 
    description="Пу. Выключается. Михеева приняла, Пу. Выключается. Михеева приняла,"
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

    # --- ДАННЫЕ КЛИЕНТА (Всё в одном Frame) ---

    # 1. Настраиваем стили текста
    style_phone = ParagraphStyle(
        'PhoneStyle',
        fontName=font_name,
        fontSize=18,
        alignment=TA_CENTER, # Выравниваем по центру!
        spaceAfter=5*mm      # Делаем отступ вниз до следующей строки
    )
    
    style_info = ParagraphStyle(
        'InfoStyle',
        fontName=font_name,
        fontSize=6,
        leading=9            # Межстрочный интервал для мелкого текста (в пунктах)
    )

    # 2. Создаем рамку. 
    # Теперь её высота 29мм (всё, что ниже линии). 
    # topPadding=1*mm дает легкий отступ от самой линии вниз.
    frame = Frame(
        0, 0, width, 29*mm, 
        leftPadding=2*mm, bottomPadding=1*mm, rightPadding=2*mm, topPadding=1*mm,
        showBoundary=1 # Поставь 1, чтобы увидеть границы рамки
    )
    
    # 3. Собираем все строки в один список (story)
    story: list[Flowable] = [
        Paragraph(f"{phone}", style_phone),
        Paragraph(f"Принял(а): {operator_name}", style_info),
        Paragraph(f"Время: {time_str}", style_info),
        Paragraph(f"Описание: {description}", style_info)
    ]
    
    # 4. Высыпаем всё это в рамку, и она сама всё расставит!
    frame.addFromList(story, c)

    # Сохраняем готовый PDF
    c.save()
    print(f"Готово! Этикетка сохранена как {filename}")

if __name__ == "__main__":
    create_pdf_label()