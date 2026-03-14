const cpfInput = document.getElementById("cpf");

cpfInput.addEventListener("input", function (e) {

    let value = e.target.value.replace(/\D/g, "");

    value = value.replace(/(\d{3})(\d)/, "$1.$2");
    value = value.replace(/(\d{3})(\d)/, "$1.$2");
    value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");

    e.target.value = value;

});


document.getElementById("editar-form").addEventListener("submit", function (event) {

    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    let usuario = JSON.parse(localStorage.getItem("usuario")) || {};

    usuario = { ...usuario, ...data };

    localStorage.setItem("usuario", JSON.stringify(usuario));

    alert("Perfil atualizado com sucesso!");

    window.location.href = "login.html";

});
