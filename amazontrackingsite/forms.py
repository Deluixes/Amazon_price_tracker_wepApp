from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class NewAmazonPageForm(forms.Form):
  page_url = forms.URLField(help_text="Enter a url from an amazon page")

  def clean_page_url(self):
    data = self.cleaned_data['page_url']

    # Vérifier qu'il y a bien www.amazon.com dans l'URL'
    if 'https://www.amazon.' not in data :
      raise ValidationError(_('URL not from amazon. Please enter a valid amazon URL'))

    return data
