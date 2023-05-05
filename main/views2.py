from .models import *
from .forms import *
from django.contrib.auth.models import User,Group
from django.db import DatabaseError, transaction
from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
from .forms import *
from .view_logics import *
from django.shortcuts import render, get_object_or_404

context = {}


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
    

@login_required(login_url='/login/')
def adminHOme(request):
    if request.user.is_authenticated and  not request.user.is_superuser:
        current_profile = Profile.objects.get(user=request.user.id)
        context['profile_type']=current_profile
        context['startups'] = Startup.objects.exclude(profile__user=request.user.id)
        context['mentors'] = Mentor.objects.exclude(profile__user=request.user.id)
        context['iah'] = IncubatorsAccelatorsHub.objects.exclude(profile__user=request.user.id)
        context['df'] = DonorFunder.objects.exclude(profile__user=request.user.id)
        context['government'] = Goveroment.objects.exclude(profile__user=request.user.id)
        return render(request,'startup/admin/dashboard.html',context)
    else:
        logout(request)
        return HttpResponseRedirect(reverse('main:login'))

        

def loginUser(request):
    if request.method== 'POST':
        login_request = request.POST
        username = login_request.get('username')
        password = login_request.get('password')
        try:
            user = User.objects.get(username=username)
            if user:
                if user is not None and user.is_active==True:
                    authenticated_user = authenticate(request,username=username, password=password)
                    if authenticated_user is not None:
                        login(request, user)
                        context['user']=user
                        return HttpResponseRedirect(reverse('main:home'))
                elif user.is_active==False:
                    return HttpResponse('user is not active',status=403)
                else:
                    return HttpResponse('unhandled exeption',status=403)
            else:
                return HttpResponse('unregistered user',status=403)
        except Exception as e:
            user=None
            return HttpResponse('unregistered user',status=403)

        # print(user)
        # try:
            
        #     return HttpResponse('username or password incorrect',status=403)
        # except User.DoesNotExist:
        #     user = None
        
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main:home'))
        else:
            return render (request,'startup_main/login.html',context)
        
def homePage(request):
    return render (request,'startup_main/index.html',context)


