from django import forms
from django.db import transaction
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic.edit import UpdateView
from .models import User, CarOwner, ShopOwner, ServiceDriver, Car, Service

# from phonenumber_field.modelfields import PhoneNumberField
from django.http import HttpResponseRedirect
import requests

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

class LoginForm(forms.Form):
    email = forms.CharField(label="Email", max_length=254)
    password = forms.CharField(widget=forms.PasswordInput())

class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Re-type Password"),
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email","first_name","last_name")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class CarOwnerSignUpForm(UserCreationForm):
    loc_office = forms.CharField(label='Office location', max_length=100)
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_car_owner = True
        user.save()
        car_owner = CarOwner.objects.create(user=user)
        car_owner.loc_office = self.cleaned_data.get('loc_office')
        car_owner.save()
        return user

class AddCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['car_year', 'car_make', 'car_model', 'car_model_trim', 'car_color', 'car_license', 'loc_parking']

class ShopOwnerSignUpForm(UserCreationForm):
    shop_name = forms.CharField(label='Shop name',max_length=100)
    address_street = forms.CharField(label='Address',max_length=100)
    address_gps_lat = forms.DecimalField(label='address_gps_lat', max_digits=10, decimal_places=6)
    address_gps_lng = forms.DecimalField(label='address_gps_lng', max_digits=10, decimal_places=6)
    phone_number = forms.CharField(label='Phone number',max_length=100)
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_shop_owner = True
        user.save()
        shop_owner = ShopOwner.objects.create(user=user)
        shop_owner.shop_name = self.cleaned_data.get('shop_name')
        shop_owner.address_street = self.cleaned_data.get('address_street')
        shop_owner.phone_number = self.cleaned_data.get('phone_number')
        # Prepare for Google Maps geocode API
        params = {
            'address': self.cleaned_data.get('address_street'),
            'sensor': 'false',
            'region': 'us'
        }

        # Make the request and get the response data
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()

        # Use the first result
        result = res['results'][0]

        shop_owner.address_street = result['formatted_address']
        shop_owner.address_gps_lat = result['geometry']['location']['lat']
        shop_owner.address_gps_lng = result['geometry']['location']['lng']
        shop_owner.save()
        return user

class EditShopForm(forms.ModelForm):
    class Meta:
        model = ShopOwner
        fields = ('shop_name', 'address_street', 'phone_number')

class PostRequestForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('description', 'date', 'shop')

def update_address(request):
    form = AddressForm(request.POST)
    if form.is_valid():
        address = form.save(commit = False)
        # Prepare for Google Maps geocode API
        params = {
            'address': address.street,
            'sensor': 'false',
            'region': 'us'
        }

        # Make the request and get the response data
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()

        # Use the first result
        result = res['results'][0]

        # Save the result into the address database
        address.user = request.user
        address.street = result['formatted_address']
        address.gps_lat = result['geometry']['location']['lat']
        address.gps_lng = result['geometry']['location']['lng']
        address.save()
    return_to = '/'
    return HttpResponseRedirect('/maps')

class ServiceDriverSignUpForm(UserCreationForm):
    is_over_21 = forms.BooleanField(label='is_over_21')
    is_gpa_over3 = forms.BooleanField(label='is_gpa_over3')
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_service_driver = True
        user.save()
        service_driver = ServiceDriver.objects.create(user=user)
        service_driver.is_over_21 = self.cleaned_data.get('is_over_21')
        service_driver.is_gpa_over3 = self.cleaned_data.get('is_gpa_over3')
        service_driver.save()
        return user
