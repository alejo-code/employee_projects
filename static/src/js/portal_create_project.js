odoo.define('employee_projects.portal_create_project', function (require) {
    "use strict";

    const ajax = require('web.ajax');
    const rpc = require('web.rpc');
    const core = require('web.core');
    const _t = core._t;

    let employeeId = null; 

    function getCurrentUserId() {
        return new Promise(function (resolve, reject) {
            if (odoo.session_info && odoo.session_info.user_id) {
                resolve(odoo.session_info.user_id);
            } else {
                
                rpc.query({
                    model: 'res.users',
                    method: 'search_read',
                    args: [
                        [['id', '!=', false]], 
                        ['id'] 
                    ],
                    kwargs: { limit: 1 }, 
                }).then(function (users) {
                    if (users.length > 0) {
                        resolve(users[0].id);
                    } else {
                        reject('No se encontró un usuario válido.');
                    }
                }).catch(function (error) {
                    console.error('Error al obtener el ID del usuario actual:', error);
                    reject(error);
                });
            }
        });
    }

   
    function getEmployeeId(userId) {
        return rpc.query({
            model: 'hr.employee',
            method: 'search_read',
            args: [
                [['user_id', '=', userId]], 
                ['id'] 
            ],
            kwargs: { limit: 1 }, 
        }).then(function (employees) {
            if (employees.length > 0) {
                return employees[0].id;
            }
            return null; 
        }).catch(function (error) {
            console.error('Error al obtener el ID del empleado:', error);
            return null;
        });
    }

    // Función para crear un proyecto
    function createProject(event) {
        event.preventDefault();

        const Name = $('#name').val().trim();
        const Description = $('#description').val().trim();
        const StartDate = $('#start_date').val().trim();
        const EndDate = $('#end_date').val().trim();

        // Validar que la fecha de inicio no sea mayor a la fecha de fin
        if (StartDate && EndDate && new Date(StartDate) > new Date(EndDate)) {
            alert(_t('La fecha de inicio no puede ser mayor que la fecha de fin.'));
            return;
        }

        if (!employeeId) {
            alert(_t('No se encontró un empleado asociado al usuario actual.'));
            return;
        }

        // Llamada para crear el proyecto
        ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            model: 'employee.project',
            method: 'create',
            args: [{
                'name': Name,
                'description': Description,
                'start_date': StartDate,
                'end_date': EndDate,
                'employee_id': employeeId, 
            }],
            kwargs: {},
        })
        .then(function (result) {
            alert(_t('Proyecto creado con éxito.'));
            window.location.href = '/portal/my/profile';
        })
        .catch(function (error) {
            console.error('Error al crear el proyecto:', error);
            alert(_t('Error al crear el proyecto.'));
        });
    }

    // Lógica para ejecutar al cargar la página
    $(document).ready(function () {
        const form = $('#create_project_form');

        // Obtener el ID del usuario actual y luego el ID del empleado
        getCurrentUserId().then(function (userId) {
            return getEmployeeId(userId);
        }).then(function (id) {
            employeeId = id; // Guardamos el ID del empleado
        }).catch(function (error) {
            console.error('Error al inicializar el empleado:', error);
        });

        if (form.length) {
            form.on('submit', createProject); 
        } else {
            console.warn('Formulario no encontrado: #create_project_form');
        }
    });
});
