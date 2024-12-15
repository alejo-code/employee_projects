# -*- coding: utf-8 -*-
# Copyright 2024 Alejandro Olano <Github@alejo-code>

from odoo import http
from odoo.http import request
import json


class Main(http.Controller):
    @http.route("/employee_projects/custom", type="http", auth="public", website=True)
    def employee_projects_custom(self, **kw):
        return request.render(
            "employee_projects.custom_page",
        )

    @http.route(
        "/employee_projects/custom_rpc", type="http", auth="public", website=True
    )
    def employee_projects_custom_rpc(self, **kw):
        return request.render(
            "employee_projects.custom_page_rpc",
        )

    @http.route("/portal/create_partner", type="http", auth="public", website=True)
    def create_partner(self, **kwargs):
        # Recibir los datos del formulario
        name = kwargs.get("name")
        email = kwargs.get("email")

        if name and email:
            # Crear el nuevo socio (res.partner)
            partner = (
                request.env["res.partner"]
                .sudo()
                .create(
                    {
                        "name": name,
                        "email": email,
                    }
                )
            )
            # Redirigir al usuario a la vista del nuevo socio (o a otra página de confirmación)
            return request.redirect("/portal/my/profile")
        return request.render(
            "employee_projects.portal_partner_form",
            {
                "error": "Por favor, complete todos los campos.",
            },
        )
