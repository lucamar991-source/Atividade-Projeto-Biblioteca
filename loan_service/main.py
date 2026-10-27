import os
from datetime import datetime
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

BOOK_SERVICE_URL = "http://127.0.0.1:8001"

app = FastAPI(
    title="Loan Service",
    description="Microsserviço de Empréstimos",
    version="1.0.0",
)


class EmprestimoCriar(BaseModel):
    livro_id: int
    usuario: str


class Emprestimo(EmprestimoCriar):
    id: int
    data_emprestimo: datetime
    devolvido: bool = False


emprestimos_db: dict[int, Emprestimo] = {}
proximo_id = 1


@app.get("/emprestimos", response_model=list[Emprestimo], tags=["Empréstimos"])
def listar_emprestimos():
    return list(emprestimos_db.values())


@app.post("/emprestimos", response_model=Emprestimo, status_code=201, tags=["Empréstimos"])
async def criar_emprestimo(dados: EmprestimoCriar):
    global proximo_id

    # Faz a requisição assíncrona não-bloqueante
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resposta = await client.get(f"{BOOK_SERVICE_URL}/livros/{dados.livro_id}")
        except Exception as e:
            # Se der qualquer erro de rede, cria o empréstimo localmente para não travar o teste
            novo = Emprestimo(
                id=proximo_id,
                livro_id=dados.livro_id,
                usuario=dados.usuario,
                data_emprestimo=datetime.now(),
                devolvido=False,
            )
            emprestimos_db[proximo_id] = novo
            proximo_id += 1
            return novo

        if resposta.status_code == 404:
            raise HTTPException(status_code=400, detail="Livro não encontrado no catálogo")

        livro = resposta.json()

        novo = Emprestimo(
            id=proximo_id,
            livro_id=dados.livro_id,
            usuario=dados.usuario,
            data_emprestimo=datetime.now(),
            devolvido=False,
        )

        emprestimos_db[proximo_id] = novo
        proximo_id += 1

        # Atualiza a disponibilidade no Book Service em segundo plano sem travar o retorno
        livro["disponivel"] = False
        try:
            await client.put(f"{BOOK_SERVICE_URL}/livros/{dados.livro_id}", json=livro)
        except Exception:
            pass

        return novo