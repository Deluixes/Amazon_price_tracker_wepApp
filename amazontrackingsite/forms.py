from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .FunctionFindInfosinPage import *
from .models import *
from django.contrib.auth.forms import AuthenticationForm

class NewAmazonPageForm(forms.Form):
    page_url = forms.URLField(label='Enter the Amazon URL of a product to follow the price evolution'
                              , widget=forms.TextInput(attrs={'placeholder': 'https://www.amazon.'}))

    def clean_page_url(self):
        data = self.cleaned_data['page_url']
        list_infos = find_infos_in_amazon_page(data)
        product = ""

        if list_infos != "Error":
            name = list_infos[1]

            if AmazonPage.objects.filter(url=data).exists():
                product = AmazonPage.objects.get(url=data)
            elif AmazonPage.objects.filter(product_name=name).exists():
                product = AmazonPage.objects.get(product_name=name)


            # Vérifier si le produit est déjà suivi par l'utilisateur
            if FollowedAmazonPages.objects.filter(product_id=product.pk).exists():
                raise ValidationError(_('You already follow this product'))

        else:

            # Vérifier qu'il y a bien www.amazon.com dans l'URL'
            if 'https://www.amazon.' not in data:
                raise ValidationError(_('URL not from amazon. Please enter a valid amazon URL'))

            elif list_infos == "Error":
                raise ValidationError(_('The URL is not a URL from an amazon product page. Please enter a correct URL'))

        return data


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('page_url', css_class=''),
            ),
            Submit('submit', 'Add new product')
        )


class CustomLoginForm(AuthenticationForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update(
      {'class': 'my-username-class'}
    )
    self.fields['password'].widget.attrs.update(
      {'class': 'my-password-class'}
    )
