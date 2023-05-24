from .models import *
from .forms import *
from django.db.models import *
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
import json
from operator import or_
from functools import reduce
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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
    
STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'Accepted'),
        (3, 'Rejected'),
    )
def getFilteredOf(objectT,request,connect):
    objectT=objectT.annotate(
             is_connected=Case(
             When(
             Exists(
             Subquery(  
             connect.filter(
                  Q(requester=OuterRef('profile__user'),responser=request.user.id) |
                     Q(responser=OuterRef('profile__user'),requester=request.user.id)
             ).values_list('status',flat=True))),
             then=connect.filter(
                  Q(requester=OuterRef('profile__user'),responser=request.user.id) |
                     Q(responser=OuterRef('profile__user'),requester=request.user.id)
             ).values_list('status',flat=True)
             ),
             default=Value(0)
             )
        )
    return objectT



@login_required(login_url='/login/')
def logged_user(request):
    if request.user.is_authenticated and  not request.user.is_superuser:
        current_profile = Profile.objects.get(user=request.user.id)
        context['profile_type']=current_profile
        context['connect'] = Connect.objects.filter(Q(responser=request.user.id) | Q(requester=request.user.id))
        context['startups'] = Startup.objects.exclude(profile__user=request.user.id)
        context['mentors'] = Mentor.objects.exclude(profile__user=request.user.id)
        context['iah'] = IncubatorsAccelatorsHub.objects.exclude(profile__user=request.user.id)
        context['df'] = DonorFunder.objects.exclude(profile__user=request.user.id)
        context['government'] = Goveroment.objects.exclude(profile__user=request.user.id)
        context['startups']= getFilteredOf(context['startups'],request,context['connect'])
        context['mentors']=  getFilteredOf(context['mentors'],request,context['connect'])
        context['iah']= getFilteredOf(context['iah'],request,context['connect'])
        context['df']=  getFilteredOf(context['df'],request,context['connect'])
        context['government']=  getFilteredOf(context['government'],request,context['connect'])
        return render (request,'logged_user/index.html',context)




def currentUserConnectUserList(request):
    user = get_object_or_404(User, id=request.POST['user'])
    context['connect'] = Connect.objects.filter(Q(responser=user.id) | Q(requester=user.id))
    context['startups'] = Startup.objects.exclude(profile__user=user.id)
    context['mentors'] = Mentor.objects.exclude(profile__user=user.id)
    context['iah'] = IncubatorsAccelatorsHub.objects.exclude(profile__user=user.id)
    context['df'] = DonorFunder.objects.exclude(profile__user=user.id)
    context['government'] = Goveroment.objects.exclude(profile__user=user.id)
    context['startups']= getFilteredOf(context['startups'],request,context['connect']).values('profile__user__username','profile__user__id')
    context['mentors']=  getFilteredOf(context['mentors'],request,context['connect']).values('profile__user__username','profile__user__id')
    context['iah']= getFilteredOf(context['iah'],request,context['connect']).values('profile__user__username','profile__user__id')
    context['df']=  getFilteredOf(context['df'],request,context['connect']).values('profile__user__username','profile__user__id')
    context['government']=  getFilteredOf(context['government'],request,context['connect']).values('profile__user__username','profile__user__id')
    
    all_connected_names = context['startups'].union(context['mentors'],context['iah'],context['df'],context['government'])
    print(list(all_connected_names))
    return JsonResponse(list(all_connected_names),safe=False)

from django.db.models import OuterRef, Subquery
def messages(request):
    messages = Messages.objects.filter(
        id__in =  Subquery(
        User.objects.filter(
            Q(sender__reciever=request.user.id) |#filters messages related to user
            Q(reciever__sender=request.user.id)
         ).distinct().annotate(
             last_msg=Subquery(
                 Messages.objects.filter(
                     Q(sender=OuterRef('id'),reciever=request.user.id) |
                     Q(reciever=OuterRef('id'),sender=request.user.id)
                 ).order_by('-timestamp')[:1].values_list('id',flat=True) 
             )
         ).values_list('last_msg', flat=True)
    )
)
   
    context['messages_sent_d'] = messages
    print(messages)
    return render(request, 'logged_user/messages.html',context)
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def message_detail(request):
    context['my_message']=Messages.objects.filter(sender=request.POST['sender']).filter(reciever=request.POST['reciver'])
    
    return render(request,'logged_user/message_detail.html',context)


