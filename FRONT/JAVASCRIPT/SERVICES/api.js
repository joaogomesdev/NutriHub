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
    }
};