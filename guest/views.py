from django.contrib import messages
from django.contrib.auth import forms
from django.contrib.auth.backends import RemoteUserBackend
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from guest.forms import ContactForm, UserRegistrationForm, EditUserProfileForm, ProfilePicForm, AddroomForm, GuestReviewsForm
from guest.models import AddroomModel, GuestReviewsModel
from django.contrib.auth.models import User
from django.db.models import Q


# Create your views here.

########## Difference b/w render and redirect ###########
    # REDIRECT: means you are sending someone to a particular position. for example, 
    # if you are going to Pune to Mumbai then you are redirected to Pune to Mumbai. 
    # in computer terms if you click on any link then it will redirect you on a specific page. 
    # that is called redirect.
    # 1-) Redirect will give a new URL.

    # RENDER: means you are collecting some information through a data set. means you go to Mumbai 
    # and ask for some good places to explore that is data rendering. and in computer terms, 
    # you set a function to get the location of a particular user when he comes to a particular page. 
    # then this is the data rendering of location
    # 1-) Render will give a new webpage but not a new URL.


# Index page views
def index_view(request):
    return render(request, 'index.html')


# About us views
def about_view(request):
    return render(request, 'about.html')


# contact us views
def contact_view(request):
    context = {}
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your query has been submitted successfully. Thank You!')
            return redirect('contact')
            
    context['form'] = form
    return render(request, 'contact.html', context)


# user register views
def register_view(request):
    context = {}
    form = UserRegistrationForm()
    if request.method == 'POST':
        agree = request.POST.get('consent')
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            ###### code for automatic login after registration if user check the Keep Login Me #######     
            if agree == 'YES':
                password = form.cleaned_data.get('password1')
                user = authenticate(request, username=username, password=password)
                login(request, user)
                messages.success(request, 'Loged in successfully ' + username)
                return redirect('account_settings')
            else:
                messages.success(request, 'Account Created successfully ' + username)
                return redirect('login')

    context['form'] = form
    return render(request, 'register.html', context)


# User Login views
def login_view(request):
    context ={}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                messages.success(request, 'Logged in successfully ' + username)
                return redirect('dashboard', request.user.id)
        else:
            messages.warning(request, 'Username or password is incorrect')
    return render(request, 'login.html', context)


# User Logout view
def logout_view(request):
    logout(request)
    messages.success(request, 'Loged out successfully ')
    return redirect('index')


# User profile account settings views handling two form parallel (EditUserProfileForm and ProfilePicForm)
@login_required(login_url='login')
def account_settings_view(request):
    context = {}
    if request.method == 'POST':
        u_form = EditUserProfileForm(request.POST, instance=request.user)
        p_form = ProfilePicForm(request.POST, request.FILES, instance=request.user.profilepic)
        if u_form.is_valid() and p_form.is_valid():
            messages.success(request, 'Your profile is updated successfully!')
            u_form.save()
            p_form.save()
    else:
        u_form = EditUserProfileForm(instance=request.user)
        p_form = ProfilePicForm(instance=request.user.profilepic)
    context['u_form'] = u_form
    context['p_form'] = p_form
    return render (request, 'account_settings.html', context)


# update password with Old password views
@login_required(login_url='login')
def update_password_view(request):
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            messages.success(request, 'Your password is updated successfully!')
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('account_settings')
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form 
    return render(request, 'update_password.html', context)


# Delete User account views
@login_required(login_url='login')
def delete_user_account_view(request, pk):
    rooms = AddroomModel.objects.filter(user=pk)
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        user.delete()
        messages.success(request, 'Your account is deleted permanently!')
        return redirect('index')

    return render(request, 'delete_user.html', {'rooms': rooms})


# Adding new room views
@login_required(login_url='login')
def addroom_view(request):
    context = {}
    form = AddroomForm()
    if request.method == 'POST':
        # stn = request.POST.get('state_name')
        # print(stn)
        form = AddroomForm(request.POST, request.FILES)
        if form.is_valid():
            instanse = form.save(commit=False)
            instanse.user = request.user
            instanse.save()
            messages.success(request, 'Your room has been registered successfully. Thank You!')
            return redirect('dashboard', request.user.id)
        else:
            messages.error(request, "Please fill correct detail's. Verify your form again?")
                
    context['form'] = form
    return render(request, 'addroom.html', context)


# Updating added rooms
@login_required(login_url='login')
def update_room_view(request, pk):
    context = {}
    room = AddroomModel.objects.get(id=pk)
    form = AddroomForm(instance=room)
    if request.method == 'POST':
        form = AddroomForm(request.POST, instance=room)
        if form.is_valid():
            instanse = form.save(commit=False)
            instanse.user = request.user
            instanse.save()
            messages.success(request, 'Your room details is updated successfully. Thank You!')
            return redirect('dashboard', request.user.id)

    context['form'] = form
    return render(request, 'addroom.html', context)


# Delete room view
@login_required(login_url='login')
def delete_room_view(request, pk):
    context = {}
    room = AddroomModel.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Your room is deleted permanently. Thank You!')
        return redirect('dashboard', request.user.id)

    context['room'] = room
    return render(request, 'delete_room.html', context)


# User Dashboard view
@login_required(login_url='login')
def dashboard_view(request, pk):
    context = {}
    user = User.objects.get(id=pk)
    allrooms = user.addroommodel_set.all()
    # print(len(allrooms))
    # print(allrooms)
    context['allrooms'] = allrooms
    return render(request, 'dashboard.html', context)


