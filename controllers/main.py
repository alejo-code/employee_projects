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

    @http.route("/my/employee", type="json", auth="user")
    def get_employee_data(self):
        user = request.env.user
        employee = request.env["hr.employee"].search(
            [("user_id", "=", user.id)], limit=1
        )
        if employee:
            return {
                "id": employee.id,
                "name": employee.name,
                "job_title": employee.job_title,
                "department": employee.department_id.name,
                "work_email": employee.work_email,
                "work_phone": employee.work_phone,
            }
        return {}

    @http.route(["/my/employee_projects"], type="http", auth="user", website=True)
    def portal_employee_projects(self, **kwargs):

        employee = (
            request.env["hr.employee"]
            .sudo()
            .search([("user_id", "=", request.env.user.id)], limit=1)
        )
        projects = (
            request.env["employee.project"]
            .sudo()
            .search([("employee_id", "=", employee.id)])
        )

        return request.render(
            "employee_projects.portal_my_projects",
            {
                "projects": projects,
                "employee": employee,
            },
        )

    @http.route(
        ["/my/employee_projects/<int:project_id>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_employee_project_detail(self, project_id, **kwargs):
        project = request.env["employee.project"].sudo().browse(project_id)
        if not project or project.employee_id.user_id.id != request.env.user.id:
            return request.render("http_routing.http_404")

        return request.render(
            "employee_projects.portal_employee_project_detail",
            {
                "project": project,
            },
        )

    @http.route(["/my/home"], type="http", auth="user", website=True)
    def portal_my_home(self, **kwargs):
        values = {}
        employee = (
            request.env["hr.employee"]
            .sudo()
            .search([("user_id", "=", request.env.user.id)], limit=1)
        )
        projects = (
            request.env["employee.project"]
            .sudo()
            .search([("employee_id", "=", employee.id)])
        )

        values.update(
            {
                "projects": projects,
            }
        )
        response = request.render("portal.portal_my_home", values)
        return response

    @http.route(["/"], type="http", auth="user", website=True)
    def index(self, **kw):
        values = {}
        employee = (
            request.env["hr.employee"]
            .sudo()
            .search([("user_id", "=", request.env.user.id)], limit=1)
        )
        projects = (
            request.env["employee.project"]
            .sudo()
            .search([("employee_id", "=", employee.id)])
        )

        values.update(
            {
                "projects": projects,
            }
        )
        response = request.render("employee_projects.website_my_home_extension", values)
        return response

    @http.route("/portal/user_session_info", type="json", auth="public")
    def user_session_info(self):
        user = http.request.env.user
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "login": user.login,
        }
