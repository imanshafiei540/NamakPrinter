from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import time
import random
import json
import win32api, win32print, time, os
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


def get_farsi_text(text):
    if reshaper.has_arabic_letters(text):
        words = text.split()
        reshaped_words = []
        for word in words:
            if reshaper.has_arabic_letters(word):
                # for reshaping and concating words
                reshaped_text = reshaper.reshape(word)
                # for right to left
                bidi_text = get_display(reshaped_text)
                reshaped_words.append(bidi_text)
            else:
                reshaped_words.append(word)
        reshaped_words.reverse()
        return ' '.join(reshaped_words)
    return text


def get_farsi_bulleted_text(text, wrap_length=None):
    farsi_text = get_farsi_text(text)
    if wrap_length:
        line_list = textwrap.wrap(farsi_text, wrap_length)
        line_list.reverse()

        farsi_text = '<br/>'.join(line_list)
        return '<font>%s</font>' % farsi_text
    return '<font>%s &#x02022;</font>' % farsi_text

GHOSTSCRIPT_PATH = "C:/Program Files/gs/gs9.27/bin/gswin64.exe"
GSPRINT_PATH = 'C:/Program Files/gs/gsprint/gsprint.exe'
FILE = 'C:/Users/CafeBoard/Desktop/file.html'

@csrf_exempt
def print_something(request):
    currentprinter = 'Cash'
    #win32print.SetDefaultPrinter('NowKitchen')
    #win32api.ShellExecute(0, "print", 'C:/Users/CafeBoard/Desktop/file.pdf', None, ".", 0)
    #params = '-ghostscript "' + GHOSTSCRIPT_PATH + '" -printer "' + currentprinter + '" -copies 1 "C:/Users/CafeBoard/Desktop/file.html "'
    #print(params)
    import os

    #os.startfile("C:/Users/CafeBoard/Desktop/file.pdf", "print")
    #win32api.ShellExecute(0, 'open', GSPRINT_PATH, params, 'K', 0)
    #time.sleep(1)
    #win32print.SetDefaultPrinter('NowBar')
    #win32api.ShellExecute(0, "print", 'C:/Users/CafeBoard/Desktop/file.html', None, ".", 0)
    #time.sleep(1)
    #win32print.SetDefaultPrinter('Cash')

    data = request.POST
    print(data)
    for e in data:
        data = json.loads(e)
    doc = SimpleDocTemplate("form_letter.pdf", pagesize=(80 * units.mm, 200 * units.mm),
                            rightMargin=72, leftMargin=72,
                            topMargin=12, bottomMargin=18)
    pdfmetrics.registerFont(TTFont('IRANSANS', 'C:/Users/CafeBoard/Desktop/font.ttf'))
    Story = []
    logo = "C:/Users/CafeBoard/Desktop/boardlogored.png"
    limitedDate = "03/05/2010"

    formatted_time = time.ctime()
    full_name = "Infosys"

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

    if data['is_customer_print'] == 0:
        invoice_data = []
        item_data_list = []
        for item in data['items']:
            item_data_list.append(Paragraph(get_farsi_bulleted_text(str(item['numbers']), wrap_length=120), styles["Persian"]))
            item_data_list.append(Paragraph(get_farsi_bulleted_text(item['name'], wrap_length=120), styles["Persian"]))
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

    else:
        invoice_data = []
        item_data_list = []
        for item in data['items']:
            item_data_list.append(Paragraph(get_farsi_bulleted_text(str(item['price']), wrap_length=120), styles["Persian"]))
            item_data_list.append(Paragraph(get_farsi_bulleted_text(str(item['numbers']), wrap_length=120), styles["Persian"]))
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

        t = Table(invoice_data, colWidths=20 * units.mm)
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
