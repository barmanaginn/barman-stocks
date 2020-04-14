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

from django.db import models
from django.utils.translation import ugettext_lazy as _

from management.models import Product


class Stock(models.Model):
    """Stock object.

    For each product, it uniquely associates a stock object.
    """

    class Meta:
        verbose_name = _("Stock")

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, verbose_name=_("Product")
    )
    use_stock = models.BooleanField(default=True, verbose_name=_("Use stock"))
    stock = models.IntegerField(verbose_name=_("Stock"), default=0)
