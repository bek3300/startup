from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User,Group
from django.core.exceptions import ValidationError
from .modelVariables import *
from multiselectfield import MultiSelectField
from django.contrib.postgres.fields import ArrayField

class EthRegion(models.Model):
     region_name = models.CharField(
         verbose_name = 'Region',
        max_length=50,
        choices=Regions,
        blank=False,
        null=False,
        unique=True)
     

     def __str__(self):
        return self.region_name
      
class Wereda(models.Model):
    regionId = models.ForeignKey(EthRegion,blank=False,null=False,on_delete=models.CASCADE,verbose_name='Region',default=1,related_name='wereda')
    wereda_name = models.CharField(max_length=30, 
                                   verbose_name = 'Wereda',
                                   blank=False,null=False)
    def __str__(self):
        return self.wereda_name


class Address(models.Model):
    country = models.CharField(
        verbose_name = 'Country',
        max_length=30,null=False, blank=False)
    location = models.OneToOneField(Wereda,
                                    verbose_name = 'Wereda',
                                    on_delete=models.DO_NOTHING,null=False, blank=False,default=1,related_name='location')
    phone_number = models.IntegerField(
        verbose_name = 'Phone Number',
        null=False, blank=False)
    city_name = models.CharField(
        verbose_name = 'City Name',
        max_length=30, blank=False,null=False)
    website = models.CharField(
        verbose_name = 'Website',
        max_length=30,null=False, blank=False)
    def __str__(self):
        return self.location.wereda_name
    

def validate_image(image):
    file_size = image.file.size
    limit = 2
    if file_size > limit * 1024 *1024:
        raise ValidationError("Max size of file is %s MB" % limit)

GENDER = ((0,'Male'),(1,'Female'))
class Profile(models.Model):
    middile_name         = models.CharField(
        verbose_name = 'Middile Name',
        max_length =15, null=False, blank=False)
    user            = models.OneToOneField(
        User,on_delete=models.CASCADE)
    birth_date      = models.DateField(verbose_name = 'Birth Date',null=False, blank=False)
    profile_pic     = models.ImageField(verbose_name = 'Profile Picture',upload_to='user_pic/%Y/%m/%d', blank=False, null=False, validators=[validate_image]) 
    contact         = models.CharField(verbose_name = 'Contact',max_length =15, null=False, blank=False)
    secondary_email = models.EmailField(verbose_name = 'Alternate Email',max_length=150,null=False, blank=False)
    gender          = models.IntegerField(verbose_name = 'Sex/Gender',default=0,choices=GENDER)
    friends = models.ManyToManyField("Profile", blank=True)
    modified        = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING,blank=True,null=True)
    def __str__(self):
        return str(self.user.email)  
    def get_absolute_url(self):
    	return "/users/{}".format(self.user.id)  
    

class Description(models.Model):
    name = models.CharField(verbose_name = 'Name',max_length=30,blank=False,null=False)
    description = models.TextField(verbose_name = 'Description',max_length=1000,blank=False,null=False)
    sector = models.CharField(
        verbose_name = 'Sector',
        max_length=50,
        choices=SECTORS,
        blank=False,
        null=False,
        )
    other_sector = models.CharField(
        
        max_length=30,
        blank=True,null=True
    )
    logo = models.ImageField(upload_to='logo/startup',blank=True,null=True)
    def __str__(self):
        return self.name

class Startup(models.Model):
    establishment_year = models.DateField(verbose_name="Establishment Year", blank=False,null=False)
    market_scope = models.CharField(
        verbose_name = 'Market Scope',
        max_length=50,
        choices=MARKET_SCOPE,
        blank=False,
        null=False,
        )
    stage = models.CharField(
        verbose_name = 'Stage',
        max_length=50,
        choices=STAGE,
        blank=False,
        null=False
        )
    description = models.OneToOneField(Description, on_delete=models.DO_NOTHING,blank=False,null=False,related_name='startup_description')
    address = models.OneToOneField(Address, on_delete=models.DO_NOTHING,blank=False,null=False,related_name='startup_address')
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,blank=False,null=False,related_name='startup_profile')
    def __str__(self):
        return self.description.name.__str__()
    def get_absolute_url(self):
    	return "/startup/{}".format(self.description.name)
    

class Mentor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE,blank=False,null=False)
    address = models.OneToOneField(Address, on_delete=models.DO_NOTHING,blank=False,null=False,related_name='mentor_address')
    educational_level = models.CharField(
        verbose_name = 'Educational Level',
        choices=EDUCATIONAL_LEVEL,
        max_length=50,blank=False,null=False)
    educational_level_other = models.CharField(
        verbose_name = 'Specify Other Level',
        max_length=50,blank=True,null=True)
    educational_background = models.CharField(
        verbose_name = 'Educational Background',
        choices=EDUCATIONAL_BACKGROUND,
        max_length=50,blank=False,null=False)
    educational_background_other = models.CharField(
        verbose_name = 'Specify Other Background',
        max_length=50,blank=True,null=True)
    mentor_area = models.CharField(
        verbose_name = 'Mentor Area',
        choices=MENTORSHIP_AREA,
        max_length=50,blank=False,null=False)
    mentor_area_other = models.CharField(
        verbose_name = 'Specify Other Area',
        max_length=50,blank=True,null=True)
    airelated_expriance = models.CharField(
        verbose_name = 'AI Related Experience',
        max_length=50,blank=False,null=False)
    attachments = models.FileField(
        verbose_name = 'Attachment',
        upload_to='mentor/attachments',blank=True,null=True, help_text="please upload relevant documents max 10")
    description = models.OneToOneField(Description, on_delete=models.DO_NOTHING,blank=False,null=False,related_name='mentor_description')

    def __str__(self):
        return self.description.name.__str__()


