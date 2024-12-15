odoo.define('employee_projects.portal_create_partner', function (require) {
    "use strict";

    const ajax = require('web.ajax');
    const core = require('web.core');
    const _t = core._t;

    function createPartner(event) {
        event.preventDefault();

        // Obtener valores del formulario
        const partnerName = $('#partner_name').val().trim();
        const partnerEmail = $('#partner_email').val().trim();

        // Validar que los campos no estén vacíos
        if (!partnerName || !partnerEmail) {
            alert(_t('Por favor, complete todos los campos.'));
            return;
        }

        // Realizar la llamada JSON-RPC para crear el nuevo socio
        ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            model: 'res.partner',  // Modelo a afectar
            method: 'create',      // Método a llamar
            args: [{
                'name': partnerName,
                'email': partnerEmail,
            }], // Lista de argumentos posicionales
            kwargs: {},            // Diccionario adicional (puede estar vacío)
        })
        .then(function (result) {
            alert(_t('Nuevo socio creado con éxito.'));
            window.location.href = '/portal/my/profile'; // Redirigir tras éxito
        })
        .catch(function (error) {
            console.error('Error:', error);
            alert(_t('Error al crear el nuevo socio.'));
        });
    }

    // Asociar evento al formulario cuando el DOM esté listo
    $(document).ready(function () {
        const form = $('#create_partner_form');
        if (form.length) {
            form.on('submit', createPartner); // Asignar función al evento submit
        } else {
            console.warn('Formulario no encontrado: #create_partner_form');
        }
    });
});
