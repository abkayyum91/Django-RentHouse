from django.contrib import admin
from guest.models import ContactModel, ProfilePic, AddroomModel, GuestReviewsModel
# Register your models here.

# user profile pic model
admin.site.register(ProfilePic)

# guest review  model
class GuestReviewModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience', 'pub_date')
    list_filter = ('experience', 'pub_date')
    search_fields = ['name']
admin.site.register(GuestReviewsModel, GuestReviewModelAdmin)


# Contact us model
@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject_snipet', 'query_snipet', 'date']
    list_filter = ['date']


# Customizing Admin Form For Addroom Models
class AddroomModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'for_rent', 'address', 'get_pub_date')
    list_filter = ('for_rent', 'pub_date')
    search_fields = ['name']

    fieldsets = [
        ('Uploaded By',   {'fields': ['user']}),
        ('Owner Details', {'fields': ['title', 'name', 'email', 'contact']}),
        ('Room Details',  {'fields': [ 'for_rent', 'water_supply', 'kitchen', 'washroom', 'parking_space', 'troom', 'price']}),
        ('Room Address',   {'fields': ['country', 'state', 'district', 'pincode', 'address', 'nearest_city']}),
        ('Room Description',   {'fields': ['desc']}),
        ('Room Images',   {'fields': ['rmg1', 'rmg2', 'rmg3']}),
        ('Room Agreement',   {'fields': ['agreement']}),
    ]
admin.site.register(AddroomModel, AddroomModelAdmin)