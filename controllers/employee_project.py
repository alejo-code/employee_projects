# -*- coding: utf-8 -*-
# Copyright 2024 Alejandro Olano <Github@alejo-code>

from odoo import http
from odoo.http import request
import json


class EmployeeProjectPortal(http.Controller):

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

    @http.route(["/employee_projects/playground"], type="http", auth="public")
    def show_playground(self):
        """
        Renders the owl playground page
        """
        return request.render("employee_projects.playground")

    @http.route(["/employee_projects/create_project"], type="http", auth="public")
    def create_project(self):
        """
        Renders the owl playground page
        """
        return request.render("employee_projects.create_project")
