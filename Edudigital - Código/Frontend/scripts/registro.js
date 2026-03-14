document.getElementById("reg-form").addEventListener("submit", async (event) => {


    event.preventDefault();


    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    try {

        const response = await fetch("http://127.0.0.1:5000/usuarios", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const fetchedData = await response.json();

        const mensagem = document.getElementById("mensagem");


        if (fetchedData.erro !== undefined) {
            mensagem.innerHTML = fetchedData.erro;
            return;
        }


        if (fetchedData.mensagem !== undefined) {

            mensagem.innerHTML = fetchedData.mensagem;


            document.getElementById("perfil-nome").innerHTML = data.nome;
            document.getElementById("perfil-email").innerHTML = data.email;


            document.getElementById("perfil-senha").innerHTML = "********";


            document.getElementById("cadastro-card").style.display = "none";


            document.getElementById("perfil-card").style.display = "block";
        }

    } catch (erro) {

        document.getElementById("mensagem").innerHTML = "Erro ao conectar com o servidor.";

        console.error(erro);
    }

});

function editarPerfil() {
    window.location.href = "editar_perfil.html";
}
