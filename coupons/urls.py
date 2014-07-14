from django.conf.urls import patterns, url
from coupons.views import SheetListView, SheetDetailView, CouponAddView,\
    CouponEditView, CouponSheetAddView, CouponSheetEditView, CouponDetailView


urlpatterns = patterns('',
    url(regex=r'^$', 
           view='coupons.views.home', name='home'),
        
    url(r'^sheet/list/$', 
        SheetListView.as_view() , name='sheet_list'),
    url(r'^sheet/(?P<sheet_id>\d+)/$', 
        SheetDetailView.as_view(), name='sheet_detail'),        
#         url(regex=r'^sheet/(?P<sheet_id>\d+)/pdf/$', 
#            view='pdf_view', name='pdf_view'),
#            
    url('^sheet/add/$',
        CouponSheetAddView.as_view(), name='coupon_sheet_add'),
    url(r'^sheet/(?P<sheet_id>\d+)/edit/$',
        CouponSheetEditView.as_view(), name='coupon_sheet_edit'),
           
    url(r'^coupon/add/$',
        CouponAddView.as_view(), name='coupon_add'),
    url(r'^coupon/(?P<coupon_id>\d+)/$', 
        CouponDetailView.as_view(), name='coupon_detail'),
    url(r'^coupon/(?P<coupon_id>\d+)/edit/$', 
        CouponEditView.as_view(), name='coupon_edit'),

)

