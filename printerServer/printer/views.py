from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import time
import random
import json
# import win32api, win32print, time, os
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib import colors, pagesizes, units
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from bidi.algorithm import get_display
from rtl import reshaper
import textwrap
import pdfkit

GHOSTSCRIPT_PATH = "C:/Program Files/gs/gs9.27/bin/gswin64.exe"
GSPRINT_PATH = 'C:/Program Files/gs/gsprint/gsprint.exe'
FILE = 'C:/Users/CafeBoard/Desktop/file.html'

options = {
    'page-width': '80mm',
    'page-height': '200mm',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
}
pdfkit.from_url('http://127.0.0.1:9001/template/invoice-cash?invoice_id=91', 'out.pdf', options=options)

@csrf_exempt
def print_something(request):
    data = request.POST
    print(data)
    for e in data:
        data = json.loads(e)

    if data['is_customer_print'] == 0:
        invoice_data = []
        item_data_list = []
        for printer_data in data['data']:
            printer_name = printer_data['printer_name']
            if len(printer_data['items']) == 0:
                break

            # config printers

            doc = SimpleDocTemplate("form_letter.pdf", pagesize=(80 * units.mm, 200 * units.mm),
                                    rightMargin=72, leftMargin=72,
                                    topMargin=12, bottomMargin=18)
            pdfmetrics.registerFont(TTFont('IRANSANS', 'C:/Users/CafeBoard/Desktop/font.ttf'))
            # pdfmetrics.registerFont(TTFont('IRANSANS', '/Users/impala69/Desktop/font.ttf'))
            Story = []
            logo = "C:/Users/CafeBoard/Desktop/boardlogored.png"
            # logo = "/Users/impala69/Desktop/boardlogored.png"

            formatted_time = time.ctime()

            im = Image(logo, 1 * units.inch, 1 * units.inch, hAlign='LEFT')
            Story.append(im)
            Story.append(Spacer(1, 12))

            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='IRANSANS'))
            styles.add(ParagraphStyle(name='RIGHT', alignment=TA_RIGHT, fontName='IRANSANS'))
            styles.add(ParagraphStyle(name='Persian', alignment=TA_CENTER, fontName='IRANSANS'))

            ptext = '<font size=6>%s</font>' % formatted_time
            Story.append(Paragraph(ptext, styles["Persian"]))
            Story.append(Spacer(1, 12))

            ptext = '<font size=10>%s</font>' % data['table_name']
            Story.append(Paragraph(get_farsi_bulleted_text(ptext, wrap_length=120), styles["Persian"]))
            Story.append(Spacer(1, 12))

            # end config

            for item in printer_data['items']:
                item_data_list.append(
                    Paragraph(get_farsi_bulleted_text(str(item['numbers']), wrap_length=120), styles["Persian"]))
                item_data_list.append(
                    Paragraph(get_farsi_bulleted_text(item['name'], wrap_length=120), styles["Persian"]))
                invoice_data.append(item_data_list)
                item_data_list = []

            t_style = TableStyle([
                ('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                ('TEXTCOLOR', (1, 1), (-2, -2), colors.black),
                ('VALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
                ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                ('TEXTFONT', (0, -1), (-1, -1), 'IRANSANS'),
                ('VALIGN', (0, -1), (-1, -1), 'RIGHT'),
                ('TEXTFONT', (0, -1), (-1, -1), 'IRANSANS'),
                ('TEXTCOLOR', (0, -1), (-1, -1), colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ])

            t = Table(invoice_data, colWidths=20 * units.mm)
            t.setStyle(t_style)

            Story.append(t)
            Story.append(Spacer(1, 12))

            doc.build(Story)
            invoice_data = []
            print("printing in: %s" % printer_name)

    else:

        doc = SimpleDocTemplate("form_letter.pdf", pagesize=(80 * units.mm, 200 * units.mm),
                                rightMargin=72, leftMargin=72,
                                topMargin=12, bottomMargin=18)
        pdfmetrics.registerFont(TTFont('IRANSANS', '/Users/impala69/Desktop/font.ttf'))
        Story = []
        logo = "/Users/impala69/Desktop/boardlogored.png"

        formatted_time = time.ctime()

        im = Image(logo, 1 * units.inch, 1 * units.inch, hAlign='LEFT')
        Story.append(im)
        Story.append(Spacer(1, 12))

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='IRANSANS'))
        styles.add(ParagraphStyle(name='RIGHT', alignment=TA_RIGHT, fontName='IRANSANS'))
        styles.add(ParagraphStyle(name='Persian', alignment=TA_CENTER, fontName='IRANSANS'))

        ptext = '<font size=6>%s</font>' % formatted_time
        Story.append(Paragraph(ptext, styles["Persian"]))
        Story.append(Spacer(1, 12))

        if data['is_customer_print'] == 1:
            ptext = '<font size=8>%s</font>' % get_farsi_bulleted_text(data['customer_name'], wrap_length=120)
            Story.append(Paragraph(ptext, styles["Persian"]))
            Story.append(Spacer(1, 12))

        ptext = '<font size=10>%s</font>' % data['table_name']
        Story.append(Paragraph(get_farsi_bulleted_text(ptext, wrap_length=120), styles["Persian"]))
        Story.append(Spacer(1, 12))

        invoice_data = []
        item_data_list = []

        item_data_list.append(
            Paragraph(get_farsi_bulleted_text('کل', wrap_length=120), styles["Persian"]))
        item_data_list.append(
            Paragraph(get_farsi_bulleted_text("تعداد", wrap_length=120), styles["Persian"]))
        item_data_list.append(
            Paragraph(get_farsi_bulleted_text("فی", wrap_length=120), styles["Persian"]))
        item_data_list.append(Paragraph(get_farsi_bulleted_text("نام", wrap_length=120), styles["Persian"]))
        invoice_data.append(item_data_list)

        item_data_list = []

        for item in data['items']:
            item_data_list.append(
                Paragraph(get_farsi_bulleted_text(str(item['price']), wrap_length=120), styles["Persian"]))
            item_data_list.append(
                Paragraph(get_farsi_bulleted_text(str(item['numbers']), wrap_length=120), styles["Persian"]))
            item_data_list.append(
                Paragraph(get_farsi_bulleted_text(str(item['item_price']), wrap_length=120), styles["Persian"]))
            item_data_list.append(Paragraph(get_farsi_bulleted_text(item['name'], wrap_length=120), styles["Persian"]))
            invoice_data.append(item_data_list)
            item_data_list = []

        t_style = TableStyle([
            ('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
            ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
            ('VALIGN', (0, 0), (0, -1), 'TOP'),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
            ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
            ('TEXTFONT', (0, -1), (-1, -1), 'IRANSANS'),
            ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
            ('TEXTFONT', (0, -1), (-1, -1), 'IRANSANS'),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ])

        t = Table(invoice_data, colWidths=18 * units.mm)
        t.setStyle(t_style)

        Story.append(t)
        Story.append(Spacer(1, 12))

        doc.build(Story)

    for printer in data['printers']:
        print("Printing in %s" % printer)
        print("Printing in %s" % printer)
        currentprinter = 'Cash'
        params = '-ghostscript "' + GHOSTSCRIPT_PATH + '" -printer "' + currentprinter + '" -copies 1 "C:/Users/CafeBoard/Desktop/form_letter.pdf "'
        print(params)
        win32api.ShellExecute(0, 'open', GSPRINT_PATH, params, 'K', 0)

    return JsonResponse({"response": 'OK'})
