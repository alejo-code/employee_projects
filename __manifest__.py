# -*- coding: utf-8 -*-
# Copyright 2024 Alejandro Olano <Github@alejo-code>
{
    "name": "Employee Project Management",
    "version": "16.0.1.0.0",
    "summary": "Extends Human Resources and adds custom views to the portal.",
    "description": """
        This module allows managing employee projects and extends functionalities
        of the Human Resources module. It includes:
        - New views for managing projects associated with employees.
        - Portal extensions to display projects and tasks to employees.
    """,
    "author": "Alejandro Olano <Github@alejo-code>",
    "category": "Human Resources",
    "website": "https://www.linkedin.com/in/alejocode/",
    "license": "LGPL-3",
    "depends": ["hr"],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/employee_project_view.xml",
    ],
}
