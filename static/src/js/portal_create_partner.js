odoo.define('employee_projects.portal_create_partner', function (require) {
    "use strict";

    const ajax = require('web.ajax');
    const core = require('web.core');
    const _t = core._t;

    function createPartner(event) {
        event.preventDefault();

        
        const partnerName = $('#partner_name').val().trim();
        const partnerEmail = $('#partner_email').val().trim();

       
        if (!partnerName || !partnerEmail) {
            alert(_t('Por favor, complete todos los campos.'));
            return;
        }

        
        ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            model: 'res.partner',  
            method: 'create',      
            args: [{
                'name': partnerName,
                'email': partnerEmail,
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
        const form = $('#create_partner_form');
        if (form.length) {
            form.on('submit', createPartner); 
        } else {
            console.warn('Formulario no encontrado: #create_partner_form');
        }
    });
});
