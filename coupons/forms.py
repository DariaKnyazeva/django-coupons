from django import forms
from coupons.models import Coupon, Sheet, CouponSheet


class CouponSheetForm(forms.ModelForm):
    coupons = forms.ModelMultipleChoiceField(queryset=Coupon.objects.all(),
                                             widget=forms.CheckboxSelectMultiple)
    
    def __init__(self, coupons=None, *args, **kwargs):
        super(CouponSheetForm, self).__init__(*args, **kwargs)
        self.fields['coupons'].initial = coupons
        
        for coupon in Coupon.objects.all():
            label = "Count of % s" % coupon
            self.fields['count_%s' % coupon.pk] = forms.IntegerField(label=label,
                                                                     required=False)
        if self.instance and coupons:
            for coupon in coupons:
                try:
                    coupon_sheet = CouponSheet.objects.get(sheet=self.instance, coupon=coupon)
                    self.fields['count_%s' % coupon.pk].initial = coupon_sheet.count
                except CouponSheet.DoesNotExist:
                    pass
                            
    def clean_coupons(self):
        coupons = self.cleaned_data['coupons']
        for coupon in coupons:
            if not self.data.get('count_%s' % coupon.pk):
                raise forms.ValidationError("Please, specify count of the coupon %s." % coupon)
        return coupons
    
    class Meta:
        model = Sheet       
        exclude = ('coupons',) 
        
        
class CouponForm(forms.ModelForm):
    #image = forms.ImageField()
    
    def __init__(self, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)
        #if self.instance.pk:
        #    image = self.instance.image
        #    if image:
        #        self.fields['image'].initial = image.path
    
    class Meta:
        model = Coupon
        exclude = ('is_printed',)