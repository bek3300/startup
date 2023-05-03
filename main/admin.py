from django.contrib import admin
from .models import *

# # class ZoneAdmin(admin.ModelAdmin):
# #     pass



# class ZoneInline(admin.TabularInline):
#     model = Wereda

#     # title.short_description = 'Action'
# # title.allow_tags = True


    
#     # list_display=['region_name','button'] 
    
    

@admin.register(EthRegion)
class EthRegionAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in EthRegion._meta.get_fields()]

    search_fields = ['region_name']
@admin.register(Wereda)
class EthRegionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Wereda._meta.get_fields()]
    search_fields = ['wereda_name','regionId__region_name']
@admin.register(Address)
class Addressdmin(admin.ModelAdmin):
    list_display = [field.name for field in Address._meta.get_fields()]
    search_fields = ['country','email','location__wereda_name','phoneNumber','cityName','website',]
# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     pass
#     # search_fields = [field.name for field in Profile._meta.fields]
@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    pass
@admin.register(Connect)
class ConnectAdmin(admin.ModelAdmin):
    pass
@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    pass
    # list_display = [field.name for field in Startup._meta.get_fields()]

#     search_fields = ['startupName','establishmentYear','sector','stage','marketScope','description',]
@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    pass
@admin.register(IncubatorsAccelatorsHub)
class IncubateLevelsAdmin(admin.ModelAdmin):
    pass
# @admin.register(IncubatorsAccelatorsHub)
# class IncubatorsAccelatorsHubAdmin(admin.ModelAdmin):
#     pass
@admin.register(DonorFunder)
class DonorFunderAdmin(admin.ModelAdmin):
    pass
@admin.register(Goveroment)
class GoveromentAdmin(admin.ModelAdmin):
    pass
# @admin.register(ConnectionList)
# class ConnectionListAdmin(admin.ModelAdmin):
#     pass
# @admin.register(MessageReciver)
# class MessageReciverAdmin(admin.ModelAdmin):
#     pass


from django.contrib import admin
from .models import *
# Register your models here.

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name','parent','order']
#     list_filter = ('name',)

@admin.register(Profile)
class UserProfileDataAdmin(admin.ModelAdmin):
    list_display = ['id','user_id','user','birth_date','profile_pic',]
    list_filter = ('user', 'birth_date')

# @admin.register(UserVerification)
# class UserVerificationAdmin(admin.ModelAdmin):
#     list_display = ['user','verified','hash_key']
#     list_filter = ('user',)

# @admin.register(MasterLookUp)
# class MasterLookUpAdmin(admin.ModelAdmin):
#     list_display = ['id','name','parent','code','order']
#     list_filter = ('name',)

# @admin.register(UserSubscription)
# class UserSubscriptionAdmin(admin.ModelAdmin):
#     list_display = ['user','master_data','active']
#     list_filter = ('user',)


# @admin.register(Location)
# class LocationAdmin(admin.ModelAdmin):
#     list_display = ['id','name','parent','code','order']
#     list_filter = ('name',)

# @admin.register(SocialMediaLink)
# class SocialMediaLinkAdmin(admin.ModelAdmin):
#     list_display = ['user','master_data','active','url']
#     list_filter = ('user',)

# @admin.register(UserEducation)
# class UserEducationAdmin(admin.ModelAdmin):
#     list_display = ['user','college','type_of_degree','broad_stream','certificate_course']
#     list_filter = ('user',)

# @admin.register(UserWork)
# class UserWorkAdmin(admin.ModelAdmin):
#     list_display = ['user','company','role','industry']
#     list_filter = ('user',)