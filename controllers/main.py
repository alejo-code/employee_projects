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

    @http.route("/portal/create_project", type="http", auth="public", website=True)
    def create_project(self, **kwargs):
        # Recibir los datos del formulario
        name = kwargs.get("name")
        description = kwargs.get("description")
        start_date = kwargs.get("start_date")
        end_date = kwargs.get("end_date")
        employee = (
            request.env["hr.employee"]
            .sudo()
            .search([("user_id", "=", request.env.user.id)], limit=1)
        )

        if name and description:
            # Crear el nuevo socio (res.partner)
            partner = (
                request.env["employee.project"]
                .sudo()
                .create(
                    {
                        "name": name,
                        "description": description,
                        "employee_id": employee.id,
                        "start_date": start_date,
                        "end_date": end_date,
                    }
                )
            )
            # Redirigir al usuario a la vista del nuevo socio (o a otra página de confirmación)
            return request.redirect("/portal/my/profile")
        return request.render(
            "employee_projects.portal_create_project",
            {
                "error": "Por favor, complete todos los campos.",
            },
        )
