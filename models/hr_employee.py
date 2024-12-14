# -*- coding: utf-8 -*-
# Copyright 2024 Alejandro Olano <Github@alejo-code>

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    total_projects = fields.Integer(
        string="Nuber Of Project Employee",
        compute="_compute_total_projects",
        store=True,
    )

    employee_project_ids = fields.One2many(
        comodel_name="employee.project", inverse_name="employee_id", string="Projects"
    )

    @api.depends("employee_project_ids")
    def _compute_total_projects(self):
        for employee in self:
            employee.total_projects = len(employee.employee_project_ids)
