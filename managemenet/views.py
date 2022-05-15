from urllib import request
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views import View
from django.db.models import  Q
from .forms import *
from django.utils import timezone
from django.views.generic.list import ListView


class home_view(View):
    def get(self, request):
        if request.user.is_authenticated:
           return render(request,'home.html')
        else:
            return redirect('signin_view')

class company_view(View):
    def get(self, request):
        if request.user.is_superuser:
           industries=Industry.objects.all()
        else:   
            industries=Industry.objects.all().filter(user=request.user)   
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
        if not request.user.is_authenticated:
            return redirect('signin_view')
        form = self.form_class(request.POST)
        print(form)
        if form.is_valid():
           industry=form.save(commit=False)
           industry.user=request.user
           industry.save()
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
    

def MatchListView(request,id):
    data = {}
    user_industries = Industry.objects.get(id=id)
    data['user_industries']=user_industries
    loggeduser_wastes=user_industries.wasteproducts.all()
    user_inputs=user_industries.inputs.all()
    matchmatching_industries=[]
    user_wastes=[]
    #matched_inputs=[]
    for waste in loggeduser_wastes:
        industry=Industry.objects.filter(Q(inputs__name__icontains=waste.name) | Q(inputs__description__icontains=waste.description)).values('id','name','location','email','description','inputs__name','inputs__description','wasteproducts__name')
        matchmatching_industries.append(industry)
        user_wastes.append({'name':waste.name,'reuse_plan':waste.reuse_plan,'price':waste.price,'image':waste.image})
    data['matchmatching_industries']=matchmatching_industries[0]
    data['user_wastes']=user_wastes
    data['user_inputs']=user_inputs
   
    print(user_industries)
    print(user_wastes)
    print(matchmatching_industries)
    #print(matched_inputs)
    return render(request, 'pages/company/detail.html', {'data':data}) 