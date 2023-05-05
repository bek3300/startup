from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import *
from .forms import *
from django.contrib.auth.models import User,Group
from django.db import DatabaseError, transaction
from .models import *
from django.shortcuts import render,redirect
from .forms import *

def saveWereda(context):
    region= EthRegion.objects.get(region_name=context['region_form'].cleaned_data['region_name'])
    wereda = Wereda(wereda_name=context['wereda_form'].data['wereda_name'], regionId=region)
    wereda.save()
    return wereda

def saveDescription(request,description_instance):
    def checkSector():
        if description_instance['sector'] == 'Other':
            return request.POST['other__sector']
        else:
            return ''
    description = Description(name=description_instance['name'],
                              description=description_instance['description'],
                              sector=description_instance['sector'],
                              logo=description_instance['logo'],
                              other_sector=checkSector(),)
    description.save()
    return description
def saveIncubatorDescription(request,incubator_description_instance):
    description = Description(name=incubator_description_instance['name'],
                              description=incubator_description_instance['description'],
                              sector='Other',
                              logo=incubator_description_instance['logo'],
                              other_sector='no',)
    description.save()
    return description
def saveAddress(request,address_instance,context):
    address= Address(
         country='Ethiopia',
         location=saveWereda(context),
         phone_number=address_instance['phone_number'],
         city_name=address_instance['city_name'],
         website=address_instance['website'],
         )
    address.save()
    return address

def saveUser(user_instance):
    usero=User(username=user_instance['username'],
                email=user_instance['email'],
                is_active = False,
                first_name = user_instance['first_name'],
                last_name = user_instance['last_name']
                )
    usero.set_password(user_instance['password'])
    usero.save()
    return usero

def saveProfile(user_instance,profile_instance,group):
    profile= Profile(
         middile_name=profile_instance['middile_name'],
         birth_date=profile_instance['birth_date'],
         user=saveUser(user_instance),
         profile_pic=profile_instance['profile_pic'],
         contact=profile_instance['contact'],
         secondary_email=profile_instance['secondary_email'],
         gender=profile_instance['gender'],
         group=group
         )
    profile.save()
    return profile


def saveDonor(donor_instance,
              request,
                                   description_instance,
                                   address_instance,
                                   user_instance,
                                   profile_instance,
                                   group,context):
    def checkDonor():
        if donor_instance['doner_type'] == 'Other':
            return request.POST['other__doner_type']
        else:
            return ''
    def checkInvestment():
        if donor_instance['investment_type'] == 'Other':
            return request.POST['other__investment_type']
        else:
            return ''
    donor = DonorFunder(
         doner_type=donor_instance['doner_type'],
        doner_type_by_other=checkDonor(),
        level=donor_instance['level'],
        investment_type=donor_instance['investment_type'],
        investment_type_other=checkInvestment(),
        maxInvestRange=donor_instance['maxInvestRange'],
        description=saveDescription(request,description_instance),
        address=saveAddress(request,address_instance,context),
        profile=saveProfile(user_instance,profile_instance,group)
        )
    donor.save()
    return donor


def saveStartup(startup_instance,
                request,
                description_instance,
                address_instance,
                user_instance,profile_instance,group,context):
    startup = Startup(establishment_year=startup_instance['establishment_year'],
        market_scope=startup_instance['market_scope'],
        stage=startup_instance['stage'],
        description=saveDescription(request,description_instance),
        address=saveAddress(request,address_instance,context),
        profile=saveProfile(user_instance,profile_instance,group)
        )
    startup.save()
    return startup

def saveGovernment(government_instance,
                request,
                description_instance,
                address_instance,
                user_instance,profile_instance,group,context):
    def checkInvestment():
        if government_instance['goveroment_type'] == 'Other':
            return request.POST['other__goveroment_type']
        else:
            return ''
    government = Goveroment(
         goveroment_type=government_instance['goveroment_type'],
        goveroment_type_other=checkInvestment(),
        level=government_instance['level'],
        description=saveDescription(request,description_instance),
        address=saveAddress(request,address_instance,context),
        profile=saveProfile(user_instance,profile_instance,group)
        )
    government.save()
    return government


