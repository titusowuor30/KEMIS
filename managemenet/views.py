from urllib import request
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from .forms import *
from django.utils import timezone
from django.views.generic.list import ListView
import secrets
from django.contrib.auth import logout
from django.contrib import messages
from .payment_views import send_email,sendSMS

invoice_id = ""
class home_view(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'home.html')
        else:
            return redirect('signin_view')


def invoiceListView(request):
    guest_user = True
    obj = {}
    if len(request.user.industries.all()) < 1 and request.user.is_superuser:
        obj = waste_invoice.objects.all()
        messages.info(
            request, "Hi Admin, Viewing invoices for other companies?\tYou do not have any registered company yet!")
        return render(request, "pages/company/invoices.html", {"object_list": obj, 'guest_user': guest_user})
    elif len(request.user.industries.all()) < 1 and not request.user.is_superuser:
        messages.info(request, "Hi {}, you\'re being redirected to home page!\tYou do not have any invoices yet!".format(
            request.user.username))
        return redirect("/")
    try:
        matching_company = request.user.industries.all()[0]
        print(matching_company)
    except Exception as e:
        print(e)
    for item in waste_invoice.objects.all():
        if request.user == item.created_by:
            guest_user = False
    print("Guest User => "+str(guest_user))
    for object in waste_invoice.objects.all():
        if request.user == object.created_by:
            print(object.created_by)
            obj = waste_invoice.objects.filter(created_by=request.user)
            print(obj)
            return render(request, "pages/company/invoices.html", {"object_list": obj, 'guest_user': guest_user})
        else:
            obj = waste_invoice.objects.filter(companyB=matching_company)
            print(request.session.get('amount'))
            print(obj)
        return render(request, "pages/company/invoices.html", {"object_list": obj, 'guest_user': guest_user})
    return render(request, "pages/company/invoices.html", {"object_list": obj, 'guest_user': guest_user})


class company_view(View):
    def get(self, request):
        if request.user.is_superuser:
            industries = Industry.objects.all()
        else:
            industries = Industry.objects.all().filter(user=request.user)
        return render(request, 'pages/company/list.html', {'industries': industries})


class result_view(View):
    def get(self, request):
        return render(request, 'pages/result/success.html')


class add_industry(View):
    form_class = add_company
    waste_form = addWasteForm
    inputs_form = inputsForm
    initial = {'key': 'value'}
    template_name = 'pages/company/add.html'

    def get(self, request, *args, **kwargs):
        data = {}
        form = self.form_class(initial=self.initial)
        add_waste_form = self.waste_form(initial=self.initial)
        addinputs_form = self.inputs_form(initial=self.initial)
        data['inputs'] = Input.objects.all()
        data['wastes'] = WasteProduct.objects.all()
        return render(request, self.template_name, {'form': form, 'addinputs_form': addinputs_form, 'add_waste_form': add_waste_form, 'data': data})

    def post(self, request, *args, **kwargs):
        if "wasteform" in self.request.POST:
            form = addWasteForm(self.request.POST, self.request.FILES)
            print(self.request.POST)
            if form.is_valid():
                form.save()
                return redirect('add-industry')
        if "inputsform" in self.request.POST:
            form = inputsForm(self.request.POST)
            print(self.request.POST)
            if form.is_valid():
                form.save()
                return redirect('add-industry')
        if not request.user.is_authenticated:
            return redirect('signin_view')
        form = self.form_class(self.request.POST)
        print(form)
        if form.is_valid():
            industry = form.save(commit=False)
            industry.user = request.user
            industry.save()
            inputsearchkeys = self.request.POST.getlist('inputs')
            wastesearchkeys = self.request.POST.getlist('wastes')
            myval = ''
            myval2 = ''
            i = 0
            for j in range(0, len(wastesearchkeys)):
                for i in range(0, len(inputsearchkeys)):
                    print(wastesearchkeys)
                    myval2 = wastesearchkeys[j]
                    print(myval2)
                    selectedwaste2 = WasteProduct.objects.get(name=myval2)
                    industry.wasteproducts.add(selectedwaste2)
                    industry.save()
                    print(selectedwaste2)
                    print(inputsearchkeys)
                    myval = inputsearchkeys[i]
                    print(myval)
                    selectedinput = Input.objects.get(name=myval)
                    industry.inputs.add(selectedinput)
                    industry.save()
                    print(selectedinput)
            # <process form cleaned data>
            return HttpResponseRedirect('/result/')
        return render(request, self.template_name, {'form': form})


