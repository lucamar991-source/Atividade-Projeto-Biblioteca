from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="MOCK do Book Service",
    description="Versão falsa do Book Service, usada apenas para testes.",
    version="mock",
)


class Livro(BaseModel):
    id: int
    titulo: str
    autor: str
    ano: int
    disponivel: bool


livros_mock: dict[int, Livro] = {
    1: Livro(id=1, titulo="Livro Mockado A", autor="Autor Fake", ano=2000, disponivel=True),
    99: Livro(id=99, titulo="Livro Indisponivel", autor="Autor Fake", ano=2010, disponivel=False),
}


@app.get("/livros/{livro_id}", response_model=Livro, tags=["Mock"])
def buscar_livro_mock(livro_id: int):
    livro = livros_mock.get(livro_id)
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado (mock)")
    return livro


@app.put("/livros/{livro_id}", response_model=Livro, tags=["Mock"])
def atualizar_livro_mock(livro_id: int, dados: Livro):
    livros_mock[livro_id] = dados
    return dados