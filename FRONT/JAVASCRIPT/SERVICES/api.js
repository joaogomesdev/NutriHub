// Endereço do nosso backend FastAPI.
const API_CONFIG = {
    BASE_URL: "http://127.0.0.1:8000"
};

// Serviço responsável pelas requisições HTTP.
const API = {

    async request(endpoint, options = {}) {

        const headers = {
            "Content-Type": "application/json",
            ...options.headers
        };

        // Recupera o token JWT, caso exista.
        const token = sessionStorage.getItem("nutrihub_token");

        if (token) {
            headers.Authorization = `Bearer ${token}`;
        }

        const response = await fetch(
            `${API_CONFIG.BASE_URL}${endpoint}`,
            {
                ...options,
                headers
            }
        );

        // Converte a resposta da API para JSON.
        const data = await response.json();

        // Trata erros retornados pelo backend.
        if (!response.ok) {
            throw new Error(
                data.detail || "Erro ao comunicar com o servidor."
            );
        }

        return data;
    },

    async getMe() {
        return await this.request("/me");
    },

    async alterarSenha(dados) {
        return await this.request("/usuario/senha", {
            method: "PUT",
            body: JSON.stringify(dados)
        });
    },

    async getQuestionario() {
        return await this.request("/questionario");
    },

    async getPlanoAlimentar() {
        return await this.request("/plano-alimentar");
    },

    async getRefeicoes() {
        return await this.request("/refeicoes");
    },

    async criarRefeicao(dados) {
        return await this.request("/refeicoes", {
            method: "POST",
            body: JSON.stringify(dados)
        });
    },

    async excluirRefeicao(id) {
        return await this.request(`/refeicoes/${id}`, {
            method: "DELETE"
        });
    },

    async getMetas() {
        return await this.request("/metas");
    },

    async criarMeta(dados) {
        return await this.request("/metas", {
            method: "POST",
            body: JSON.stringify(dados)
        });
    },

    async atualizarConclusaoMeta(id, concluida) {
        return await this.request(`/metas/${id}`, {
            method: "PATCH",
            body: JSON.stringify({ concluida })
        });
    },

    async excluirMeta(id) {
        return await this.request(`/metas/${id}`, {
            method: "DELETE"
        });
    }
};