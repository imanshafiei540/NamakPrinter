from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# import win32api, win32print, time, os
import pdfkit

GHOSTSCRIPT_PATH = "C:/Program Files/gs/gs9.27/bin/gswin64.exe"
GSPRINT_PATH = 'C:/Program Files/gs/gsprint/gsprint.exe'
FILE = 'C:/Users/CafeBoard/Desktop/file.html'


@csrf_exempt
def print_something(request):
    data = request.POST
    for e in data:
        data = json.loads(e)
    print(data)

    if data['is_customer_print'] == 0:
        for printer_data in data['invoice_data']['data']:
            print(printer_data)
            printer_name = printer_data['printer_name']
            if len(printer_data['items']) == 0:
                break
            else:
                # options = {
                #     'page-width': '80mm',
                #     'page-height': '200mm',
                #     'quiet': '',
                #     'read-args-from-stdin': ''
                # }
                # pdfkit.from_url('http://127.0.0.1:9001/template/invoice-no-cash?invoice_id=%s&printer_name=%s' % (
                #     data['invoice_id'], printer_name), '%s.pdf' % printer_name,
                #                 options=options)
                options = {
                    'page-width': '80mm',
                    'page-height': '200mm',
                    #'quiet': '',
                    #'read-args-from-stdin': ''
                }
                pdfkit.from_url('http://cafeboard.ir:8080/template/invoice-no-cash?invoice_id=%s&printer_name=%s' % (data['invoice_id'], printer_name), 'C:/Users/CafeBoard/Desktop/%s.pdf' % printer_name, options=options)

                print("printing in: %s" % printer_name)
                currentprinter = printer_name
                params = '-ghostscript "' + GHOSTSCRIPT_PATH + '" -printer "' + currentprinter + '" -copies 1 "C:/Users/CafeBoard/Desktop/"' + printer_name + '".pdf "'
                print(params)
                win32api.ShellExecute(0, 'open', GSPRINT_PATH, params, 'K', 0)
                time.sleep(2)
                os.remove("C:/Users/CafeBoard/Desktop/cash.pdf")
                file = open("C:/Users/CafeBoard/Desktop/cash.pdf", 'w')
                file.close()


    else:
        # options = {
        #     'page-width': '80mm',
        #     'page-height': '200mm',
        #     'quiet': '',
        #     'read-args-from-stdin': ''
        # }
        # pdfkit.from_url('http://127.0.0.1:9001/template/invoice-cash?invoice_id=%s' % data['invoice_id'], 'cash.pdf',
        #                 options=options)

        # currentprinter = 'Cash'
        # params = '-ghostscript "' + GHOSTSCRIPT_PATH + '" -printer "' + currentprinter + '" -copies 1 "C:/Users/CafeBoard/Desktop/form_letter.pdf "'
        # print(params)
        # win32api.ShellExecute(0, 'open', GSPRINT_PATH, params, 'K', 0)
        options = [
            ('page-width', '80mm'),
            ('page-height', '200mm'),
            #('quiet', ''),
            #('read-args-from-stdin', '')
        ]
        pdfkit.from_url('http://cafeboard.ir:8080/template/invoice-cash?invoice_id=%s' % data['invoice_id'],
                        'C:/Users/CafeBoard/Desktop/cash.pdf', options=options)
        print('http://cafeboard.ir:8080/template/invoice-cash?invoice_id=%s' % data['invoice_id'])
        print("wkhtmltopdf --page-width 80mm --read-args-from-stdin --page-height 200mm http://cafeboard.ir:8080/template/invoice-cash?invoice_id=%s C:/Users/CafeBoard/Desktop/cash.pdf" % (data['invoice_id']))
        currentprinter = 'Cash'
        params = '-ghostscript "' + GHOSTSCRIPT_PATH + '" -printer "' + currentprinter + '" -copies 1 "C:/Users/CafeBoard/Desktop/cash.pdf "'
        print(params)
        win32api.ShellExecute(0, 'open', GSPRINT_PATH, params, 'K', 0)
        time.sleep(2)
        os.remove("C:/Users/CafeBoard/Desktop/cash.pdf")
        file = open("C:/Users/CafeBoard/Desktop/cash.pdf", 'w')
        file.close()

    return JsonResponse({"response": 'OK'})
