
import sqlite3
from pathlib import Path

# Localiza o banco na mesma pasta deste script.
PASTA_PROJETO = Path(__file__).resolve().parent
CAMINHO_BANCO = PASTA_PROJETO / "nutrihub.db"


def migrar_relacionamentos():
    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        # Evita iniciar a migração se houver registros órfãos.
        conexao.execute("PRAGMA foreign_keys = ON")

        for tabela in ["questionarios", "objetivos_nutricionais"]:
            orfaos = conexao.execute(
                f"""
                SELECT COUNT(*)
                FROM {tabela} AS filho
                LEFT JOIN usuarios AS usuario
                    ON filho.usuario_id = usuario.id
                WHERE usuario.id IS NULL
                """
            ).fetchone()[0]

            if orfaos > 0:
                raise RuntimeError(
                    f"A tabela {tabela} possui {orfaos} registro(s) "
                    "sem usuário correspondente."
                )

        # A alteração da configuração deve ocorrer fora da transação.
        conexao.execute("PRAGMA foreign_keys = OFF")
        conexao.execute("BEGIN")

        # Reconstrói a tabela de questionários.
        conexao.execute("""
            CREATE TABLE questionarios_novo (
                id INTEGER NOT NULL PRIMARY KEY,
                usuario_id INTEGER NOT NULL UNIQUE,
                idade INTEGER NOT NULL,
                peso FLOAT NOT NULL,
                altura FLOAT NOT NULL,
                nivel_atividade VARCHAR NOT NULL,
                restricao_alimentar VARCHAR NOT NULL,
                refeicoes_por_dia INTEGER NOT NULL,
                FOREIGN KEY (usuario_id)
                    REFERENCES usuarios(id)
                    ON DELETE CASCADE
            )
        """)

        conexao.execute("""
            INSERT INTO questionarios_novo (
                id, usuario_id, idade, peso, altura,
                nivel_atividade, restricao_alimentar,
                refeicoes_por_dia
            )
            SELECT
                id, usuario_id, idade, peso, altura,
                nivel_atividade, restricao_alimentar,
                refeicoes_por_dia
            FROM questionarios
        """)

        # Reconstrói a tabela de objetivos nutricionais.
        conexao.execute("""
            CREATE TABLE objetivos_nutricionais_novo (
                id INTEGER NOT NULL PRIMARY KEY,
                usuario_id INTEGER NOT NULL UNIQUE,
                objetivo VARCHAR NOT NULL,
                FOREIGN KEY (usuario_id)
                    REFERENCES usuarios(id)
                    ON DELETE CASCADE
            )
        """)

        conexao.execute("""
            INSERT INTO objetivos_nutricionais_novo (
                id, usuario_id, objetivo
            )
            SELECT id, usuario_id, objetivo
            FROM objetivos_nutricionais
        """)

        # Substitui as tabelas antigas pelas novas.
        conexao.execute("DROP TABLE questionarios")
        conexao.execute("ALTER TABLE questionarios_novo RENAME TO questionarios")

        conexao.execute("DROP TABLE objetivos_nutricionais")
        conexao.execute(
            "ALTER TABLE objetivos_nutricionais_novo "
            "RENAME TO objetivos_nutricionais"
        )

        # Recria os índices explícitos das colunas id.
        conexao.execute("""
            CREATE INDEX ix_questionarios_id
            ON questionarios (id)
        """)

        conexao.execute("""
            CREATE INDEX ix_objetivos_nutricionais_id
            ON objetivos_nutricionais (id)
        """)

        conexao.commit()

        # Reativa e verifica as chaves estrangeiras.
        conexao.execute("PRAGMA foreign_keys = ON")

        problemas = conexao.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

        if problemas:
            raise RuntimeError(
                f"Foram encontradas violações de chaves estrangeiras: "
                f"{problemas}"
            )

        print("Migração concluída com sucesso!")
        print("As duas tabelas agora usam ON DELETE CASCADE.")

    except Exception:
        if conexao.in_transaction:
            conexao.rollback()

        raise

    finally:
        # Garante que a conexão seja fechada.
        conexao.close()


if __name__ == "__main__":
    migrar_relacionamentos()
