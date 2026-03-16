document.addEventListener("DOMContentLoaded", async () => {
    const id = localStorage.getItem("id")
    const resp = await fetch(`http://127.0.0.1:5000/usuarios/${id}`)
    const data = await resp.json()
    document.getElementById("nome").value = data.nome
    document.getElementById("email").value = data.email
    document.getElementById("senha").value = data.senha
})

document.getElementById("editar-form").addEventListener("submit", async (event) => {

    event.preventDefault();

    const id = localStorage.getItem("id")

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    try{
        const response = await fetch(`http://127.0.0.1:5000/usuarios/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        })
        const fetchedData = await response.json()

        if (fetchedData.erro !== undefined) {
            const errorMessage = document.getElementById("mensagem")
            errorMessage.innerHTML = fetchedData.erro

        } else {
            document.getElementById("mensagem").innerHTML = fetchedData.mensagem
        }
    } catch (err) {
        console.log(err)
    }

});
