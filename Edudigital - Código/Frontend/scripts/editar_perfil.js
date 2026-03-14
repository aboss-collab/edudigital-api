// MÁSCARA DE CPF AUTOMÁTICA
const cpfInput = document.getElementById("cpf");

cpfInput.addEventListener("input", function(e){

let value = e.target.value.replace(/\D/g, "");

value = value.replace(/(\d{3})(\d)/, "$1.$2");
value = value.replace(/(\d{3})(\d)/, "$1.$2");
value = value.replace(/(\d{3})(\d{1,2})$/, "$1-$2");

e.target.value = value;

});


// SALVAR PERFIL
document.getElementById("editar-form").addEventListener("submit", function(event){

event.preventDefault();

const formData = new FormData(event.target);
const data = Object.fromEntries(formData);

// pegar usuário já existente
let usuario = JSON.parse(localStorage.getItem("usuario")) || {};

// atualizar dados
usuario = { ...usuario, ...data };

// salvar novamente
localStorage.setItem("usuario", JSON.stringify(usuario));

// mensagem
alert("Perfil atualizado com sucesso!");

// voltar para login
window.location.href = "login.html";

});
