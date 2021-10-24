from django import forms
from django.contrib.auth import models
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import fields, widgets
from django.http.request import validate_host
from guest.models import ContactModel, ProfilePic, AddroomModel, GuestReviewsModel


# User Authentication Form
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Edit user profile form
class EditUserProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


# user profile pic form
class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = ProfilePic
        fields = ['image']



# Guest Reviews form 
class GuestReviewsForm(forms.ModelForm):
    class Meta:
        model = GuestReviewsModel
        fields = ['experience', 'name', 'explain_experience']

        widgets = {
            'experience': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Name...'}),
            'explain_experience': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Explain Your Experience...'}),
        }

    def clean_explain_experience(self):
        explain_experience = self.cleaned_data.get('explain_experience')
        if len(explain_experience) <= 20:
            raise ValidationError("Explain your experience in (20 characters minimum and 220 characters maximum!)")
        else:
            return explain_experience



# Contact Form
class ContactForm(forms.ModelForm):
    subject = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Query Heading...'}))

    class Meta:
        model = ContactModel
        fields = ['name', 'email', 'subject', 'query']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name..'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your E-mail..'}),
            'query': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Explain Query Here...', 'rows': '5'}),
        }

    # Applying django form cleaning using clean_<field_name>
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) <= 3:
            raise ValidationError('Name is too short!')
        else:
            return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '.' not in email:
            raise ValidationError("Missing '.' symbol in email! ")
        elif '@' not in email:
            raise ValidationError("Missing '@' symbol in email! ")
        else:
            return email

    def clean_subject(self, *args, **kwargs):
        abuse = ['fake', 'spam', 'idiot', 'theif']
        subject = self.cleaned_data.get('subject')
        for ww in abuse:
            if ww in subject:
                raise ValidationError("Heading containing abusive words")
            else:
                return subject

    def clean_query(self, *args, **kwargs):
        query = self.cleaned_data.get('query')
        if  len(query) <= 50:
            raise ValidationError("Your query should be minimum 50 character.")
        else:
            return query


# Addroom New Room Form
class AddroomForm(forms.ModelForm):
    class Meta:
        model = AddroomModel
        fields = ['title', 'name', 'email', 'contact', 'country', 'state', 'district', 'pincode', 'for_rent', 'water_supply', 'kitchen', 'washroom', 'parking_space', 'troom', 'price', 'nearest_city', 'address', 'desc', 'rmg1', 'rmg2', 'rmg3', 'agreement']

        gender = [('Mr', 'Mr'), ('Mrs', 'Mrs')]
        country = [('', '---Select Country---')]
        state = [('', '---Select State---')]
        district = [('', '---Select District---')]
        renting = [('House', 'House'), ('Apartment', 'Apartment'), ('Room', 'Room')]

        widgets = {
            'title': forms.Select(choices=gender, attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'for_rent': forms.RadioSelect(choices=renting),
            'water_supply': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required':True, 'checked':True}),
            'kitchen': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required':False}),
            'washroom': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required':True, 'checked':True}),
            'parking_space': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required':False}),
            'troom': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Write short description about room/aprtment redarding locality and society etc...'}),
            'country': forms.Select(choices=country, attrs={'id': 'country', 'class': 'form-select'}),
            'state': forms.Select(choices=state, attrs={'id': 'state', 'class': 'form-select'}),
            'district': forms.Select(choices=district, attrs={'id': 'district', 'class': 'form-select'}),
            'nearest_city': forms.TextInput(attrs={'class': 'form-control'}),
            'pincode': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'agreement': forms.FileInput(attrs={'accept': 'application/pdf, application/vnd.ms-excel'}),
        }

    # Applying django form cleaning using clean_<field_name>
    def clean_water_supply(self):
        water_supply = self.cleaned_data.get('water_supply')
        if water_supply != 'True':
            raise ValidationError('A room must have water supply facility.')
        else:
            return water_supply

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) <= 3:
            raise ValidationError('Name is too short!')
        else:
            return name
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '.' not in email:
            raise ValidationError("Missing '.' symbol in email! ")
        elif '@' not in email:
            raise ValidationError("Missing '@' symbol in email! ")
        else:
            return email
    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if pincode < 100000:
            raise ValidationError('Please enter a valid pincode/zipcode!')
        else:
            return pincode
    def clean_troom(self):
        troom = int(self.cleaned_data.get('troom'))
        if troom >= 100:
            raise ValidationError('Please enter less than 100 room!')
        else:
            return troom
    def clean_price(self):
        price = int(self.cleaned_data.get('price'))
        if price <= 2000:
            raise ValidationError('Please enter greater than  Rs.2000/- rupee ')
        else:
            return price
    def clean_desc(self, *args, **kwargs):
        desc = self.cleaned_data.get('desc')
        if  len(desc) <= 50:
            raise ValidationError("Room description should be minimum of 50 character!")
        else:
            return desc