# Custom fucntion for filtering room based on city/district name 
def filter_city(qset):
    room_by_city = AddroomModel.objects.filter(nearest_city=qset.upper()).order_by('-pub_date')
    room_by_district_name = AddroomModel.objects.filter(district=qset.upper()).order_by('-pub_date')
    room_by_address = AddroomModel.objects.filter(address__icontains=qset.upper()).order_by('-pub_date')

    if room_by_city:
        return room_by_city
    elif room_by_district_name:
        return room_by_district_name
    else:
        return room_by_address   


# Searched room view
def search_view(request):
    context = {}
    if request.method =='GET':
        qset = request.GET.get('query')

        if qset:
            # Calling Custom fucntion for filtering room based on search query
            context['allrooms'] = filter_city(qset)          

        else:
            context['alert'] = 'Please enter city name or district name!'
            return render(request, 'index.html', context)

    context['qset'] = qset
    return render(request, 'search.html', context)


#  Search filter for searched room
def search_filter_view(request):
    context = {}
    if request.method == 'GET':
        qset = request.GET.get('qset')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        nroom = request.GET.get('nroom')
        for_rent = request.GET.get('rtype')
        water_supply = request.GET.get('water', 'False')
        kitchen = request.GET.get('kitchen', 'False')
        washroom = request.GET.get('washroom', 'False')
        parking_space = request.GET.get('parking', 'False')

        if qset:
            ### Use __lte(double underscore less than equal to) after the model field for filtering ###
            filtertered = filter_city(qset)
            room_by_price_range = filtertered.filter(price__range=(min_price, max_price))
            
            if for_rent == 'Room':
                room_by_rent_type = room_by_price_range.filter(for_rent=for_rent)
                room_by_troom = room_by_rent_type.filter(Q(troom__lte=int(nroom)+1) & Q(troom__gte=int(nroom)-1))
                if kitchen=='True' or washroom=='True' or water_supply=='True' or parking_space=='True':
                    room_by_facility = room_by_troom.filter(Q(washroom=washroom) | Q(kitchen=kitchen) | Q(water_supply=water_supply) | Q(parking_space=parking_space))
                    context['allrooms'] = room_by_facility

            elif for_rent == 'Apartment':
                room_by_rent_type = room_by_price_range.filter(for_rent=for_rent)
                room_by_troom = room_by_rent_type.filter(Q(troom__lte=int(nroom)+1) & Q(troom__gte=int(nroom)-1))
                if kitchen=='True' or washroom=='True' or water_supply=='True' or parking_space=='True':
                    room_by_facility = room_by_troom.filter(Q(washroom=washroom) | Q(kitchen=kitchen) | Q(water_supply=water_supply) | Q(parking_space=parking_space))
                    context['allrooms'] = room_by_facility

            else:
                room_by_rent_type = room_by_price_range.filter(for_rent=for_rent)
                room_by_troom = room_by_rent_type.filter(Q(troom__lte=int(nroom)+1) & Q(troom__gte=int(nroom)-1))
                if kitchen=='True' or washroom=='True' or water_supply=='True' or parking_space=='True':
                    room_by_facility = room_by_troom.filter(Q(washroom=washroom) | Q(kitchen=kitchen) | Q(water_supply=water_supply) | Q(parking_space=parking_space))
                    context['allrooms'] = room_by_facility

            context['qset'] = qset
            return render(request, 'search.html', context)

        else:
            context['alert'] = 'Please enter city name or district name!'
            return render(request, 'index.html', context)


# Displaying room details with guest reviews
def room_view(request, rid):
    context = {}
    form = GuestReviewsForm()
    context['form'] = form
    if request.method == 'POST':
        form = GuestReviewsForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.addroommodel = AddroomModel.objects.get(id=rid)
            instance.save()
            messages.success(request, 'Your review is submitted successfully. Thank You!')
        else:
            context['form'] = form
            context['warmsg'] = 'Explain your experience in (20 characters minimum and 220 characters maximum!)'

    ################ IMPORTANT_NOTE ############################
    ### "rid" must be the same name in the urls path ###
    ### "id" must be the same name in the "AddroomModel" models ###
    room = AddroomModel.objects.get(id=rid)
    ############### IMPORTANT_NOTE #############################
    ### get(): Returns the object matching the given lookup parameters, which should be in the format described in Field lookups.
    ### filter(): Returns a new QuerySet containing objects that match the given lookup parameters.
    
    ##### Sending reviews to display in templates ######
    reviews = GuestReviewsModel.objects.filter(addroommodel=rid)
    context['reviews'] = reviews

    context['view'] = room
    return render(request, 'room.html', context)


from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# View for contact owner by the user and sending email to the room owner
def contact_owner_view(request, rid):
    room = AddroomModel.objects.get(id=rid)
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        msg = request.POST.get('msg')

        template = render_to_string('email_template.html', {'name': name, 'phone': phone, 'msg': msg, 'room': room})

        email = EmailMessage(
            'Regarding your room posted on "www.renthouse.com" website',
            template,
            settings.EMAIL_HOST_USER,
            [room.email]
        )
        email.fail_silently=False
        email.send()
        messages.success(request, 'Your details has been send to the owner. Thenk You!')

    return render(request, 'contact_owner.html', {'room': room})
