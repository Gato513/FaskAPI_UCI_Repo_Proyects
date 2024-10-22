const modal = document.querySelector("#staticBackdrop")

modal.addEventListener('show.bs.modal', function (event) {
    // Botón que disparó el modal
    // const button = event.relatedTarget;

    console.log(event.relatedTarget)

    // // Extraer el valor del atributo data-id
    // const facultyId = button.getAttribute('data-id');

    // // Insertar el id en el campo oculto del formulario
    // const inputFacultyId = modal.querySelector('#faculty_id');
    // inputFacultyId.value = facultyId;
});