const selectFacultyCreate = document.querySelector("#select-faculty-create");
const selectCourseCreate = document.querySelector("#select-curso-create");

const selectFacultyEdit = document.querySelector("#select-faculty-edit");
const selectCourseEdit = document.querySelector("#select-curso-edit");

selectCourseCreate.innerHTML = "<option selected>Seleccione Facultad...</option>";
selectCourseEdit.innerHTML = "<option selected>Seleccione Facultad...</option>";

const handleFacultySelectorChange = (facultyId, selectorToModify) => {
  const requestOptions = {
    method: "GET",
    redirect: "follow",
    credentials: "include",
  };

  fetch(`https://faskapi-uci-repo-proyects.onrender.com/dashboard/parameters/courses_by_faculty/${facultyId}`, requestOptions)
    .then((response) => response.json())
    .then((result) => {
      const { status_code } = result;

      if (status_code !== 200) {
        const { error_detail } = result;
        selectorToModify.innerHTML = `<option selected>${error_detail}</option>`;
        return;
      }

      selectorToModify.innerHTML = "<option selected >Cursos</option>";

      const { courses } = result;

      // Rellenar el select con los cursos recibidos
      courses.forEach((course) => {
        const { id_curso, nombre_carrera, nombre_curso } = course;

        const option = document.createElement("option");
        option.value = id_curso;
        option.textContent = `${nombre_carrera} - ${nombre_curso}`;
        selectorToModify.appendChild(option);
      });
    })
    .catch((error) => {
      selectorToModify.innerHTML = "<option selected>Error</option>";
      console.error("Error:", error);
    });
};

selectFacultyCreate.addEventListener("change", function () {
  const facultyId = this.value;
  handleFacultySelectorChange(facultyId, selectCourseCreate);
});

selectFacultyEdit.addEventListener("change", function () {
  const facultyId = this.value;
  handleFacultySelectorChange(facultyId, selectCourseEdit);
});
