const MODAL = document.querySelector('#staticBackdrop');
const EDITINGFORM = document.querySelector('#form_edit');
const BASE_ACTION_URL = "/dashboard/parameters/update";

MODAL.addEventListener('show.bs.modal', function (event) {
    // Obtener el id de la facultad desde el botón que activó el modal
    const FACULTYID = event.relatedTarget.getAttribute('data-id');
    
    // Obtener la referencia al parametro que se edita:
    const PARAMETER_REFERENCE = EDITINGFORM.getAttribute('parameter-to-update');

    console.log(`${BASE_ACTION_URL}/${PARAMETER_REFERENCE}/${FACULTYID}`)

    // Establecer la nueva URL con el id de la facultad (agregando '/' si es necesario)
    EDITINGFORM.setAttribute('action', `${BASE_ACTION_URL}/${PARAMETER_REFERENCE}/${FACULTYID}`);
});
