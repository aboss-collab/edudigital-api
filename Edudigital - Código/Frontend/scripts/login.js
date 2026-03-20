document.getElementById("login-form").addEventListener("submit", async (event) => {

    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    try {

        const response = await fetch("http://127.0.0.1:5001/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data),
        });

        const fetchedData = await response.json();

        console.log(fetchedData);

        const mensagem = document.getElementById("mensagem");

        if (fetchedData.erro !== undefined) {

            mensagem.innerHTML = fetchedData.erro;

        } else {

            mensagem.innerHTML = fetchedData.mensagem;

            // salva usuário logado
            localStorage.setItem("id", fetchedData.id);
            localStorage.setItem("usuario", fetchedData.usuario);

            // redireciona para perfil
            window.location.href = "perfil.html";

        }

    } catch (erro) {

        console.error(erro);

        document.getElementById("mensagem").innerHTML =
            "Erro ao conectar com o servidor.";

    }

});
