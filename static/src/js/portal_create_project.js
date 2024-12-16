odoo.define('employee_projects.portal_create_project', function (require) {
    "use strict";

    const ajax = require('web.ajax');
    const rpc = require('web.rpc');
    const core = require('web.core');
    const _t = core._t;

    let employeeId = null;
    let userId = null; 
    function fetchSessionInfo() {
        return ajax.jsonRpc('/portal/user_session_info', 'call', {})
            .then(function (data) {
                console.log('User Session Info:', data);
                return data.id;
            })
            .catch(function (error) {
                console.error('Error fetching session info:', error);
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
            window.location.href = '/';
        })
        .catch(function (error) {
            console.error('Error al crear el proyecto:', error);
            alert(_t('Error al crear el proyecto.'));
        });
    }

    // Lógica para ejecutar al cargar la página
    $(document).ready(function () {
        const form = $('#create_project_form');
        
        fetchSessionInfo().then(function (userId) {
            return getEmployeeId(userId);
        }).then(function (id) {
            employeeId = id; 
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
