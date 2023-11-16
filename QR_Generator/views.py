from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.conf import settings
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,portrait
from reportlab_qrcode import QRCodeImage
from PIL import Image
from fpdf import FPDF
from PyPDF2 import PdfMerger, PdfReader
from .models import QR
import os
import qrcode
from qrcode import *
import time, uuid, pymongo

# Create your views here.

def generatePDF(path, name) :
    w,h = 50,50
    pos_x = 0
    pos_y = 0
    counter_y = 15
    counter_x = 0
    filename = str(name) + ".pdf"
    pdf = FPDF(orientation = 'P', unit = "pt", format = 'A4')
    pdf.add_page()
    for p in path :
        pdf.image(p,pos_x,pos_y,w,h)
        pos_y = pos_y + 50
        if path.index(p) == counter_y :
            pos_x = pos_x + 50
            pos_y = 0
            counter_y = counter_y + 16
            counter_x = counter_x + 1
    pdf.output(filename, "F")
    return pdf

def generate_pdf (path, name) :
    logo= '/home/natnaelabebe/Documents/Projects/RungoQRCode/QRCode/logo2.png'
    w,h = 50,50
    pos_x = 0
    pos_y = 0
    counter_y = 6
    counter_x = 0
    filename = str(name) + ".pdf"
    pdf = FPDF(orientation = 'P', unit = "pt", format = 'A4')
    pdf.add_page()
    for p in path :
        #pdf.image(logo,pos_x+12,pos_y,20,60)
        pdf.image(p,pos_x,pos_y+60,w,h)
        pos_y = pos_y + 111
        if path.index(p) == counter_y :
            pos_x = pos_x + 50
            pos_y = 0
            counter_y = counter_y + 7
            counter_x = counter_x + 1
    pdf.output(filename, "F")
    return pdf
@api_view(['POST'])
def generate (request) :

    client = pymongo.MongoClient("mongodb+srv://natnaelabebelab:OFuVzf4e7ad6Pweq@qrcode.f5ithts.mongodb.net/?retryWrites=true&w=majority")
 
    # Database Name
    db = client["QRCode"]
    # Collection Name
    col = db["QR_Generator_qr"]
    
    if request.method == 'POST' :
        amount = request.POST.get('amount')
        tag = request.POST.get('tag')

        used = []
        duplicated = 0
        path = []

        for i in range (int(amount)) :
            index = uuid.uuid4()
            qr = qrcode.QRCode(version = 1, box_size = 10,border = 5)
            if (used == '') or (used != '' and index not in used) :
                #img = make(str(index))
                img_name = 'qr' + str(time.time()) + '.png'
                #img.save(settings.MEDIA_ROOT + '/' + img_name)
                qr.add_data(str(index))
                # dash qr manager
                qr.make(fit = True)
                img = qr.make_image(fill_color = 'black',back_color = 'white', size=50 * mm)
                img.save(settings.MEDIA_ROOT + '/' + img_name)
                path.append(settings.MEDIA_ROOT + '/' + img_name)
                used.append(str(index))
        
                # insert row (Date and amount left)
                data = {
                    'id': str(index),
                    'agent_id': '',
                    'product_id' : '',
                    'generated_date' : '',
                    'amount' : amount,
                    'tag' : tag
                }

                col.insert_one(data)

            else :
                duplicated = duplicated + 1
                continue
        
        page_number = int(int(amount) / 192) + 1
        inital_index = 0
        final_index = 193
        for num in range(page_number) :
            #counter = counter + num
            generatePDF(path[inital_index:final_index], num)
            inital_index = inital_index + 193
            final_index = final_index + 193
            #if counter == page_number - 1 :
             #   break
            merger = PdfMerger()
            merger.append(PdfReader(open('0.pdf', 'rb')))
            filename = str(num) + ".pdf"
            if num != 0 :
                filename2 = str(num - 1) + ".pdf"
                merger.append(PdfReader(open(filename2, 'rb')))
                merger.append(PdfReader(open(filename, 'rb')))
            merger.write("Final.pdf")
        return JsonResponse({'Duplicated':duplicated, 'Generated':len(used)})