def admin(request):
     return render(request, 'adminstration/index.html')

        

def loginUser(request):
    if request.method== 'POST':
        login_request = request.POST
        username = login_request.get('username')
        password = login_request.get('password')
        try:
            user = User.objects.get(username=username)
            if user:
                if user is not None and user.is_active==True and not user.is_superuser:
                    authenticated_user = authenticate(request,username=username, password=password)
                    if authenticated_user is not None:
                        logout(request)
                        login(request, user)
                        context['user']=user
                        return HttpResponseRedirect(reverse('main:home'))
                elif not user.is_superuser:
                    authenticated_user = authenticate(request,username=username, password=password)
                    if authenticated_user is not None:
                        logout(request)
                        login(request, user)
                        context['user']=user
                        return HttpResponseRedirect(reverse('main:admin'))
                     
            
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
            return render (request,'main/login.html',context)
        
def homePage(request):
    context['startup'] = Startup.objects.all()
    context['mentor'] = Mentor.objects.all()
    context['incubator'] = IncubatorsAccelatorsHub.objects.all()
    context['investor'] = DonorFunder.objects.all()
    context['government'] = Goveroment.objects.all()
    return render (request,'main/index.html',context)


def explore(request):
    if request.user.is_authenticated and  not request.user.is_superuser:
        current_profile = Profile.objects.get(user=request.user.id)
        context['profile_type']=current_profile
        context['connect'] = Connect.objects.filter(Q(responser=request.user.id) | Q(requester=request.user.id))
        context['startups'] = Startup.objects.exclude(profile__user=request.user.id)
        user = User.objects.prefetch_related('requester').prefetch_related('responser').values_list('id',flat=True)
        context['mentors'] = Mentor.objects.exclude(profile__user=request.user.id)
        context['iah'] = IncubatorsAccelatorsHub.objects.exclude(profile__user=request.user.id)
        context['df'] = DonorFunder.objects.exclude(profile__user=request.user.id)
        context['government'] = Goveroment.objects.exclude(profile__user=request.user.id)
        context['startups']= getFilteredOf(context['startups'],request,context['connect'])
        context['mentors']=  getFilteredOf(context['mentors'],request,context['connect'])
        context['iah']= getFilteredOf(context['iah'],request,context['connect'])
        context['df']=  getFilteredOf(context['df'],request,context['connect'])
        context['government']=  getFilteredOf(context['government'],request,context['connect'])
        
        
        return render (request,'logged_user/index.html',context)
    else:
        logout(request)
        return HttpResponseRedirect(reverse('main:login'))
    


@login_required(login_url='/login/')
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
            context['startup_description']= DescriptionForm(instance=Startup.objects.get(profile=profile).description)
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
	sent_friend_requests = Connect.objects.filter(requester=request.user)
	rec_friend_requests = Connect.objects.filter(responser=request.user)

	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
		if len(Connect.objects.filter(
			requester=request.user).filter(responser=p.user)) == 1:
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
			requester=request.user,
			responser=user).first()
		frequest.delete()
		return HttpResponseRedirect('/users')

def accept_friend_request(request, id):
	requester = get_object_or_404(User, id=id)
	frequest = Connect.objects.filter(requester=requester, responser=request.user).first()
	user1 = frequest.responser
	user2 = requester
	user1.profile.friends.add(user2.profile)
	user2.profile.friends.add(user1.profile)
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.id))

def delete_friend_request(request, id):
    requester = get_object_or_404(User, id=id)
    print(requester)
    frequest = Connect.objects.filter(requester=requester, responser=request.user).first()
    frequest.delete()
    return HttpResponseRedirect('/users/{}'.format(request.user.profile.id))



