from django.contrib import admin
from .models import *
#report
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def export_to_pdf(modeladmin, request, queryset):
   # Create a new PDF
   response = HttpResponse(content_type='application/pdf')
   response['Content-Disposition'] = 'attachment; filename="report.pdf"'

   # Generate the report using ReportLab
   doc = SimpleDocTemplate(response, pagesize=letter)

   elements = []

   # Define the style for the table
   style = TableStyle([
       ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
       ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
       ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
       ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
       ('FONTSIZE', (0, 0), (-1, 0), 12),
       ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
       ('BACKGROUND', (0, 1), (-1, -1), colors.white),
       ('GRID', (0, 0), (-1, -1), 1, colors.darkgrey),
   ])

   # Create the table headers
   headers = ['userid', 'orderstatus', 'phonenumber', 'address','totalbill','paymentmode','datetime']

   # Create the table data
   data = []
   for obj in queryset:
       data.append([obj.userid.name, obj.orderstatus, obj.phonenumber, obj.address,obj.totalbill,obj.paymentmode,obj.datetime])

   # Create the table
   t = Table([headers] + data, style=style)

   # Add the table to the elements array
   elements.append(t)

   # Build the PDF document
   doc.build(elements)

   return response


export_to_pdf.short_description = "Export to PDF"

def export_as_pdf(modeladmin, request, queryset):
   # Create a new PDF
   response = HttpResponse(content_type='application/pdf')
   response['Content-Disposition'] = 'attachment; filename="report.pdf"'

   # Generate the report using ReportLab
   doc = SimpleDocTemplate(response, pagesize=letter)

   elements = []

   # Define the style for the table
   style = TableStyle([
       ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
       ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
       ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
       ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
       ('FONTSIZE', (0, 0), (-1, 0), 12),
       ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
       ('BACKGROUND', (0, 1), (-1, -1), colors.white),
       ('GRID', (0, 0), (-1, -1), 1, colors.darkgrey),
   ])

   # Create the table headers
   headers = ["pitchid","userid","bookingdate","bookingtime","phonenumber","name"]

   # Create the table data
   data = []

   for obj in queryset:
       data.append([obj.userid.name, obj.pitchid.name, obj.bookingdate, obj.bookingtime,obj.phonenumber,obj.name,obj.datetime])

   # Create the table
   t = Table([headers] + data, style=style)

   # Add the table to the elements array
   elements.append(t)

   # Build the PDF document
   doc.build(elements)

   return response


export_as_pdf.short_description = "Export as PDF"




# Register your models here.


class showusertable(admin.ModelAdmin):
    list_display = ["name","email","password","phonenumber","gender"]

admin.site.register(usertable,showusertable)

class showcategory(admin.ModelAdmin):
    list_display = ["name"]

admin.site.register(categorytable,showcategory)

class showpitchtable(admin.ModelAdmin):
    list_display = ["name","areaid","phonenumber","description","price","pitch_photo"]

admin.site.register(pitchtable,showpitchtable)

class showitemtable(admin.ModelAdmin):
    list_display = ["name","catid","item_photo","price","discription","brand"]

admin.site.register(itemtable,showitemtable)

class showbookingtable(admin.ModelAdmin):
    list_display = ["pitchid","userid","bookingdate","bookingtime","phonenumber","name","datetime","paymentmode"]
    list_filter = ['datetime']
    actions = [export_as_pdf]

admin.site.register(bookingtable,showbookingtable)

class showareatable(admin.ModelAdmin):
    list_display = ["name","address"]

admin.site.register(areatable,showareatable)

class showordertable(admin.ModelAdmin):
    list_display = ["userid","orderstatus","phonenumber","address","totalbill","paymentmode","datetime"]
    list_filter = ['datetime']
    actions = [export_to_pdf]

admin.site.register(ordertable,showordertable)

class showcarttable(admin.ModelAdmin):
    list_display = ["userid","itemid","quantity","cartstatus","total","orderid"]

admin.site.register(carttable,showcarttable)

class showfeedbacktable(admin.ModelAdmin):
    list_display = ["name","rating","comment"]

admin.site.register(feedbacktable,showfeedbacktable)

class showcomplaintable(admin.ModelAdmin):
    list_display = ["userid","date","time","message","subject"]

admin.site.register(complaintable,showcomplaintable)

class showproductimages(admin.ModelAdmin):
    list_display = ["itemid","pro_photo"]

admin.site.register(productimages,showproductimages)

class showturfimages(admin.ModelAdmin):
    list_display = ["turfid","turf_photo"]

admin.site.register(turfimages,showturfimages)