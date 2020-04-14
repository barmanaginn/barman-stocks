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

"""
Add a init the stocks after a clean install
"""
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand

from management.models import Product

from ...models import Stock


class Command(BaseCommand):
    """
    Command, verifying each product to see if the associated stock exists.
    """

    help = "Verify all products for the stock object"

    def handle(self, *args, **options):
        i = 0
        for product in Product.objects.all():
            if not hasattr(product, "stock"):
                Stock.objects.create(product=product)
                i += 1
        print("{} stocks were created".format(i))
