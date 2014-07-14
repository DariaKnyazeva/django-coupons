from django.db import models
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template.context import Context


UPLOAD_DIR = 'coupons/%Y/%m/%d'


class Restriction(models.Model):
    name = models.CharField(max_length=250)
    
    def __unicode__(self):
        return self.name
    

class Inclusion(models.Model):
    name = models.CharField(max_length=250)
    
    def __unicode__(self):
        return self.name

   
class Coupon(models.Model):
    heading = models.CharField(max_length=250)
    details = models.TextField()
    footer = models.CharField(max_length=250)
    rank = models.IntegerField()    
    image = models.ImageField(upload_to=UPLOAD_DIR, blank=True)
    restrictions = models.ManyToManyField(Restriction, blank=True)
    inclusions = models.ManyToManyField(Inclusion, blank=True)
    
    is_printed = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.heading
    
    def as_html(self, for_pdf=False):
        template = get_template("coupons/_coupon_detail.html")
        context = Context({'object':self,
                           'for_pdf':for_pdf,})
        return template.render(context)
    
    def get_absolute_url(self):
        return reverse('coupon_detail', kwards={'coupon_id': self.pk})        


class Sheet(models.Model):
    heading = models.CharField(max_length=250)
    cols = models.IntegerField()
    rows = models.IntegerField()
    coupons = models.ManyToManyField(Coupon, through='CouponSheet')
    
    def __unicode__(self):
        return self.heading    
    
    def get_all_coupons(self):
        """
        Returns list of coupons, repeated by their "count" parameter.
        """
        coupon_sheets = CouponSheet.objects.filter(sheet=self)
        
        result = []
        for coupon_sheet in coupon_sheets:                
            for _idx in range(coupon_sheet.count):                
                result.append(coupon_sheet.coupon)
                
        return result
    
    def _get_coord_table(self):
        """
        Returns a dictionary, which index keys correspond to (row, col) in the row x col table.
        """
        coord_table = {}
        idx = 0       
        for row in range(self.rows):            
            for col in range(self.cols):
                coord_table['%s:%s' % (row, col)] = idx
                idx = idx + 1
        return coord_table

    def _get_html_table(self, coord_table, coupon_table, for_pdf=False):
        result = "<table>"        
        for row in range(self.rows):      
            result = "%s<tr>" % result  
            coupon_row = ""    
            for col in range(self.cols):                  
                idx = coord_table['%s:%s' % (row, col)]
                if idx in coupon_table:
                    coupon = coupon_table[idx]
                    coupon_row = "%s<td>%s</td>" % (coupon_row, coupon.as_html(for_pdf))                                                     
            result = "%s%s</tr><tr><td>&nbsp;</td></tr>" % (result, coupon_row)        
        result = "%s</table>" % result
                
        return result
    
    def as_html(self):        
        html = """
        <head> 
        <link rel="stylesheet" type="text/css" href="/media/css/reset.css" />
        <link rel="stylesheet" type="text/css" href="/media/css/text.css" />
        <link rel="stylesheet" type="text/css" href="/media/css/960.css" />
        <link rel="stylesheet" type="text/css" href="/media/css/style.css" />
        <style>
            table tr td {
                padding: 5px;
            }
        </style>             
        </head>            
        <body>            
        <h1 id="headerContent">%s</h1>
        """   % self.heading
        html_table = ""  
    
        coord_table = self._get_coord_table()        
        paginator = Paginator(self.get_all_coupons(), len(coord_table))
    
        for page_num in paginator.page_range:
            coupons = paginator.page(page_num).object_list
            coupon_table = {}
            idx = 0
            for coupon in coupons:
                coupon_table[idx] = coupon
                idx = idx + 1
            html_table = """%s%s<div id='footerContent'>Page <pdf:pagenumber/>
                          </div><pdf:nextpage/>""" % \
                        (html_table, 
                         self._get_html_table(self._get_coord_table(), coupon_table, for_pdf=True))            
        html = "%s%s</body>" % (html, html_table)        
        return html    
    
    def get_absolute_url(self):
        return reverse('sheet_detail', kwargs={'sheet_id': self.pk})        

    
class CouponSheet(models.Model):
    count = models.IntegerField(help_text="The number of times to print the same coupon in the sheet.")
    coupon = models.ForeignKey(Coupon)
    sheet = models.ForeignKey(Sheet)
    
    def __unicode__(self):
        return "CouponSheet for %s coupon, %s sheet" % (self.coupon, self.sheet)
    
    
