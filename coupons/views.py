import os
import StringIO

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings

from coupons.models import CouponSheet, Sheet, Coupon
from coupons.forms import CouponForm, CouponSheetForm
from django.views.generic.list import ListView, MultipleObjectMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView


def home(request, template_name="coupons/home.html"):    
    sheets = Sheet.objects.all()
    coupons = Coupon.objects.all()
    
    return render(
        request,
        template_name,
        {'sheets' : sheets,
         'coupons' : coupons},
    )
    
    

class SheetListView(ListView):
    model = Sheet
    

class SheetDetailView(MultipleObjectMixin, DetailView):
    model = Sheet
    pk_url_kwarg = 'sheet_id'
    
    def get_paginate_by(self, queryset):
        return len(self.coord_table)
    
    def dispatch(self, *args, **kwargs):
        self.sheet = get_object_or_404(Sheet, pk=kwargs['sheet_id'])
        self.coord_table = self.sheet._get_coord_table()
        self.object_list = self.sheet.get_all_coupons()
        return super(SheetDetailView, self).dispatch(*args, **kwargs)
    
    
def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))        
    return path


# def pdf_view(request, sheet_id):
#     sheet = get_object_or_404(Sheet, pk=sheet_id)
#     html = sheet.as_html()   
# 
#     result = StringIO.StringIO()
#     pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), 
#                             result, link_callback=fetch_resources)
#     
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), \
#              mimetype='application/pdf')
#     return HttpResponse('Gremlins ate your pdf!') 

class CouponDetailView(DetailView):
    model = Coupon
    pk_url_kwarg = 'coupon_id'
    

class CouponAddView(CreateView):
    model = Coupon
    form_class = CouponForm
    template_name="coupons/coupon_form.html"
    
    def get_success_url(self):
        return reverse('home')


class CouponEditView(UpdateView):
    model = Coupon
    pk_url_kwarg = 'coupon_id'
    form_class = CouponForm
    template_name="coupons/coupon_form.html"
    
    def get_context_data(self, *args, **kwargs):
        context = super(CouponEditView, self).get_context_data(*args, **kwargs)
        context.update({'is_edit': True})
        return context
    
    def get_success_url(self):
        return reverse('home')
    
 
class CouponSheetAddView(CreateView):
    form_class = CouponSheetForm
    model = Sheet
    template_name="coupons/add_coupon_sheet.html"
    
    def form_valid(self, form):
        self.object = form.save()
        coupons = form.cleaned_data['coupons']
        for coupon in coupons:
            CouponSheet.objects.create(sheet=self.object, 
                                       coupon=coupon, 
                                       count=form.cleaned_data['count_%s' % coupon.pk])
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('home')
    

class CouponSheetEditView(UpdateView):
    form_class = CouponSheetForm
    model = Sheet
    pk_url_kwarg = 'sheet_id'
    template_name = "coupons/add_coupon_sheet.html"
     
    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(CouponSheetEditView, self).get_form_kwargs(*args, **kwargs)
        form_kwargs.update({
            'coupons': self.coupons
        })
        return form_kwargs
    
    def form_valid(self, form):
        self.object = form.save()        
        for coupon in form.cleaned_data['coupons']:
            coupon_sheet, _ = CouponSheet.objects.get_or_create(sheet=self.object, 
                                                                coupon=coupon,
                                                               count = form.cleaned_data['count_%s' % coupon.pk])                
              
        for coupon_sheet in self.coupon_sheets:
            if not coupon_sheet.coupon in form.cleaned_data['coupons']:
                coupon_sheet.delete()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('home')
    
    def dispatch(self, *args, **kwargs):
        self.sheet = get_object_or_404(Sheet, pk=kwargs['sheet_id'])
        self.coupon_sheets = CouponSheet.objects.filter(sheet=self.sheet)
        self.coupons = []
        for coupon_sheet in self.coupon_sheets:
            self.coupons.append(coupon_sheet.coupon)
        
        return super(CouponSheetEditView, self).dispatch(*args, **kwargs)