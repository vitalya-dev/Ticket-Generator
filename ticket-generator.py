import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame, Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER 

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
    
    # --- НАСТРОЙКА ШРИФТОВ (Добавили жирный шрифт) ---
    font_name = 'Arial'
    try:
        # Регистрируем обычный шрифт
        pdfmetrics.registerFont(TTFont(font_name, 'arial.ttf'))
        # Регистрируем жирный шрифт (файл arialbd.ttf должен быть рядом со скриптом!)
        pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
        
        # Объединяем их в семейство, чтобы ReportLab знал, что использовать для тега <b>
        pdfmetrics.registerFontFamily(font_name, normal=font_name, bold='Arial-Bold')
    except Exception as e:
        print("ОШИБКА: Не найден файл шрифта 'arial.ttf' или 'arialbd.ttf'!")
        print("Убедитесь, что оба файла лежат в папке со скриптом.")
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
        alignment=TA_CENTER, 
        spaceAfter=5*mm      
    )
    
    style_info = ParagraphStyle(
        'InfoStyle',
        fontName=font_name,
        fontSize=6,
        leading=9            
    )

    # 2. Создаем рамку
    frame = Frame(
        0, 0, width, 29*mm, 
        leftPadding=2*mm, bottomPadding=1*mm, rightPadding=2*mm, topPadding=1*mm,
        showBoundary=0 # Вернул 0, чтобы скрыть рамку
    )
    
    # 3. Собираем все строки в один список (story)
    # Используем HTML-тег <b> для жирного шрифта
    story: list[Flowable] = [
        Paragraph(f"<b>{phone}</b>", style_phone),
        Paragraph(f"<b>Принял(а):</b> {operator_name}", style_info),
        Paragraph(f"<b>Время:</b> {time_str}", style_info),
        Paragraph(f"<b>Описание:</b> {description}", style_info)
    ]
    
    # 4. Высыпаем всё это в рамку, и она сама всё расставит!
    frame.addFromList(story, c)

    # Сохраняем готовый PDF
    c.save()
    print(f"Готово! Этикетка сохранена как {filename}")

if __name__ == "__main__":
    create_pdf_label()