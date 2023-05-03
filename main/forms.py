

from django.forms import *
from .models import *
from django import forms
from urllib.request import urlopen
import json
from django.contrib.auth.models import User,Group
from crispy_forms.helper import FormHelper,Layout
# from crispy_forms import FormHelper, Layout

from crispy_forms.layout import Layout, Submit, Row, Column

class DateInput(forms.DateInput):
    input_type = 'date'

class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email','last_name','first_name']
        help_texts = {
            'username': None,
        }
        # exclude = ('username',)

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email','last_name','first_name','password']
        # exclude = ('username',)






class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['middile_name','birth_date','profile_pic','contact','secondary_email','gender']
        widgets = {
            'birth_date': DateInput()
        }

class ProfileEditForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['middile_name','birth_date','profile_pic','contact','secondary_email','gender']
        widgets = {
            'birth_date': DateInput()
        }
    # def __init__(self, *args, **kwargs):
    #     super(ProfileForm, self).__init__(*args, **kwargs)
    #     self.fields['group'].required = False
Regions = [
        ('' ,'Please Select Region'),
        (adissAbeba, 'Addis Ababa'),
        (afar, 'Afar'),
        (amhara, 'Amhara'),
        (benishangulgumuz, 'Benishangul-Gumuz'),
        (diredawa, 'Dire Dawa'),
        (gambela, 'Gambela'),
        (harari, 'Harari'),
        (oromia, 'Oromia'),
        (somali, 'Somali'),
        (sidama, 'Sidama '),
        (southwest, 'South West'),
        (snnp, 'SNNP'),
        (tigray, 'Tigray'),
        
    ]

class RegionForm(forms.Form):
    region_name=forms.ChoiceField(choices = Regions)
    def clean_region_name(self):
        name = self.cleaned_data['region_name']
        if name =="Please Select Region":
            raise forms.ValidationError('Invalid Region Name.')

        return name

class RegionEditForm(ModelForm):
    class Meta:
        model = EthRegion
        fields = ('region_name',)
        # exclude = ('region_name',)
    # region_name=forms.ChoiceField(choices = Regions)

    # def __init__(self, *args, **kwargs):
    #     super(RegionEditForm, self).__init__(*args, **kwargs)
    #     print(self.instance)

  
    

def getGeoserverData():
    url = "http://localhost:8088/geoserver/elri/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=elri%3AETH_adm2&maxFeatures=5000&outputFormat=application%2Fjson"
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json
class WeredaForm(ModelForm):
    class Meta:
        model = Wereda
        # fields = ['wereda_name']
        exclude=('wereda_name',)
    def clean_wereda_name(self):
        return None

    def __init__(self, *args, **kwargs):
        super(WeredaForm, self).__init__(*args, **kwargs)
        result_obj = self.instance
        if result_obj:   # Checks if result_obj is None or not
            self.fields['wereda_name'] = forms.ChoiceField()
            self.fields['wereda_name'].required=False 

class WeredaEditForm(ModelForm):
    class Meta:
        model = Wereda
        fields = ['wereda_name']
        
    def __init__(self, *args, **kwargs):
        super(WeredaEditForm, self).__init__(*args, **kwargs)
        result_obj = self.instance
        if result_obj:   # Checks if result_obj is None or not
            # print(result_obj.regionId)
            self.fields['wereda_name'] = forms.ChoiceField(choices = tuple((e,j) for e,j in [(d['properties']['NAME_2'],d['properties']['NAME_2']) for d in getGeoserverData().get('features') if d['properties']['NAME_1'] in [str(result_obj.regionId)] ]))
       
class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['phone_number','city_name','website'] 

       
class DescriptionForm(ModelForm):
    class Meta:
        model = Description
        fields = ['name','description','sector','logo'] 
        widgets = {
        'description': forms.Textarea(attrs={'rows':5, 'cols':40}),            # 'roll': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     print(self)
    #     self.fields['sector'].widget.attrs['onclick'] = 'alert("Hello, world!")';
 



class StartupForm(ModelForm):
    class Meta:
        model = Startup
        fields = ['establishment_year', 'stage', 'market_scope' ]
        widgets = {
            'establishment_year': DateInput()
        }
  

class MentorForm(ModelForm):
   
    class Meta:
        model = Mentor
        fields = ['educational_level','educational_level_other', 
                  'educational_background','educational_background_other',
                   'mentor_area','mentor_area_other','airelated_expriance',
                   'attachments' ]
       
    
class IncubatorsAccelatorsHubForm(ModelForm):
    level = forms.MultipleChoiceField(
        widget=forms.SelectMultiple(multiple=False),
        choices=[('red', 'Red'), ('blue', 'Blue'), ('green', 'Green')]
    )
    class Meta:
        model = IncubatorsAccelatorsHub
        fields = ['service', 'ownership', 'focusIndustry','level','funded_by','program_duration','attachments' ]
    
class DonerFunderForm(ModelForm):
   
    class Meta:
        model = DonorFunder
        fields = ['doner_type', 'doner_type_by_other', 'level','investment_type','investment_type_other','maxInvestRange' ]
       
    

class GovermentForm(ModelForm):
   
    class Meta:
        model = Goveroment
        fields = ['goveroment_type', 'level' ]
       
    