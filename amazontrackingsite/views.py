from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import *
from .forms import *
from .FunctionFindInfosinPage import *
from datetime import date
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


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
    price = 0
    name = ""
    error_message = ""

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
            # On checke si l'URL existe déjà dans la base de données des pages amazon
            if AmazonPage.objects.filter(url=url).exists():
                error_message = "You already follow this product."
                product = AmazonPage.objects.get(url=url)

                if not FollowedAmazonPages.objects.filter(product_id=product.pk).exists():
                    new_followed_product = FollowedAmazonPages(user_id=request.user.pk, product_id=product.pk)
                    new_followed_product.save()

            else:
                list_infos = find_infos_in_amazon_page(url)

                # On vérifie qu'on est bien sur une page amazon produit et non sur une page de navigation
                if list_infos == "Error":
                    error_message = "The URL is not a URL from an amazon product page. Please enter a correct URL"
                else:
                    price = list_infos[0]
                    name = list_infos[1]
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

    # S'il s'agit d'une requête GET (ou toute autre méthode), créer le formulaire par défaut.
    else:
        form = NewAmazonPageForm(initial={'renewal_date': 'url'})

    # On récupère la liste des produits suivis par le user logged in
    followed_products_list = FollowedAmazonPages.objects.filter(user_id=request.user)

    context = {
        'form': form,
        'followed_products_list': followed_products_list,
        'price': price,
        'name': name,
        'error_message': error_message,
    }

    return render(request, template_name, context)


@login_required
def product_detail_view(request, product_id):
    # Récupère les objets de product instance dont la clé est égale à primary key
    # products = get_object_or_404(ProductInstance, pk=product_id)

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
