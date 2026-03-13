function irCadastro() {
    window.location.href = "pages/cadastro.html"
}
/* Function irInicio só funciona para voltar da Pagina Cadastro e Login */
function irInicio() {
    window.location.href = "../index.html";
}

function irLogin() {
    window.location.href = "pages/login.html";
}

function voltarLogin() {
    window.location.href = "login.html";
}

function voltarAulas() {
    window.location.href = "aula.html";
}

function irPagamentos() {
    window.location.href = "pagamentos.html"
}

function irPerguntas() {
    window.location.href = "perguntas.html"
}

function abrirAula(tipo) {
    localStorage.setItem("tipoAula", tipo)
    window.location.href = "aula.html"
}

document.addEventListener("DOMContentLoaded", function () {

    let aula = localStorage.getItem("tipoAula")
    let conteudo = document.getElementById("conteudoAula")

    if (!conteudo) return

    if (aula === "pix") {

        conteudo.innerHTML = `
            <h2>Como pagar com PIX</h2>

            <ol>
            <li>Abra o aplicativo do seu banco</li>
            <li>Toque na opção PIX</li>
            <li>Escolha "Pagar"</li>
            <li>Escaneie o QR Code ou digite a chave PIX</li>
            <li>Confira os dados do pagamento</li>
            <li>Confirme o pagamento</li>
            </ol>
            `

    }

    if (aula === "boleto") {

        conteudo.innerHTML = `
            <h2>Como pagar um boleto</h2>

            <ol>
            <li>Abra o aplicativo do banco</li>
            <li>Escolha a opção "Pagar boleto"</li>
            <li>Escaneie o código de barras</li>
            <li>Confira o valor</li>
            <li>Confirme o pagamento</li>
            </ol>
            `

    }

    if (aula === "cartao") {

        conteudo.innerHTML = `
            <h2>Como pagar com cartão</h2>

            <ol>
            <li>Escolha pagar com cartão</li>
            <li>Digite os dados do cartão</li>
            <li>Confira o valor da compra</li>
            <li>Confirme o pagamento</li>
            </ol>
            `
    }
})

function responderPergunta(pergunta) {

    let resposta = document.getElementById("resposta")

    if (!resposta) return

    if (pergunta === "pix") {

        resposta.innerHTML =
            "PIX é uma forma de pagamento instantâneo criada pelo Banco Central."
    }

    if (pergunta === "seguro") {

        resposta.innerHTML =
            "Sim, o PIX é seguro quando você confirma o destinatário antes de pagar."
    }

    if (pergunta === "erro") {

        resposta.innerHTML =
            "Se você pagar para a pessoa errada, deve entrar em contato com o banco."

    }

}
