from django import template

register = template.Library()

class SheetHtmlNode(template.Node):    

    def __init__(self, sheet, coupons):    
        self.sheet = template.Variable(sheet)         
        self.coupons = template.Variable(coupons)        

    def render(self, context):
        sheet = self.sheet.resolve(context)
        coupons = self.coupons.resolve(context)
        coupon_table = {}
        idx = 0
        for coupon in coupons:
            coupon_table[idx] = coupon
            idx = idx + 1
        return sheet._get_html_table(coord_table=sheet._get_coord_table(), 
                                     coupon_table=coupon_table)
       
       
@register.tag
def sheet_html(parser, token):
    bits = list(token.split_contents())
    if len(bits) < 3:
        raise template.TemplateSyntaxError("sheet_html requires at least 2 arguments")
    
    sheet = bits[1]
    coupons = bits[2]
    return SheetHtmlNode(sheet, coupons)