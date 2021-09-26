from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, StreamingHttpResponse, FileResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .forms import PartnerModelForm, StockModelForm, ProductModelForm, DealModelForm, DealProductModelForm, ReportModelForm, ReportDateForm, SignatureFileForm
from .models import Partner, Stock, Product, Deal, DealProduct, DealType

from wsgiref.util import FileWrapper
import os
from stock.classes.report import collect_data_for_report
from stock.classes.utils import generate_report
from stock.classes.verify_signature import verify_signature
# CRUD

# GET -> Retrieve / List

# POST -> Create / Update / DELETE

# Create Retrieve Update Delete

def get_object_by_url_name(object_name):
    object_list = {
    'partner': Partner,
    'stock': Stock,
    'product': Product,
    'deal': [Deal, DealProduct]
    }
    return object_list[object_name]

def get_object_form_by_url_name(request, object_name):
    object_form_list = {
    'partner': PartnerModelForm(request.POST or None, request.FILES or None),
    'stock': StockModelForm(request.POST or None, request.FILES or None),
    'product': ProductModelForm(request.POST or None, request.FILES or None),
    }
    return object_form_list[object_name]


def get_object_form_by_url_name_with_instance(request, object_name, obj):
    object_form_list = {
    'partner': PartnerModelForm(request.POST or None, instance=obj),
    'stock': StockModelForm(request.POST or None, instance=obj),
    'product': ProductModelForm(request.POST or None, instance=obj),
    }
    return object_form_list[object_name]


def objects_list_view(request, object_name):
    # list out objects
    # could be search
    current_object = get_object_by_url_name(object_name)
    qs = current_object.objects.all()
    template_name = 'objects/{0}_list.html'.format(object_name)
    create_url = 'new/'.format(object_name)
    context = {'object_list': qs, 'create_url': create_url}
    return render(request, template_name, context)

def deal_list_view(request):
    deal_object = Deal
    qs_deal = deal_object.objects.all()
    deals_dictionary = fill_deal_dictionary(qs_deal)
    template_name = 'objects/deal_list.html'
    create_url = 'new/'
    generate_report_url = 'generate_report/'
    context = {
        'deals_dictionary': deals_dictionary,
        'create_url': create_url,
        'generate_report_url': generate_report_url
        }
    return render(request, template_name, context)


# def generate_report_view(request):
#     template_name = 'report_generation.html'
#     deal_form = ReportModelForm(request.POST or None)
#     report_date_form = ReportDateForm(request.POST or None)
#     deals_list = []
#     if deal_form.is_valid():
#         partner_data = deal_form.cleaned_data
#         if report_date_form.is_valid():
#             date_data = report_date_form.cleaned_data
#             deals_list = Deal.objects.filter(partner_id=partner_data['partner_id'],
#                                              deal_type=DealType.objects.get(value='Продажа'),
#                                              date__range=[date_data['start_date'], date_data['finish_date']])
#             report_info = collect_data_for_report(deals_list, partner_data['partner_id'], date_data)
#             generate_report(report_info)
#             path_to_zip = "media/report.zip"
#             response = HttpResponse(FileWrapper(open(path_to_zip,'rb')), content_type='application/zip')
#             response['Content-Disposition'] = 'attachment; filename="report.zip"'
#             return response
#             #return send_from_directory('/home/bobkovs/PycharmProjects/Documents/', 'report.zip', as_attachment=True)
#     context = {
#         'deal_form': deal_form,
#         'date_form': report_date_form
#     }
#     return render(request, template_name, context)


def fill_deal_dictionary(deal_list):
    deal_dictionary = {}
    for deal in deal_list:
        products = DealProduct.objects.filter(deal_id=deal.id)
        amount_of_deal = calculate_amount_of_deal(deal.deal_type, products)
        deal_dictionary[deal] = [products, amount_of_deal]
    return deal_dictionary

def calculate_amount_of_deal(deal_type, deal_products):
    amount_of_deal = 0.00
    print(deal_type)
    if str(deal_type) == 'Покупка':
        for deal_product in deal_products:
            product_object = Product.objects.get(id=deal_product.product_id.id)
            amount_of_deal += float(product_object.purchase_price) * int(deal_product.count)
    elif str(deal_type) == 'Продажа':
        for deal_product in deal_products:
            product_object = Product.objects.get(id=deal_product.product_id.id)
            amount_of_deal += float(product_object.purchase_price) * int(deal_product.count)
    return amount_of_deal


# @login_required
@staff_member_required
def deal_create_view(request):
    template_name = 'objects/deal_create_form.html'
    form = DealModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect("/stock/deal/{0}/new-product/".format(obj.id))
    context = {'form': form}
    return render(request, template_name, context)