def saveIncubator(incubator_instance,
                request,
                incubator_description_instance,
                address_instance,
                user_instance,profile_instance,group,context):
    def setFundedOther():
        if incubator_instance['funded_by'] == 'Other':
            return request.POST['other__funded_by']
        else:
            return ''
    def setOwnerOther():
        if incubator_instance['ownership'] == 'Other':
            return request.POST['other__ownership']
        else:
            return ''
        
    incubator = IncubatorsAccelatorsHub(service=incubator_instance['service'],
        ownership=incubator_instance['ownership'],
        ownership_other=setOwnerOther(),
        focusIndustry=incubator_instance['focusIndustry'],
        level=incubator_instance['level'],
        funded_by=incubator_instance['funded_by'],
        funded_by_other=setFundedOther(),
        program_duration=incubator_instance['program_duration'],
        attachments=incubator_instance['attachments'],
        description=saveIncubatorDescription(request,incubator_description_instance),
        address=saveAddress(request,address_instance,context),
        profile=saveProfile(user_instance,profile_instance,group)
        )
    incubator.save()
    return incubator

def saveMentor(mentor_instance,request,description_instance,address_instance,user_instance,profile_instance,group,context):
    def checkEduLevel():
        if mentor_instance['educational_level'] == 'other':
            return request.POST['other_educational_level']
        else:
            return ''
    def checkBackground():
        if mentor_instance['educational_background'] == 'other':
            return request.POST['other_educational_background']
        else:
            return ''
    def checkMentorArea():
         if mentor_instance['mentor_area'] == 'other':
            return request.POST['other_mentor_area']
         else:
              return ''
    mentor = Mentor(educational_level=mentor_instance['educational_level'],
    educational_level_other=checkEduLevel(),
    educational_background = mentor_instance['educational_background'],
    educational_background_other = checkBackground(),
    mentor_area = mentor_instance['mentor_area'],
    mentor_area_other = checkMentorArea() ,
    airelated_expriance = mentor_instance['airelated_expriance'],
    attachments = mentor_instance['attachments'],
    description=saveDescription(request,description_instance),
    address=saveAddress(request,address_instance,context),
    profile=saveProfile(user_instance,profile_instance,group)
    )
    mentor.save()
    return mentor
     

def saveStartupObject(request,context):
    group = Group.objects.get(name=request.POST['Startup'])           
    valid_startup = context['startup_form'].is_valid()
    valid_descriptions = context['description'].is_valid()
    valid_region= context['region_form'].is_valid() 
    valid_address = context['address'].is_valid() 
    valid_profile = context['profile'].is_valid()
    valid_user = context['user_form'].is_valid()
    address_instance = context['address'].cleaned_data
    description_instance = context['description'].cleaned_data
    profile_instance = context['profile'].cleaned_data
    startup_instance = context['startup_form'].cleaned_data
    user_instance = context['user_form'].cleaned_data 
    if valid_descriptions and valid_startup  and valid_region and valid_address and valid_profile and valid_user:
        try:
            with transaction.atomic():
                 saveStartup(startup_instance,
                request,
                description_instance,
                address_instance,
                user_instance,profile_instance,group,context)
        except DatabaseError as e:
            print(e)
        return redirect("main:homepage")
    else:
        return redirect ("main:homepage")
    
def saveMentorObject(request,context):
            print(context['address'].is_valid())
            valid_mentor = context['mentor_form'].is_valid()
            valid_descriptions = context['description'].is_valid()
            valid_region= context['region_form'].is_valid() 
            valid_address = context['address'].is_valid() 
            valid_profile = context['profile'].is_valid()
            valid_user = context['user_form'].is_valid() 
            if valid_descriptions and valid_mentor  and valid_region and valid_address and valid_profile and valid_user:
                group = Group.objects.get(name=request.POST['Startup'])
                address_instance = context['address'].cleaned_data
                description_instance = context['description'].cleaned_data
                profile_instance = context['profile'].cleaned_data
                mentor_instance = context['mentor_form'].cleaned_data
                user_instance = context['user_form'].cleaned_data
                try:
                    with transaction.atomic():
                        saveMentor(mentor_instance,
                                   request,
                                   description_instance,
                                   address_instance,
                                   user_instance,
                                   profile_instance,
                                   group,context)      
                except DatabaseError as e:
                    print(e)
                return redirect("main:homepage")
            else:
                for field, errors in context['mentor_form'].errors.items():
                     print("Error in field {}: {}".format(field, errors))

