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

from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from barman.plugin import BarmanPlugin


class PluginApp(BarmanPlugin):
    name = "barman_stocks"

    class BarmanPluginMeta:
        name = "Stocks"
        author = "Yoann Pietri"
        description = _("Add stocks for products")
        version = 0.1
        url = "https://github.com/barmanaginn/barman-stocks"
        email = "me@nanoy.fr"

        # Define here urls for navbar. See documentation for more details.
        nav_urls = (
            {
                "text": _("Stocks"),
                "icon": "fas fa-boxes",
                "link": reverse_lazy("plugins:barman_stocks:stocks"),
                "permission": "gestion.change_product",
                "login_required": True,
                "admin_required": False,
                "superuser_required": False,
            },
        )

        # Define here settings specific to this plugin. See documentation for more details.
        settings = (
            {
                "name": "STOCKS_STRICT",
                "description": _(
                    "If True, transactions that make the stock neagtive will return an error. If False, the stock goes in negative"
                ),
                "default": True,
            },
            {
                "name": "STOCKS_AUTO_DISABLE_DRAFT",
                "description": _(
                    "If True, draft products will automatically set use_stocks to False, as a different plugin should be used."
                ),
                "default": True,
            },
        )

        # Define here additionnal info for user profile. See documentation for more details.
        user_profile = ()

    def ready(self):
        from . import signals

        return super().ready()


default_app_config = "barman_stocks.PluginApp"