def connect_list_view(request, pk=None):
	u = User.objects.get(pk=pk)
	p = u.profile
	
	sent_friend_requests = Connect.objects.filter(requester=p.user)
	rec_friend_requests = Connect.objects.filter(responser=p.user)

	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
		if len(Connect.objects.filter(
			requester=request.user).filter(responser=p.user)) == 1:
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
			requester=request.user,
			responser=user)
		return HttpResponseRedirect('/users')


@login_required(login_url='/login/')
def connect(request):
    user = get_object_or_404(User, id=request.POST.get('userId'))
    print(user)
    print(request.user)
    previuosly_connected = Connect.objects.filter(Q(requester=user)).filter( Q(responser=request.user))
    print(previuosly_connected)
    if not previuosly_connected:
        try:
            frequest, created = Connect.objects.get_or_create(
                requester=request.user,
                responser=user)
            print('saved')
        except Exception as e:
            print(e)
    else:
         print('already connected')
         
         
    print(previuosly_connected)
   
    return HttpResponse('users')

def networks(request,typeOf):
    filters=[]
    if(typeOf=='startup'):
        for field in Startup._meta.get_fields(include_parents=False):
            if isinstance(field, models.OneToOneField):
                if field.name=='description':
                        for f in field.related_model._meta.get_fields(include_parents=False):
                            if( str(f.name) ==  'name' or str(f.name)=='sector'):
                                filters.append(f.verbose_name)
                if field.name=='address':
                        for f in field.related_model._meta.get_fields(include_parents=False):
                            if( str(f.name) ==  'location' ):
                                filters.append('Address')
                                        
            else:  
                if(not field.verbose_name ==  'ID'):
                    filters.append(field.verbose_name)
                    context['filters'] = filters    
        startups = Startup.objects.filter(profile__user__is_active=True).exclude(profile__user=request.user.id)
        context['startups'] = startups
        if request.user.is_authenticated:
            connectList = Connect.objects.filter(Q(responser=request.user.id)|Q(requester=request.user.id))
            context['connectList']=connectList
            return render(request,'main/startup.html', context)
        else:
            connectList = Connect.objects.exclude(responser=request.user.id,requester=request.user.id)
            startups = Startup.objects.filter(profile__user__is_active=True)
            context['startups'] = startups
            return render(request,'main/startup.html', context)
    if(typeOf=='mentor'):
        for field in Mentor._meta.get_fields(include_parents=False):
            if isinstance(field, models.OneToOneField):
                if field.name=='description':
                        for f in field.related_model._meta.get_fields(include_parents=False):
                            if( str(f.name) ==  'name' or str(f.name)=='sector'):
                                filters.append(f.verbose_name)
                if field.name=='address':
                        for f in field.related_model._meta.get_fields(include_parents=False):
                            if( str(f.name) ==  'location' ):
                                filters.append('Address')                      
            else:  
                if(not field.verbose_name ==  'ID' and not field.name == 'educational_level_other' and not field.name == 'educational_background_other' and not field.name == "mentor_area_other" and not field.name == "attachments"):
                    filters.append(field.verbose_name)
                    context['filters'] = filters  
        if request.user.is_authenticated:
            mentors = Mentor.objects.filter(profile__user__is_active=True).exclude(profile__user=request.user.id)
            context['mentors'] = mentors
            connectList = Connect.objects.filter(Q(responser=request.user.id)|Q(requester=request.user.id))
            context['connectList']=connectList
            return render(request,'main/mentor.html', context)
        else:
            connectList = Connect.objects.exclude(responser=request.user.id,requester=request.user.id)
            mentors = Mentor.objects.filter(profile__user__is_active=True)
            context['mentors'] = mentors
        return render(request,'main/mentor.html', context)
    if(typeOf=='incubator'):
        for field in IncubatorsAccelatorsHub._meta.get_fields(include_parents=False):
            if isinstance(field, models.OneToOneField):
                if field.name=='description':
                        for f in field.related_model._meta.get_fields(include_parents=False):
                            if( str(f.name) ==  'name' or str(f.name)=='sector'):
                                filters.append(f.verbose_name)
                if field.name=='address':
                        for f in field.related_model._meta.get_fields(include_parents=False):
                            if( str(f.name) ==  'location' ):
                                filters.append('Address')                      
            else:  
                if(not field.verbose_name ==  'ID' and not field.name == 'ownership_other' and not field.name == 'funded_by_other'   and not field.name == "attachments" and not field.name == "focusIndustry"):
                    filters.append(field.verbose_name)
                    context['filters'] = filters
        if request.user.is_authenticated:
            iah = IncubatorsAccelatorsHub.objects.filter(profile__user__is_active=True).exclude(profile__user=request.user.id)
            context['iah'] = iah
            connectList = Connect.objects.filter(Q(responser=request.user.id)|Q(requester=request.user.id))
            context['connectList']=connectList
            return render(request,'main/iah.html', context)
        else:
            connectList = Connect.objects.exclude(responser=request.user.id,requester=request.user.id)
            iah = IncubatorsAccelatorsHub.objects.filter(profile__user__is_active=True)
            context['iah'] = iah  
        return render(request,'main/iah.html', context)
    if(typeOf=='investor'):
        for field in DonorFunder._meta.get_fields(include_parents=False):
            if isinstance(field, models.OneToOneField):
                if field.name=='description':
                        for f in field.related_model._meta.get_fields(include_parents=False):
                            if( str(f.name) ==  'name' or str(f.name)=='sector'):
                                filters.append(f.verbose_name)
                if field.name=='address':
                        for f in field.related_model._meta.get_fields(include_parents=False):
                            if( str(f.name) ==  'location' ):
                                filters.append('Address')                      
            else:  
                if(not field.verbose_name ==  'ID' and not field.name == 'doner_type_by_other' and not field.name == 'investment_type_other' and not  field.name == "maxInvestRange"):
                    filters.append(field.verbose_name)
                    context['filters'] = filters
        if request.user.is_authenticated:
            investor = DonorFunder.objects.filter(profile__user__is_active=True).exclude(profile__user=request.user.id)
            context['investor'] = investor
            connectList = Connect.objects.filter(Q(responser=request.user.id)|Q(requester=request.user.id))
            context['connectList']=connectList
            return render(request,'main/investor.html', context)
        else:
            connectList = Connect.objects.exclude(responser=request.user.id,requester=request.user.id)
            investor = DonorFunder.objects.filter(profile__user__is_active=True)
            context['investor'] = investor  
        return render(request,'main/investor.html', context)



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
        return render (request,'main/registration.html',context)
    
