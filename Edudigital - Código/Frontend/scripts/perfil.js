document.addEventListener("DOMContentLoaded", async () => {
    const id = localStorage.getItem("id")
    const resp = await fetch(`http://127.0.0.1:5000/usuarios/${id}`)
    const data = await resp.json()
    document.getElementById("perfil-nome").innerHTML = data.nome
    document.getElementById("perfil-email").innerHTML = data.email
    document.getElementById("perfil-senha").innerHTML = "*********"
})

document.getElementById("deletar").addEventListener("click", async (event) => {
    event.preventDefault()

    const id = localStorage.getItem("id")

    if (confirm("Tem certeza que deseja excluir seu perfil?")) {
        console.log("SIIIM")
        try{
            const response = await fetch(`http://127.0.0.1:5000/usuarios/${id}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
            const fetchedData = await response.json()

            if (fetchedData.erro !== undefined) {
                const errorMessage = document.getElementById("mensagem")
                errorMessage.innerHTML = fetchedData.erro

            } else {
                document.getElementById("mensagem").innerHTML = fetchedData.mensagem
                window.location.href = "login.html"
                alert("Conta excliuída com sucesso!")
            }
        } catch (err) {
            console.log(err)
        }
    }

})