class IncubatorsAccelatorsHub(models.Model):
    address = models.OneToOneField(Address, on_delete=models.DO_NOTHING,blank=False,null=False,related_name='iha_address')
    service = models.CharField(
        verbose_name = 'Service',
        max_length=50,
        choices=SERVICE_TYPE,
        blank=False,null=False
    )
    ownership = models.CharField(
        verbose_name = 'Owner Ship',
        max_length=50,
        choices=OWNERSHIP,
        blank=False,null=False
    )
    ownership_other = models.CharField(
        max_length=50,
        blank=True,null=True
    )
    description = models.OneToOneField(Description, on_delete=models.DO_NOTHING,blank=False,null=False,related_name='iha_description')
    
    focusIndustry = ArrayField(models.CharField(
        # choices=SECTORS,
        max_length=500),default=list
        )
    

    level = ArrayField(models.CharField(
        max_length=500,
        # choices=STARTUP_STAGE,
        # read_only=False,
    ),size=20,default=list)
    funded_by = models.CharField(
        verbose_name = 'Funded By',
        max_length=50,
        choices=FUNDEDBY,
        blank=False,null=False
    )
    funded_by_other = models.CharField(max_length=50,blank=False,null=False)
    program_duration = models.CharField(
        verbose_name = 'Program Duration',
        max_length=50,
        choices=PROGRAM_DURATION,
        blank=True,null=True
    )
    attachments = models.FileField(upload_to='incubetor/attachments',blank=True,null=True,help_text="please upload relevant documents max 10")
    profile = models.OneToOneField(Profile, on_delete=models.DO_NOTHING,blank=False,null=False,related_name='iha_address')
    def __str__(self):
        return self.description.name.__str__()


class DonorFunder(models.Model):
    doner_type = models.CharField(
        verbose_name = 'Donor Type',
        max_length=50,
        choices=FUNDEDBY,
        blank=False,null=False
    )
    doner_type_by_other = models.CharField(
        max_length=50,blank=True,null=True)
    address = models.OneToOneField(Address, on_delete=models.DO_NOTHING,blank=False,null=False,related_name='donor_address')
    level = ArrayField(models.CharField(
        max_length=500,
        # choices=STARTUP_STAGE,
        # read_only=False,
    ),size=20,default=list)
    investment_type = models.CharField(
        verbose_name = 'Investment Type',
        max_length=50,
        choices=INVESTMENT_TYPE,
        blank=False,null=False
    )
    investment_type_other = models.CharField(max_length=50,blank=True,null=True)
    profile = models.OneToOneField(Profile, on_delete=models.DO_NOTHING,blank=False,null=False,related_name='donor_profile')
    description = models.OneToOneField(Description, on_delete=models.DO_NOTHING,blank=False,null=False,related_name='donor_description')
    maxInvestRange = models.CharField(verbose_name = 'Investment Range',
                                      max_length=100,blank=True,null=True)
    def __str__(self):
        return self.description.name.__str__()

class Goveroment(models.Model):
    address = models.OneToOneField(Address, on_delete=models.DO_NOTHING,blank=False,null=False,related_name='goveroment_address')
    goveroment_type = models.CharField(
        verbose_name = 'Government type',
        max_length=50,
        choices=GOVEROMENT_TYPE,
        blank=False,null=False
    )
    goveroment_type_other = models.CharField(
        max_length=50,blank=False,null=False)
    level = ArrayField(models.CharField(
        max_length=500,
        # choices=STARTUP_STAGE,
        # read_only=False,
    ),size=20,default=list)
    
    description = models.OneToOneField(Description, on_delete=models.DO_NOTHING,blank=False,null=False,related_name='goveroment_description')
    profile = models.OneToOneField(Profile, on_delete=models.DO_NOTHING,blank=False,null=False)
    def __str__(self):
        return self.description.name

class Connect(models.Model):
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE,)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE,)
    timestamp = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'Accepted'),
        (3, 'Rejected'),
    )
    # store this as an integer, Django handles the verbose choice options
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)
    @staticmethod
    def connects(user):
        connects = []
        for _ in Connect.objects.filter(to_user=user, status=1):
            connects.append({"username": _.friend.username, "gravatar": _.friend.avatar})
        for _ in Connect.objects.filter(friend=user, status=1):
            connects.append({"username": _.user.username, "gravatar": _.user.avatar})

        return connects

    @staticmethod
    def pending_requests(user):
        requests = []
        for _ in Connect.objects.filter(friend=user, status=0):
            requests.append({"username": _.user.username, "gravatar": _.user.avatar})

        return requests
