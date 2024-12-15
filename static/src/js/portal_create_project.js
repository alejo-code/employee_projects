odoo.define('employee_projects.portal_create_project', function (require) {
    "use strict";

    const ajax = require('web.ajax');
    const core = require('web.core');
    const _t = core._t;

    function createProject(event) {
        event.preventDefault();

        
        const Name = $('#name').val().trim();
        const Description = $('#description').val().trim();
        const StartDate = $('#start_date').val().trim();
        const EndDate = $('#end_date').val().trim();
        const Employee = $('#employee_id').val().trim();

        
        
        ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            model: 'employee.project',  
            method: 'create',      
            args: [{
                'name': Name,
                'description': Description,
                "start_date" : StartDate,
                "end_date": EndDate,
                "employee_id":Employee

            }], 
            kwargs: {},            
        })
        .then(function (result) {
            alert(_t('Nuevo socio creado con éxito.'));
            window.location.href = '/portal/my/profile'; // 
        })
        .catch(function (error) {
            console.error('Error:', error);
            alert(_t('Error al crear el nuevo socio.'));
        });
    }

    
    $(document).ready(function () {
        const form = $('#create_project_form');
        if (form.length) {
            form.on('submit', createProject); 
        } else {
            console.warn('Formulario no encontrado: #create_project_form');
        }
    });
});
