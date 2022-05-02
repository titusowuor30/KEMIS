from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.db.models import  Q
from .forms import *


class home_view(View):
    def get(self, request):
        return render(request,'home.html')

class company_view(View):
    def get(self, request):
        industries=Industry.objects.all()
        return render(request,'pages/company/list.html',{'industries':industries})
    
class result_view(View):
    def get(self, request):
        return render(request,'pages/result/success.html')    


class add_industry(View):
    form_class = add_company
    initial = {'key': 'value'}
    template_name = 'pages/company/add.html'

    def get(self, request, *args, **kwargs):
        data = {}
        form = self.form_class(initial=self.initial)
        data['inputs']=Input.objects.all()
        data['wastes']=WasteProduct.objects.all()
        return render(request, self.template_name, {'form': form,'data':data})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(form)
        if form.is_valid():
           industry=form.save()
           inputsearchkeys=self.request.POST.getlist('inputs')
           wastesearchkeys = self.request.POST.getlist('wastes')
           myval=''
           myval2=''
           i=0
           for j in range(0, len(wastesearchkeys)):
              for i in range(0,len(inputsearchkeys)):
                    print(wastesearchkeys)
                    myval2 = wastesearchkeys[j]
                    print(myval2)
                    selectedwaste2 = WasteProduct.objects.get(name=myval2)
                    industry.wasteproducts.add(selectedwaste2)
                    industry.save()
                    print(selectedwaste2)
                    print(inputsearchkeys)
                    myval=inputsearchkeys[i]
                    print(myval)
                    selectedinput=Input.objects.get(name=myval)
                    industry.inputs.add(selectedinput)
                    industry.save()
                    print(selectedinput)
           # <process form cleaned data>
           return HttpResponseRedirect('/result/')
        return render(request, self.template_name, {'form': form})