# sudo kill -9 `sudo lsof -t -i:9001`
# 
def filter(request,typeOf):
    if request.method== 'POST':
        if typeOf=='startup':
            filterParams=json.loads(list(request.POST)[0])
            if filterParams:
                startup = Startup.objects.all()
                for param in filterParams:
                    if param=='market_scope':
                        if filterParams[param]:
                            startup = startup.filter(market_scope__in = filterParams[param])     
                    if param=='stage':
                        if filterParams[param]:
                            startup = startup.filter(stage__in = filterParams[param]) 
                    if param=='daterange':
                        if filterParams[param]:
                            startup =  startup.filter(establishment_year__gte=filterParams[param].split(' - ')[0],
                                        establishment_year__lte=filterParams[param].split(' - ')[1])  
                    if param=='name':
                        if filterParams[param]:
                            query = reduce(or_, (Q(description__name__startswith=item) for item in filterParams[param]))
                            startup = startup.filter(query)       
                    if param=='sector':
                        if filterParams[param]:
                            query = reduce(or_, (Q(description__sector__startswith=item) for item in filterParams[param]))
                            startup = startup.filter(query) 
                    if param == 'regionn':
                        if filterParams[param]:
                            startup = startup.filter(address__location__regionId__region_name=filterParams[param])
                    if param == 'wereda':
                        if filterParams[param]:
                            startup = startup.filter(address__location__wereda_name=filterParams[param])
                context['startups'] = startup
                return render(request,'main/startup_filters.html',context)
        if typeOf=='mentor':
            filterParams=json.loads(list(request.POST)[0])
            if filterParams:
                mentor = Mentor.objects.all()
                for param in filterParams:
                    if param=='educational_level':
                        if filterParams[param]:
                            mentor = mentor.filter(educational_level__in = filterParams[param])     
                    if param=='educational_background':
                        if filterParams[param]:
                            mentor = mentor.filter(educational_background__in = filterParams[param]) 
                    if param=='mentor_area':
                        if filterParams[param]:
                            mentor = mentor.filter(mentor_area__in = filterParams[param])
                    if param=='name':
                        if filterParams[param]:
                            query = reduce(or_, (Q(description__name__startswith=item) for item in filterParams[param]))
                            mentor = mentor.filter(query)       
                    if param=='sector':
                        if filterParams[param]:
                            query = reduce(or_, (Q(description__sector__startswith=item) for item in filterParams[param]))
                            mentor = mentor.filter(query) 
                    if param=='airelated_expriance':
                        if filterParams[param]:
                            # query = reduce(or_, (Q(description__sector__startswith=item) for item in filterParams[param]))
                            mentor = mentor.filter(airelated_expriance=not None) 
                    if param == 'regionn':
                        if filterParams[param]:
                            mentor = mentor.filter(address__location__regionId__region_name=filterParams[param])
                    if param == 'wereda':
                        if filterParams[param]:
                            mentor = mentor.filter(address__location__wereda_name=filterParams[param])
                context['mentors'] = mentor
                return render(request,'main/mentor_filters.html',context)
            
        if typeOf=='iah':
            filterParams=json.loads(list(request.POST)[0])
            if filterParams:
                iah = IncubatorsAccelatorsHub.objects.all()
                for param in filterParams:
                    if param=='service':
                        if filterParams[param]:
                            iah = iah.filter(service__in=filterParams[param])
                    if param=='ownership':
                        if filterParams[param]:
                            iah = iah.filter(ownership__in=filterParams[param]) 
                    if param=='level':
                        if filterParams[param]:
                            query = reduce(or_, (Q(level__in=item) for item in filterParams[param]))
                            iah = iah.filter(query)
                    if param=='name':
                        if filterParams[param]:
                            query = reduce(or_, (Q(description__name__startswith=item) for item in filterParams[param]))
                            iah = iah.filter(query)       
                    if param=='sector':
                        if filterParams[param]:
                            query = reduce(or_, (Q(description__sector__startswith=item) for item in filterParams[param]))
                            iah = iah.filter(query) 
                    if param=='funded_by':
                        if filterParams[param]:
                            iah = iah.filter(funded_by__in=filterParams[param]) 
                    if param=='program_duration':
                        if filterParams[param]:
                            query = reduce(or_, (Q(program_duration__in=item) for item in filterParams[param]))
                            iah = iah.filter(query) 
                    if param == 'regionn':
                        if filterParams[param]:
                            iah = iah.filter(address__location__regionId__region_name=filterParams[param])
                    if param == 'wereda':
                        if filterParams[param]:
                            iah = iah.filter(address__location__wereda_name=filterParams[param])
                context['iahs'] = iah
                return render(request,'main/iah_filters.html',context)   
        return render(request,'main/iah_filters.html',context)
             






@csrf_exempt
def getContent(request,typeOf):
    if typeOf == 'startups':
        #   print(typeOf)
          context['startups'] = Startup.objects.filter(profile__user__is_active=True).exclude(profile__user=request.user.id) if request.user.is_authenticated else Startup.objects.filter(profile__user__is_active=True)
          return  render(request,'main/startup_content.html',context)
    if typeOf == 'mentors':
          print(typeOf)
    if typeOf == 'incubators':
          print(typeOf)
    if typeOf == 'hubs':
          print(typeOf)
    if typeOf == 'acclerators':
          print(typeOf)
    if typeOf == 'doners':
          print(typeOf)
    if typeOf == 'funder':
          print(typeOf)
    if typeOf == 'government':
          print(typeOf)
    
     
    return render(request,'main/startup_filters.html',context)
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:homepage'))

