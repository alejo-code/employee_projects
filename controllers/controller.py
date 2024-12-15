# -*- coding: utf-8 -*-
# Copyright 2024 Alejandro Olano <Github@alejo-code>

from odoo import http
from odoo.http import request
import json


class OwlPlayground(http.Controller):
    @http.route(["/owl_playground/playground"], type="http", auth="public")
    def show_playground(self):
        """
        Renders the owl playground page
        """
        return request.render("employee_projects.playground")

    @http.route("/get_products", type="json", auth="user")
    def get_products(self):
        products = request.env["product.product"].search([], limit=10)
        return [
            {"id": product.id, "name": product.name, "price": product.lst_price}
            for product in products
        ]
