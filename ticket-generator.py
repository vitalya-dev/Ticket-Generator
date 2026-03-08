import os
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame, Flowable, BaseDocTemplate, PageTemplate
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

def create_multipage_label(
    filename="label_output.pdf", 
    logo_path="logo.png", 
    operator_name="@vital...", 
    phone="8 (978) 895-47-13", 
    time_str="2025-05-16 10:47", 
    # Сделали описание гигантским для проверки переноса страниц!
    description="Пу. Выключается. Михеева приняла. "
):
    
    width = 57 * mm
    height = 40 * mm
    
    # --- НАСТРОЙКА ШРИФТОВ ---
    font_name = 'Consolas'
    try:
        # Регистрируем обычный Consolas
        pdfmetrics.registerFont(TTFont(font_name, 'consola.ttf'))
        # Регистрируем жирный Consolas
        pdfmetrics.registerFont(TTFont('Consolas-Bold', 'consolab.ttf'))
        
        pdfmetrics.registerFontFamily(font_name, normal=font_name, bold='Consolas-Bold')
    except Exception as e:
        print("ОШИБКА: Не найден файл шрифта 'consola.ttf' или 'consolab.ttf'!")
        return

    # --- 1. ФУНКЦИЯ ДЛЯ ШАПКИ (будет вызываться на КАЖДОЙ странице) ---
    def draw_header(canvas, doc):
        canvas.saveState()
        
        if os.path.exists(logo_path):
            canvas.drawImage(logo_path, 2*mm, 31*mm, width=8*mm, height=8*mm, mask='auto')

        canvas.setFont(font_name, 9)
        canvas.drawString(12*mm, 35.5*mm, "ООО «ВТИ»")
        
        canvas.setFont(font_name, 4)
        canvas.drawString(12*mm, 33.5*mm, "ул Советская 26, г. Керчь")
        
        canvas.setFont(font_name, 4)
        canvas.drawString(12*mm, 31.5*mm, "8 (978) 762-89-67  8 (978) 010-49-49")

        # Разделительная линия
        canvas.setLineWidth(0.5)
        canvas.line(0*mm, 29*mm, width, 29*mm)
        
        canvas.restoreState()

    # --- 2. НАСТРОЙКА ДОКУМЕНТА И ШАБЛОНА ---
    
    # Создаем базовый документ
    doc = BaseDocTemplate(filename, pagesize=(width, height))
    
    # Наш старый добрый Frame (занимает место строго под линией)
    frame = Frame(
        0, 0, width, 29*mm, 
        leftPadding=2*mm, bottomPadding=1*mm, rightPadding=2*mm, topPadding=1*mm,
        showBoundary=0 
    )
    
    # Создаем шаблон: связываем наш Frame и функцию draw_header
    template = PageTemplate(id='LabelTemplate', frames=[frame], onPage=draw_header)
    doc.addPageTemplates([template])

    # --- 3. НАСТРОЙКА СТИЛЕЙ И ТЕКСТА ---
    style_phone = ParagraphStyle(
        'PhoneStyle', fontName=font_name, fontSize=16, alignment=TA_CENTER, spaceAfter=5*mm      
    )
    style_info = ParagraphStyle(
        'InfoStyle', fontName=font_name, fontSize=6, leading=9            
    )

    # Собираем story. Телефон будет только на первой этикетке! 
    # (если нужно на каждой - скажи, перенесем его в draw_header)
    story: list[Flowable] = [
        Paragraph(f"<b>{phone}</b>", style_phone),
        Paragraph(f"<b>Принял(а):</b> {operator_name}", style_info),
        Paragraph(f"<b>Время:</b> {time_str}", style_info),
        Paragraph(f"<b>Описание:</b> {description}", style_info)
    ]
    
    # --- 4. ЗАПУСК МАГИИ ---
    # Команда build сама разобьет story по страницам!
    doc.build(story)
    print(f"Готово! Многостраничная этикетка сохранена как {filename}")

if __name__ == "__main__":
    create_multipage_label()