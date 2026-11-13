const AuthService = {

    // Realiza o login do usuário.
    async login(email, senha) {

        const dados = await API.request("/login", {
            method: "POST",
            body: JSON.stringify({
                email: email,
                senha: senha
            })
        });

        // Guarda o token recebido do backend.
        sessionStorage.setItem(
            "nutrihub_token",
            dados.access_token
        );

        return dados;
    },

    // Realiza o cadastro de um usuário.
    async register(nome, email, senha) {

        const dados = await API.request("/usuario", {
            method: "POST",
            body: JSON.stringify({
                nome: nome,
                email: email,
                senha: senha
            })
        });

        return dados;
    },

    // Encerra a sessão do usuário.
    logout() {
        sessionStorage.removeItem("nutrihub_token");
    }
};