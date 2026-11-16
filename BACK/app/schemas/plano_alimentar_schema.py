from pydantic import BaseModel

    # Define como os dados serão recebidos para o nosso plano alimentar

class PlanoAlimentarSchema(BaseModel):
    dieta_titulo: str
    dieta_descricao: str

    rotina_titulo: str
    rotina_descricao: str