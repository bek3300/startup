from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from django.db import DatabaseError, transaction
from .models import *
from django.contrib.auth.models import Group,User
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import *
from django.shortcuts import get_object_or_404
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse(loginUser))


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'startup/admins/profile.html', {
        'form': form
    })


@login_required(login_url='/login/')
def profile(request):
    startup_instance = Startup.objects.get(profile__user=str(request.user.id))
    startup_form = StartupForm(request.POST or None, request.FILES or None, instance=startup_instance)
    address_instance = Address.objects.get(pk=str(startup_instance.address.id))
    wereda_instance = Wereda.objects.get(pk=str(address_instance.location.id))
    region_instance = EthRegion.objects.get(pk=str(wereda_instance.regionId.id))
    profile_instance = Profile.objects.get(pk=str(startup_instance.profile.pk))
    user_instance = User.objects.get(pk=str(profile_instance.user.pk))
    adress_object = AddressForm(request.POST or None, instance=address_instance)
    wereda_object = WeredaEditForm(request.POST or None, instance=wereda_instance)
    region_object = RegionForm(request.POST or None, instance=region_instance)
    profile_object = ProfileForm(request.POST or None, instance=profile_instance)
    user_object = UserForm(request.POST or None, instance=user_instance)
    password_form = PasswordChangeForm(request.user)

    
    def getGeoserverData():
        url = "http://localhost:8080/geoserver/Startup/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=Startup%3AETH_adm2&maxFeatures=1000&outputFormat=application%2Fjson"
        response = urlopen(url)
        data_json = json.loads(response.read())
        return data_json

    if request.method== 'POST':
        startup_obj = Startup.objects.get(id=request.POST.get('pk'))
        address = Address.objects.get(id=startup_obj.address.id)
        location = Wereda.objects.get(id=address.location.id)
        region = EthRegion.objects.get(id=location.regionId.id)
        profile_type = get_object_or_404(Group,pk=request.POST.get('group'))
        if(str(profile_type)=='Startups'):
            try:
                with transaction.atomic():
                    startup_obj.startupName= request.POST.get('startupName')
                    startup_obj.address=address
                    region_instance_obj = EthRegion.objects.get(region_name=str([d['properties']['NAME_1'] for d in getGeoserverData().get('features') if d['properties']['NAME_2']==request.POST.get('wereda_name')][0]))
                    location.wereda_name = request.POST.get('wereda_name')
                    location.regionId = region_instance_obj
                    location.save()
                    address.location = location
                    address.save()
                    startup_obj.establishmentYear= request.POST.get('establishmentYear')
                    startup_obj.sector= request.POST.get('sector')
                    startup_obj.stage= request.POST.get('stage')
                    startup_obj.description= request.POST.get('description')
                    # print(request.FILES.get('logo'))
                 
                    startup_obj.logo= request.FILES.get('logo')
                    startup_obj.save()
            except DatabaseError as e:
                print(e)
        startup_instance = Startup.objects.get(profile__user=str(request.user.id))
        startup_form = StartupForm(request.POST , request.FILES, instance=startup_instance)
        context['adress_form']=adress_object
        context['wereda_form']=wereda_object
        context['region_form']=region_object
        context['profile_form']=profile_object
        context['user_form']=user_object
        context['startup_form']=startup_form
        context['password_form']=password_form
        return render(request,'startup/admins/profile.html',context)
    else:
        context['adress_form']=adress_object
        context['wereda_form']=wereda_object
        context['region_form']=region_object
        context['profile_form']=profile_object
        context['user_form']=user_object
        context['startup_form']=startup_form
        context['password_form']=password_form
        return render(request,'startup/admins/profile.html',context)
    


context = {}
@login_required(login_url='/login/')
def adminHOme(request):
        current_profile = Profile.objects.get(user=request.user.id)
        context['profile_type']=current_profile.group
        context['startups'] = Startup.objects.exclude(profile__user=request.user.id)
        context['mentors'] = Mentor.objects.exclude(profile__user=request.user.id)
        context['iah'] = IncubatorsAccelatorsHub.objects.exclude(profile__user=request.user.id)
        context['df'] = DonorFunder.objects.exclude(profile__user=request.user.id)
        context['government'] = Goveroment.objects.exclude(profile__user=request.user.id)
        return render(request,'startup/admins/admin.html',context)

