from django.contrib import admin

from coupons.models import Restriction, Inclusion, \
    Coupon, Sheet, CouponSheet


admin.site.register(Restriction)
admin.site.register(Inclusion)
admin.site.register(Coupon)
admin.site.register(Sheet)
admin.site.register(CouponSheet)