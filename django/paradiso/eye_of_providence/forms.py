from django import forms
from paradiso.storage_backends import FaceStorage, EventStorage

# TODO: transform the cbv into these functions
# def rename_guest_photo(instance, filename):
#     ext = filename.split(".")[-1]
#     return "{}_{}.{}".format(instance.first_name, instance.last_name, ext)


# class GuestForm(forms.Form):
#     first_name = forms.CharField(label="First Name", max_length=100)
#     last_name = forms.CharField(label="Last Name", max_length=100)
#     photo = forms.ImageField(upload_to=rename_guest_photo, storage=FaceStorage())