def explore(request):
    return render (request,'startup/admin/explore.html',context)


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    context['startup_form']= StartupForm(instance=Startup.objects.get(profile=profile))
    context['description']= DescriptionForm(instance=Startup.objects.get(profile=profile).description)
    context['region_form']= RegionEditForm(instance = EthRegion.objects.get(pk=Wereda.objects.get(pk=Startup.objects.get(profile=profile).address.location_id).regionId.id) )
    context['wereda_form']= WeredaForm(instance=Wereda.objects.get(pk=Startup.objects.get(profile=profile).address.location_id))
    context['address']= AddressForm(instance=Startup.objects.get(profile=profile).address)
    context['user_form']= UserEditForm(instance = request.user)
    context['profile']= ProfileForm(instance = Startup.objects.get(profile=profile).profile)
    if request.method== 'POST':
        if profile == 'Government':
            pass
        if profile == 'Funder/Donor':
           pass
        if profile == 'Incubators/Accelators/Hub':
            pass
        if profile == 'Mentor':
            pass
        if profile.group.name == 'Startup':
            startup_obj = Startup.objects.get(profile=profile)
            address_obj = Address.objects.get(id=startup_obj.address.id)
            description_obj = Description.objects.get(id=startup_obj.description.id)
            location_obj = Wereda.objects.get(id=address_obj.location.id)
            profile_obj = Profile.objects.get(user=request.user)
            user_obj = User.objects.get(id=request.user.id)
            region_obj = EthRegion.objects.get(id = location_obj.regionId.id )

            region = RegionEditForm(request.POST or None,instance=region_obj,)
            startup = StartupForm(request.POST or None,instance=startup_obj, )
            description = DescriptionForm(request.POST or None,request.FILES,instance=description_obj )
            location = WeredaForm(request.POST or None, instance=location_obj )
            address = AddressForm(request.POST or None,instance=address_obj )
            user = UserEditForm(request.POST or None, instance=user_obj )
            profile = ProfileEditForm(request.POST or None, request.FILES, instance=profile_obj)
            try:
                with transaction.atomic():
                        location_obj.regionId = EthRegion.objects.get(region_name=region['region_name'].value())
                        location_obj.wereda_name = location['wereda_name'].value()
                        location_obj.save()
                        address_obj.phone_number = address['phone_number'].value()
                        address_obj.city_name = address['city_name'].value()
                        address_obj.website = address['website'].value()
                        address_obj.location = location_obj
                        address_obj.save()
                        user_obj.username = user['username'].value()
                        user_obj.email = user['email'].value()
                        user_obj.last_name = user['last_name'].value()
                        user_obj.first_name = user['first_name'].value()
                        user_obj.save()
                        profile_obj.middile_name = profile['middile_name'].value()
                        profile_obj.birth_date = profile['birth_date'].value()
                        profile_obj.profile_pic = profile['profile_pic'].value()
                        profile_obj.contact = profile['contact'].value()
                        profile_obj.gender = profile['gender'].value()
                        profile_obj.user = user_obj
                        profile_obj.save()
                        description_obj.name = description['name'].value()
                        description_obj.description = description['description'].value()
                        description_obj.sector = description['sector'].value()
                        description_obj.logo = description['logo'].value() 
                        description_obj.save()
                        startup_obj.establishment_year = startup['establishment_year'].value()
                        startup_obj.stage = startup['stage'].value()
                        startup_obj.market_scope = startup['market_scope'].value()
                        startup_obj.description = description_obj
                        startup_obj.address = address_obj
                        startup_obj.profile = profile_obj
                        startup_obj.save()
            except DatabaseError as e:
                print(e)
            profile = Profile.objects.get(user=request.user)
            context['startup_form']= StartupForm(instance=Startup.objects.get(profile=profile))
            context['description']= DescriptionForm(instance=Startup.objects.get(profile=profile).description)
            context['region_form']= RegionEditForm(instance = EthRegion.objects.get(pk=Wereda.objects.get(pk=Startup.objects.get(profile=profile).address.location_id).regionId.id) )
            context['wereda_form']= WeredaForm(instance=Wereda.objects.get(pk=Startup.objects.get(profile=profile).address.location_id))
            context['address']= AddressForm(instance=Startup.objects.get(profile=profile).address)
            context['user_form']= UserEditForm(instance = request.user)
            context['profile']= ProfileForm(instance = Startup.objects.get(profile=profile).profile)
            return render (request,'startup/admin/profile.html',context)
            

        pass
    else:
        profile = Profile.objects.get(user=request.user)
        if profile == 'Government':
            pass
        if profile == 'Funder/Donor':
           pass
        if profile == 'Incubators/Accelators/Hub':
            pass
        if profile == 'Mentor':
            pass
        if profile.group.name == 'Startup':
            
            # print(context['region_form']['region_name'].value())
        
            return render (request,'startup/admin/profile.html',context)
        
def users_list(request):
	users = Profile.objects.exclude(user=request.user)
	context = {
		'users': users
	}
	return render(request, "startup/admin/user_list.html", context)


def connect_list(request):
	p = Profile.objects.filter(user=request.user).first()
	u = p.user
	sent_friend_requests = Connect.objects.filter(from_user=request.user)
	rec_friend_requests = Connect.objects.filter(to_user=request.user)

	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
		if len(Connect.objects.filter(
			from_user=request.user).filter(to_user=p.user)) == 1:
				button_status = 'friend_request_sent'

	context = {
		'u': u,
		'button_status': button_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests
	}
	return render(request, "startup/admin/connect_list.html", context)


def cancel_friend_request(request, id):
		user = get_object_or_404(User, id=id)
		frequest = Connect.objects.filter(
			from_user=request.user,
			to_user=user).first()
		frequest.delete()
		return HttpResponseRedirect('/users')