def MatchListView(request, id):
    data = {}
    user_industry_id = id
    user_industries = Industry.objects.get(id=id)
    data['user_industries'] = user_industries
    loggeduser_wastes = user_industries.wasteproducts.all()
    user_inputs = user_industries.inputs.all()
    matchmatching_industries = []
    user_wastes = []
    # matched_inputs=[]
    for waste in loggeduser_wastes:
        industry = Industry.objects.filter(Q(inputs__name__icontains=waste.name) | Q(inputs__description__icontains=waste.description)).values(
            'id', 'name', 'location', 'email', 'description', 'inputs__id', 'inputs__name', 'inputs__description', 'wasteproducts__id', 'wasteproducts__name', 'wasteproducts__description')
        matchmatching_industries.append(industry)
        user_wastes.append({'id': waste.id, 'name': waste.name, 'reuse_plan': waste.reuse_plan,
                           'price': waste.price, 'image': waste.image})
    data['matchmatching_industries'] = matchmatching_industries[0]
    data['user_wastes'] = user_wastes
    data['user_inputs'] = user_inputs
    data['id'] = user_industry_id

    print(user_industries)
    print(user_wastes)
    print(matchmatching_industries)
    print(data['id'])
    return render(request, 'pages/company/detail.html', {'data': data})


def CreateInvoice(request, current_companyid, matching_companyid, waste_id):
    data = {}
    global invoice_id
    invoice_id = secrets.token_hex(nbytes=8).upper()
    print(invoice_id)
    current_user_company = request.user.industries.get(id=current_companyid)
    matching_company = Industry.objects.get(id=matching_companyid)
    data['current_company'] = current_user_company
    data['matching_company'] = matching_company
    waste = WasteProduct.objects.get(id=waste_id)
    data['waste'] = WasteProduct.objects.get(id=waste_id)
    data['invoice_id'] = invoice_id
    data['amount'] = waste.price
    data['recycle_plan'] = waste.reuse_plan
    if request.method == 'POST':
        invoice = waste_invoice()
        invoice.invoice_id = invoice_id
        invoice.created_by = request.user
        invoice.companyA = current_user_company
        invoice.companyB = matching_company
        invoice.waste = waste
        print("Mass:"+request.POST.get("mass"))
        if request.POST.get("mass") == None or '':
            invoice.weight = float(0)
        else:
            invoice.weight = float(request.POST.get("mass"))
        if request.POST.get("trcost") == None or '':
            invoice.transportation = float(1)
        else:
            invoice.transportation = float(request.POST.get("trcost"))
        if request.POST.get("cost") == None or '':
            invoice.amount = float(0)
        else:
            invoice.amount = float(request.POST.get("cost"))
        invoice.payment_method = request.POST.get("mpesa")
        invoice.message = request.POST.get("message")
        invoice.save()
        print(request.POST.get("cost"))
        if request.POST.get("email") is not None:
            send_email("New Invoice #ID {}".format(invoice_id), request.POST.get("message"))
        if request.POST.get("sms") is not None:
            sendSMS("New Invoice #ID {}".format(invoice_id), request.POST.get("message"))
        return redirect("invoices")
    return render(request, 'pages/company/createinvoice.html', {'data': data})


def select_pay_method(request, id):
    data = waste_invoice.objects.get(id=id)
    return render(request, 'pages/payments/chose_pay_method.html', {'data': data})


def reject_invoice(request, id):
    invoice = waste_invoice.objects.get(id=id)
    invoice.status="Rejected"
    invoice.save()
    return redirect("invoices")

def delete_invoice(request,id):
    if request.method=='POST':
        invoice=waste_invoice.objects.get(id=id)
        print(invoice)
        invoice.delete()
    return redirect("invoices")