def loginUser(request):
    if request.methoregisterd== 'POST':
        login_request = request.POST
        username = login_request.get('username')
        password = login_request.get('password')
        user = User.objects.get(username=username)
        try:
            if user:
                if user is not None and user.is_active==True:
                    authenticated_user = authenticate(request,username=username, password=password)
                    if authenticated_user is not None:
                        login(request, user)
                        context['user']=user
                        return HttpResponseRedirect(reverse(adminHOme)+'?profile_type='+checkProfileType(user))
                elif user.is_active==False:
                    return HttpResponse('user is not active',status=403)
                else:
                    return HttpResponse('unhandled exeption',status=403)
            else:
                return HttpResponse('unregistered user',status=403)
            return HttpResponse('username or password incorrect',status=403)
        except User.DoesNotExist:
            user = None
        
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse(adminHOme))
        else:
            return render (request,'startup/login.html',context)


def homePage(request):
    return render (request,'main/index.html',context)

def networkStartups(request):
    return render (request,'startup/network.html',context)


def activePartner(request):
    return render (request,'startup/user.html',context)


def register(request):
    return render (request,'startup_main/registration.html',context)

def checkProfileType(user):
    print(len(Startup.objects.filter(profile__user=user.id)))
    if len(Startup.objects.filter(profile__user=user.id))>=1:
        return 'Startup'
    if len(Mentor.objects.filter(profile__user=user.id))>=1:
        return 'Mentor'
    if len(IncubatorsAccelatorsHub.objects.filter(profile__user=user.id))>=1:
        return 'Incubators/Accelators/Hub'
    if len(DonorFunder.objects.filter(profile__user=user.id))>=1:
        return 'Donor/Funder'
    if len(Goveroment.objects.filter(profile__user=user.id))>=1:
        return 'Goveroment'
    
    




@transaction.atomic
def registerUsers(request):
    if request.method == 'POST':
        if request.POST.get('profile_type')=='startup':
            startup_form =request.POST
            sname = startup_form.get('mystartup')
            sex = startup_form.get('sex')
            description = startup_form.get('description')
            region = startup_form.get('region')
            wereda = startup_form.get('wereda')
            phone_number = startup_form.get('phone_number')
            city = startup_form.get('city')
            website = startup_form.get('website')
            establishment = startup_form.get('datepicker')
            sector = startup_form.get('sector')
            others = startup_form.get('others')
            stage  = startup_form.get('stage')
            market = startup_form.get('market')
            logo = request.FILES.get('logo')
            startup_fname = startup_form.get('startup_fname')
            startup_mname = startup_form.get('startup_mname')
            startup_lname = startup_form.get('startup_lname')
            startup_email = startup_form.get('startup_email')
            startup_password = startup_form.get('startup_password')
            startup_contact = startup_form.get('startup_contact')
            startup_profile = request.FILES.get('startup_profile')
            try:
                with transaction.atomic():
                      region = EthRegion.objects.get(region_name=region)
                      region.save()
                      wereda_ = Wereda(regionId=region,wereda_name=wereda)
                      wereda_.save()
                      adress = Address(
                          country='Ethiopia',
                          email=startup_email,
                          location=wereda_,
                          phoneNumber=phone_number,
                          cityName = city,
                          website = website
                          )
                      adress.save()
                      user=User.objects.create_user(username=startup_email,
                                 email=startup_email,
                                 password=startup_password,
                                 is_active = False,
                                 first_name = startup_fname,
                                 last_name = startup_lname
                                 )
                      user.save()   
                      startup_group = Group.objects.get(name='Startups')    
                   
                      profile = Profile(user = user,
                                         middile_name = startup_mname,
                                         profile_pic = startup_profile,
                                         sex=sex,
                                         group =startup_group,
                                         contact = startup_contact
                                         
                                         )
                      profile.save()
                      startup = Startup(startupName=sname,
                                        address=adress,
                                        establishmentYear=establishment,
                                        sector=sector,
                                        stage=stage,
                                        marketScope=market,
                                        description = description,
                                        logo=logo,
                                        profile=profile
                                        )
                      startup.save()
            except DatabaseError as e:
                print(e)
            return render(request,'startup/signup.html',context)
    # form = SignUpForm()
    return render(request, 'startup/signup.html', context)