def accept_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = Connect.objects.filter(from_user=from_user, to_user=request.user).first()
	user1 = frequest.to_user
	user2 = from_user
	user1.profile.friends.add(user2.profile)
	user2.profile.friends.add(user1.profile)
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.id))

def delete_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    print(from_user)
    frequest = Connect.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return HttpResponseRedirect('/users/{}'.format(request.user.profile.id))



def connect_list_view(request, pk=None):
	u = User.objects.get(pk=pk)
	p = u.profile
	
	sent_friend_requests = Connect.objects.filter(from_user=p.user)
	rec_friend_requests = Connect.objects.filter(to_user=p.user)

	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
		if len(Connect.objects.filter(
			from_user=request.user).filter(to_user=p.user)) == 1:
				button_status = 'friend_request_sent'

	context = {
		'u': u,
		'button_status': button_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests
	}

	return render(request, "startup/admin/connect_list.html", context)


def send_friend_request(request, id):
		user = get_object_or_404(User, id=id)
		frequest, created = Connect.objects.get_or_create(
			from_user=request.user,
			to_user=user)
		return HttpResponseRedirect('/users')


def connect(request):
    user = get_object_or_404(User, id=request.POST['connect'])
    try:
        frequest, created = Connect.objects.get_or_create(
			from_user=request.user,
			to_user=user)
    except Exception as e:
        print(e)
    return HttpResponse('users')
    # return render(request,'startup_main/startup.html', context)
def startup(request):
    if request.user.is_authenticated:
        startups = Startup.objects.exclude(profile__user=request.user.id)
        context['startups'] = startups
        filters=[]
        for field in Startup._meta.get_fields(include_parents=False):
            if isinstance(field, models.OneToOneField):
            # if field.get_internal_type()=='OneToOneField':
                
                # for related_field? in field:
                print(field)
                pass
            else:
                filters.append(field.name)
                context['filters'] = filters
        return render(request,'startup_main/startup.html', context)
    else:
        startups = Startup.objects.all()
        context['startups'] = startups
        return render(request,'startup_main/startup.html', context)

def register(request):
    if request.method== 'POST':
        context['government_form']= GovermentForm(request.POST, None)
        context['donor_form']= DonerFunderForm(request.POST, None)
        context['incubator_form']= IncubatorsAccelatorsHubForm(request.POST, None)
        context['incubator_description']= DescriptionIncubatorForm(request.POST, request.FILES)
        context['mentor_form']= MentorForm(request.POST, None)
        context['startup_form']= StartupForm(request.POST, None)
        context['description']= DescriptionForm(request.POST, request.FILES)
        context['region_form']= RegionForm(request.POST, None)
        context['wereda_form']= WeredaForm(request.POST, None)
        context['address']= AddressForm(request.POST, None)
        context['user_form']= UserForm(request.POST, None)
        context['profile']= ProfileForm(request.POST,request.FILES)        
        if request.POST['Startup'] == 'Startup':
            saveStartupObject(request,context)
        if request.POST['Startup'] == 'Mentor':
            saveMentorObject(request,context)
        if request.POST['Startup'] == 'Incubator/Hub/Acclerator':
            saveIncubatorObject(request,context)
        if request.POST['Startup'] == 'Funder/Donor':
            saveDonorObject(request,context)
        if request.POST['Startup'] == 'Government':
            saveGovernmentObject(request,context)
        return redirect ("main:homepage")
    else:
        context['mentor_form']= MentorForm()
        context['incubator_form']= IncubatorsAccelatorsHubForm()
        context['donor_form']= DonerFunderForm()
        context['goveroment_form']= GovermentForm()
        context['startup_form']= StartupForm()
        context['description']= DescriptionForm()
        context['address']= AddressForm()
        context['profile']= ProfileForm()
        context['region_form']= RegionForm()
        context['wereda_form']= WeredaForm()
        context['user_form']= UserForm()
        return render (request,'startup_main/registration.html',context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:login'))





