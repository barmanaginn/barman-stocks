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

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from management.models import ConsumptionHistory, Product

from . import PluginApp
from .models import Stock


@receiver(pre_save, sender=ConsumptionHistory)
def update_stock(sender, **kwargs):
    """Update stock when a transaction is made
    
    Args:
        sender (Model): sender of the signal
    
    Raises:
        Exception: raised if STOCKS_STRICT is set to True and when a transaction would make the stock negative
    """
    instance = kwargs["instance"]
    product = instance.product
    quantity = instance.quantity
    if product.stock.use_stock:
        if (
            product.stock.stock >= quantity
            or not PluginApp.BarmanPluginMeta.STOCKS_STRICT
        ):
            product.stock.stock -= quantity
            product.stock.save()
        else:
            raise Exception(
                _("The stock of the product does not authorize the operation.")
            )


@receiver(post_save, sender=Product)
def create_stocks(sender, instance, created, **kwargs):
    """Create a stock object when a product is created.
    
    Args:
        sender (Model): sender of the signal
        instance (Product): instance modified
        created (bool): True if the instance was just created
    """
    if created:
        Stock.objects.create(product=instance)


@receiver(post_save, sender=Stock)
def auto_disable_draft(sender, instance, created, **kwargs):
    """Auto disable use_stock on drafts if STOCKS_AUTO_DISABLE_DRAFT is true
    
    Args:
        sender (Model): sender of the signal
        instance (Product): instance modified
        created (bool): True if the instance was just created
    """
    if created:
        if (
            PluginApp.BarmanPluginMeta.STOCKS_AUTO_DISABLE_DRAFT
            and instance.product.draft_category != Product.DRAFT_NONE
        ):
            instance.use_stock = False
            instance.save()
