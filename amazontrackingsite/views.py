from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import *
from .forms import *
from .FunctionFindInfosinPage import *
from datetime import date
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.shortcuts import redirect


def index(request):
    """View function for home page of site."""
    context = {
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


@login_required
def AmazonProductsListView(request):
    # Liste des produits amazon et autres variables
    template_name = 'amazontrackingsite/amazonproducts_list.html'
    number_followed_products = FollowedAmazonPages.objects.filter(user_id=request.user).count()

    # Formulaire pour rentrer un nouvel URL et ajouter le produit à la liste
    ###########################################
    # S'il s'agit d'une requête POST, traiter les données du formulaire.
    if request.method == 'POST':

        # Créer une instance de formulaire et la peupler avec des données récupérées dans la requête (liaison) :
        form = NewAmazonPageForm(request.POST)

        # Vérifier que le formulaire est valide :
        if form.is_valid():

            # Traiter les données dans form.cleaned_data tel que requis (ici on les écrit dans le champ de modèle due_back) :
            url = form.cleaned_data['page_url']
            list_infos = find_infos_in_amazon_page(url)
            product = ""
            price = list_infos[0]
            name = list_infos[1]

            # On checke si l'URL existe déjà dans la base de données des pages amazon
            if AmazonPage.objects.filter(url=url).exists():
                product = AmazonPage.objects.get(url=url)
            elif AmazonPage.objects.filter(product_name=name).exists():
                product = AmazonPage.objects.get(product_name=name)

            if product != "": #Le produit est déjà suivi dans la base de données
                if not FollowedAmazonPages.objects.filter(product_id=product.pk).exists():
                    new_followed_product = FollowedAmazonPages(user_id=request.user.pk, product_id=product.pk)
                    new_followed_product.save()

            else: #Il faut commencer à suivre le nouveau produit
                today = date.today()
                new_date = today.strftime('%Y-%m-%d')

                # On créé la nouvelle entrée dans la base de données
                new_product = AmazonPage(url=url, product_name=name)
                new_product.save()

                new_followed_product = FollowedAmazonPages(user_id=request.user.pk, product_id=new_product.pk)
                new_followed_product.save()

                new_product_instance = ProductInstance(product_id=new_product.pk, product_price=price,
                                                       day_of_check=new_date)
                new_product_instance.save()
            return HttpResponseRedirect(reverse('products'))

    # S'il s'agit d'une requête GET (ou toute autre méthode), créer le formulaire par défaut.
    else:
        form = NewAmazonPageForm()

    # On récupère la liste des produits suivis par le user logged in
    followed_products_list = FollowedAmazonPages.objects.filter(user_id=request.user)

    context = {
        'form': form,
        'followed_products_list': followed_products_list,
        'number_followed_products': number_followed_products,
    }

    return render(request, template_name, context)


@login_required
def product_detail_view(request, product_id):
    # Récupère les objets de product instance dont la clé est égale à primary key

    # Récupère la liste des produit dont la clé est égale à la clé produit
    products_list = ProductInstance.objects.filter(product_id=product_id)
    amazon_page = AmazonPage.objects.filter(id=product_id).first()

    # Graphique
    template_name = 'amazontrackingsite/product_detail.html'
    data = []

    # Récupère seulement les objets ayant le même product_id que l'id produit et en triant par order de dayofcheck
    queryset = ProductInstance.objects.order_by('day_of_check').filter(product_id=product_id)
    for product in queryset:
        data.append({'x': product.day_of_check.strftime('%Y-%m-%d'), 'y': product.product_price})

    return render(request, template_name,
                  {  # 'product': products,
                      'data': data,
                      'product_list': products_list,
                      'amazon_page': amazon_page
                  })

@login_required
def followed_product_delete(request, id):
    followed_product = FollowedAmazonPages.objects.get(id=id, user_id=request.user)
    followed_product.delete()
    return HttpResponseRedirect(reverse('products'))

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"