@api_view(['POST'])
def generate_qrcode (request) :

    client = pymongo.MongoClient("mongodb+srv://natnaelabebelab:OFuVzf4e7ad6Pweq@qrcode.f5ithts.mongodb.net/?retryWrites=true&w=majority")
 
    # Database Name
    db = client["QRCode"]
    # Collection Name
    col = db["QR_Generator_qr"]

    if request.method == 'POST' :
        amount = request.POST.get('amount')
        tag = request.POST.get('tag')

        used = []
        duplicated = 0
        path = []

        for i in range (int(amount)) :
            index = uuid.uuid4() # check index isnot found in DB
            qr = qrcode.QRCode(version = 1, box_size = 10,border = 5)
            if (used == '') or (used != '' and index not in used) :
                #img = make(str(index))
                img_name = 'qr' + str(time.time()) + '.png'
                #img.save(settings.MEDIA_ROOT + '/' + img_name)
                qr.add_data(str(index))
                qr.make(fit = True)
                img = qr.make_image(fill_color = 'black',back_color = 'white', size=50 * mm)
                img.save(settings.MEDIA_ROOT + '/' + img_name)
                path.append(settings.MEDIA_ROOT + '/' + img_name)
                used.append(str(index))
        
                # insert row (Date and amount left)
                data = {
                    'id': str(index),
                    'agent_id': '',
                    'product_id' : '',
                    'generated_date' : '',
                    'amount' : amount,
                    'tag' : tag,
                    'fiber_tag' : ''
                }

                col.insert_one(data)

            else :
                duplicated = duplicated + 1
                continue
        
        page_number = int(int(amount) / 84) + 1
        inital_index = 0
        final_index = 85
        for num in range(page_number) :
            #counter = counter + num
            generate_pdf(path[inital_index:final_index], num)
            inital_index = inital_index + 85
            final_index = final_index + 85
            #if counter == page_number - 1 :
             #   break
            merger = PdfMerger()
            merger.append(PdfReader(open('0.pdf', 'rb')))
            filename = str(num) + ".pdf"
            if num != 0 :
                filename2 = str(num - 1) + ".pdf"
                merger.append(PdfReader(open(filename2, 'rb')))
                merger.append(PdfReader(open(filename, 'rb')))
            merger.write("Final.pdf")
        return JsonResponse({'Duplicated':duplicated, 'Generated':len(used)})

def scan (request, qr_id) :
    client = pymongo.MongoClient("mongodb+srv://natnaelabebelab:OFuVzf4e7ad6Pweq@qrcode.f5ithts.mongodb.net/?retryWrites=true&w=majority")
 
    # Database Name
    db = client["QRCode"]
    # Collection Name
    col_qrcode = db["QR_Generator_qr"]

    # first check qr id exists
    qrcode = col_qrcode.find_one({'id' : qr_id})
    if qrcode is None :
        return render(request, 'error.html') # page not found
    return render(request, 'fibertag.html',{'qr_id':qr_id})

def verify_product (request) :
    client = pymongo.MongoClient("mongodb+srv://natnaelabebelab:OFuVzf4e7ad6Pweq@qrcode.f5ithts.mongodb.net/?retryWrites=true&w=majority")
 
    # Database Name
    db = client["QRCode"]
    # Collection Name
    col_qrcode = db["QR_Generator_qr"]
    col_seller = db["Seller_seller"]
    col_product = db["Product_product"]

    if request.method == 'POST' :
        qr_id = request.POST.get('qrcode')
        tin = request.POST.get('TIN')
        passcode = request.POST.get('passcode')

        qrcode = col_qrcode.find_one({'id' : qr_id})
        if qrcode is None :
            return render(request, 'error.html') # page not found

        seller = col_seller.find_one({'id' : qrcode.get('agent_id')})
        if seller is None :
            return render(request, 'index.html',{'error_msg':'Seller not found!'}) # no seller found for qrcode
        elif seller.get('TIN') != tin :
            return render(request,'index.html',{'error_msg':'TIN number not found!'}) # if tin not match
        elif seller.get('passcode') != passcode :
            return render(request, 'index.html',{'error_msg':'Passcode is invalid!'}) # if passcode not match
        else :
            # find the product under qrcode
            return redirect('https://gofer.et/rungo/product')
    return render(request, 'index.html')

def verfiy_fibertag (request) :
    client = pymongo.MongoClient("mongodb+srv://natnaelabebelab:OFuVzf4e7ad6Pweq@qrcode.f5ithts.mongodb.net/?retryWrites=true&w=majority")
 
    # Database Name
    db = client["QRCode"]
    # Collection Name
    col_qrcode = db["QR_Generator_qr"]
    col_seller = db["Seller_seller"]

    if request.method == 'POST' :
        qr_id = request.POST.get('qrcode')
        fiber_tag = request.POST.get('fibertag')

        qrcode = col_qrcode.find_one({'$and':[ {'id':qr_id}, {'fiber_tag':fiber_tag}]})
        if qrcode is None :
            return render(request, 'error.html') # page not found
        else :
            return redirect('https://gofer.et/rungo/product')
    return render(request, 'fibertag.html')

@api_view(['DELETE'])
def delete_qrs (request) :
    client = pymongo.MongoClient("mongodb+srv://natnaelabebelab:OFuVzf4e7ad6Pweq@qrcode.f5ithts.mongodb.net/?retryWrites=true&w=majority")
 
    # Database Name
    db = client["QRCode"]
    # Collection Name
    col = db["QR_Generator_qr"]

    if request.method == 'DELETE' :
        col.delete_many({})
        return JsonResponse({
            'Msg':'Delete QRCodes'
        })
    return JsonResponse({
        'Msg':'Operation failed'
    })
