class Usuario: # Nossa classe usuario

    def __init__(self, nome, email, senha): # Nossos atributos
        self.nome = nome
        self.email = email
        self.senha = senha

                                       
    def alterar_email(self, novo_email): # Nossos metodos 
        self.email = novo_email

    def validar_senha(self, senha):
        return self.senha == senha