# @login_required
@staff_member_required
def deal_product_create_view(request, id):
    deal_obj = get_object_or_404(Deal, id=id)
    deal_products_list = DealProduct.objects.filter(deal_id=deal_obj)
    template_name = 'objects/deal_product.html'
    form = DealProductModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.deal_id = deal_obj
        obj.save()
        return redirect("/stock/deal/{0}/new-product/".format(id))
    context = {'form': form, 'deal_products_list': deal_products_list}
    return render(request, template_name, context)

# def verify_signatyre_view(request):
#     form = SignatureFileForm(request.POST or None, request.FILES or None)
#     template_name = 'sign_check.html'
#     if form.is_valid():
#         data = form.cleaned_data
#         print(request.FILES)
#         handle_uploaded_file(request.FILES['report'], 'report')
#         handle_uploaded_file(request.FILES['signature'], 'signature')
#         handle_uploaded_file(request.FILES['public_key'], 'public_key')
#         result = verify_signature()
#         os.remove('Отчет.docx')
#         os.remove('Подпись.txt')
#         os.remove('Ключ.pem')
#         return render(request, 'result.html', {'result': result})
#     context = {'form': form}
#     return render(request, template_name, context)

def handle_uploaded_file(f, file_name):
    names = {
      'report': 'Отчет.docx',
      'signature': 'Подпись.txt',
      'public_key': 'Ключ.pem'
    }
    with open(names[file_name], 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)





# @login_required
@staff_member_required
def objects_create_view(request, object_name):
    # create objects
    # ? use a form
    # request.user -> return something
    form = get_object_form_by_url_name(request, object_name)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return redirect("/stock/{0}".format(object_name))
    template_name = 'form.html'
    context = {'form': form}
    return render(request, template_name, context)




def objects_detail_view(request, object_name, slug):
    # 1 object -> detail view
    obj = get_object_or_404(get_object_by_url_name(object_name), slug=slug)
    template_name = 'stock/detail.html'
    context = {"object": obj}
    return render(request, template_name, context)




@staff_member_required
def objects_update_view(request, object_name, id):
    obj = get_object_or_404(get_object_by_url_name(object_name), id=id)
    form = get_object_form_by_url_name_with_instance(request, object_name, obj)
    if form.is_valid():
        form.save()
        return redirect("/stock/{0}".format(object_name))
    template_name = 'form.html'
    context = {"title": "Изменение записи".format(obj.name), "form": form}
    return render(request, template_name, context)


@staff_member_required
def objects_delete_view(request, object_name, id):
    obj = get_object_or_404(get_object_by_url_name(object_name), id=id)
    template_name = 'stock/delete.html'
    if request.method == "POST":
        obj.delete()
        return redirect("/stock/{0}".format(object_name))
    context = {"object": obj}
    return render(request, template_name, context)



def verify_signatyre_view(request):
    form = SignatureFileForm(request.POST or None, request.FILES or None)
    template_name = 'sign_check.html'
    if form.is_valid():
        data = form.cleaned_data
        print(request.FILES)
        handle_uploaded_file(request.FILES['report'], 'report')
        handle_uploaded_file(request.FILES['signature'], 'signature')
        handle_uploaded_file(request.FILES['public_key'], 'public_key')
        result = verify_signature()
        os.remove('Отчет.docx')
        os.remove('Подпись.txt')
        os.remove('Ключ.pem')
        return render(request, 'result.html', {'result': result})
    context = {'form': form}
    return render(request, template_name, context)


def handle_uploaded_file(f, file_name):
    names = {
      'report': 'Отчет.docx',
      'signature': 'Подпись.txt',
      'public_key': 'Ключ.pem'
    }
    with open(names[file_name], 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def generate_report_view(request):
    template_name = 'report_generation.html'
    deal_form = ReportModelForm(request.POST or None)
    report_date_form = ReportDateForm(request.POST or None)
    deals_list = []
    if deal_form.is_valid():
        partner_data = deal_form.cleaned_data
        if report_date_form.is_valid():
            date_data = report_date_form.cleaned_data
            deals_list = Deal.objects.filter(partner_id=partner_data['partner_id'],
                                             deal_type=DealType.objects.get(value='Продажа'),
                                             date__range=[date_data['start_date'], date_data['finish_date']])
            report_info = collect_data_for_report(deals_list, partner_data['partner_id'], date_data)
            generate_report(report_info)
            path_to_zip = "media/report.zip"
            response = HttpResponse(FileWrapper(open(path_to_zip,'rb')), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="report.zip"'
            return response
            #return send_from_directory('/home/bobkovs/PycharmProjects/Documents/', 'report.zip', as_attachment=True)
    context = {
        'deal_form': deal_form,
        'date_form': report_date_form
    }
    return render(request, template_name, context)