def saveIncubatorObject(request,context):
            valid_incubator_description = context['incubator_description'].is_valid()
            valid_incubator = context['incubator_form'].is_valid()
            valid_descriptions = context['description'].is_valid()
            valid_region= context['region_form'].is_valid() 
            valid_address = context['address'].is_valid() 
            valid_profile = context['profile'].is_valid()
            valid_user = context['user_form'].is_valid() 
            print(valid_incubator_description)
            if valid_incubator_description and valid_incubator  and valid_region and valid_address and valid_profile and valid_user:
                print(Group.objects.get(name="Incubator/Hub/Acclerator"))
                group = Group.objects.get(name=request.POST['Startup'])
                address_instance = context['address'].cleaned_data
                incubator_description_instance = context['incubator_description'].cleaned_data
                profile_instance = context['profile'].cleaned_data
                incubator_instance = context['incubator_form'].cleaned_data
                user_instance = context['user_form'].cleaned_data
                try:
                    with transaction.atomic():
                        saveIncubator(incubator_instance,
                                   request,
                                   incubator_description_instance,
                                   address_instance,
                                   user_instance,
                                   profile_instance,
                                   group,context)      
                except DatabaseError as e:
                    print(e)
                return redirect("main:homepage")
            else:
                for field, errors in context['incubator_form'].errors.items():
                     print("Error in field {}: {}".format(field, errors))


def saveDonorObject(request,context):
            valid_donor = context['donor_form'].is_valid()
            valid_descriptions = context['description'].is_valid()
            valid_region= context['region_form'].is_valid() 
            valid_address = context['address'].is_valid() 
            valid_profile = context['profile'].is_valid()
            valid_user = context['user_form'].is_valid() 
            print(valid_descriptions)
            if valid_descriptions and valid_donor  and valid_region and valid_address and valid_profile and valid_user:
                print(request.POST['Startup'])
                group = Group.objects.get(name=request.POST['Startup'])
                address_instance = context['address'].cleaned_data
                description_instance = context['description'].cleaned_data
                profile_instance = context['profile'].cleaned_data
                donor_instance = context['donor_form'].cleaned_data
                user_instance = context['user_form'].cleaned_data
                try:
                    with transaction.atomic():
                        saveDonor(donor_instance,
                                   request,
                                   description_instance,
                                   address_instance,
                                   user_instance,
                                   profile_instance,
                                   group,context)      
                except DatabaseError as e:
                    print(e)
                return redirect("main:homepage")
            else:
                for field, errors in context['donor_form'].errors.items():
                     print("Error in field {}: {}".format(field, errors))


def saveGovernmentObject(request,context):
            valid_government= context['government_form'].is_valid()
            valid_descriptions = context['description'].is_valid()
            valid_region= context['region_form'].is_valid() 
            valid_address = context['address'].is_valid() 
            valid_profile = context['profile'].is_valid()
            valid_user = context['user_form'].is_valid() 
            print(valid_descriptions)
            if valid_descriptions and valid_government and valid_region and valid_address and valid_profile and valid_user:
                print(request.POST['Startup'])
                group = Group.objects.get(name=request.POST['Startup'])
                address_instance = context['address'].cleaned_data
                description_instance = context['description'].cleaned_data
                profile_instance = context['profile'].cleaned_data
                government_instance = context['government_form'].cleaned_data
                user_instance = context['user_form'].cleaned_data
                try:
                    with transaction.atomic():
                        saveGovernment(government_instance,
                                   request,
                                   description_instance,
                                   address_instance,
                                   user_instance,
                                   profile_instance,
                                   group,context)      
                except DatabaseError as e:
                    print(e)
                return redirect("main:homepage")
            else:
                for field, errors in context['government_form'].errors.items():
                     print("Error in field {}: {}".format(field, errors))
