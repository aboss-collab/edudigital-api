document.getElementById("reg-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    const response = await fetch("http://127.0.0.1:5000/usuarios", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
    const fetchedData = await response.json()
    
    if(fetchedData.erro !== undefined) {
        const errorMessage = document.getElementById("mensagem")
        errorMessage.innerHTML = fetchedData.erro
    }
    
})