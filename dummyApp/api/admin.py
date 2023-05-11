from django.contrib import admin
from .models import SteelDesign, FinPlateDesign,FinPlateDesignReport, Drawing

# Register your models here.
admin.site.register(SteelDesign)
admin.site.register(FinPlateDesign)
admin.site.register(FinPlateDesignReport)
admin.site.register(Drawing)