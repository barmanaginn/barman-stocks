# barman-stocks - plugin for barman
# Copyright © 2020 Yoann Pietri <me@nanoy.fr>
#
# barman-stocks is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# barman-stocks is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with barman-stocks.  If not, see <https://www.gnu.org/licenses/>.

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from barman.acl import active_required
from management.models import Category, Product

from .models import Stock


@active_required
@login_required
@permission_required("gestion.change_product")
def stocks(request):
    """
    View to update stocks of active products
    """
    categories = Category.objects.order_by("order")
    nostock_products = Product.objects.filter(stock__use_stock=False)
    return render(
        request,
        "barman_stocks/stocks.html",
        {"categories": categories, "nostock_products": nostock_products},
    )


@active_required
@login_required
@permission_required("gestion.change_product")
def update_stock(request, pk):
    """View to update the stock value
    
    Args:
        request (dict): django request
        pk (int): primary key of the product
    
    Returns:
        HttpResponse: indicate to client that the stock was updated
    """
    product = get_object_or_404(Product, pk=pk)
    if "stock" in request.GET:
        if hasattr(product, "stock") and product.stock.use_stock:
            product.stock.stock = request.GET.get("stock")
            product.stock.save()
    return HttpResponse(_("Stock was updated"))


@active_required
@login_required
@permission_required("gestion.change_product")
def switch_use_stock(request, pk):
    """View to activate or desactivate use_stock for a product
    
    Args:
        request (dict): django request
        pk (int): primary key of the product
    
    Returns:
        HttpResponse: redirection to stock main page
    """
    product = get_object_or_404(Product, pk=pk)
    if hasattr(product, "stock"):
        product.stock.use_stock = not product.stock.use_stock
        product.stock.save()
    return redirect(reverse("plugins:barman_stocks:stocks"))
