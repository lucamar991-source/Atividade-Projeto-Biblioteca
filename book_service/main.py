import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Book Service",
    description="Microsserviço responsável pelo catálogo de livros da biblioteca.",
    version="1.0.0",
)


class LivroBase(BaseModel):
    titulo: str = Field(..., example="O Senhor dos Anéis")
    autor: str = Field(..., example="J.R.R. Tolkien")
    ano: int = Field(..., example=1954)
    disponivel: bool = Field(default=True, example=True)


class LivroCriar(LivroBase):
    pass


class Livro(LivroBase):
    id: int


livros_db: dict[int, Livro] = {
    1: Livro(id=1, titulo="O Senhor dos Anéis", autor="J.R.R. Tolkien", ano=1954, disponivel=True),
    2: Livro(id=2, titulo="Duna", autor="Frank Herbert", ano=1965, disponivel=True),
    3: Livro(id=3, titulo="1984", autor="George Orwell", ano=1949, disponivel=True),
}
proximo_id = 4


@app.get("/livros", response_model=list[Livro], tags=["Livros"])
def listar_livros(disponivel: Optional[bool] = None):
    valores = list(livros_db.values())
    if disponivel is not None:
        valores = [l for l in valores if l.disponivel == disponivel]
    return valores


@app.get("/livros/{livro_id}", response_model=Livro, tags=["Livros"])
def buscar_livro(livro_id: int):
    livro = livros_db.get(livro_id)
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


@app.post("/livros", response_model=Livro, status_code=201, tags=["Livros"])
def criar_livro(dados: LivroCriar):
    global proximo_id
    novo = Livro(id=proximo_id, **dados.model_dump())
    livros_db[proximo_id] = novo
    proximo_id += 1
    return novo


@app.put("/livros/{livro_id}", response_model=Livro, tags=["Livros"])
def atualizar_livro(livro_id: int, dados: LivroBase):
    if livro_id not in livros_db:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    atualizado = Livro(id=livro_id, **dados.model_dump())
    livros_db[livro_id] = atualizado
    return atualizado


@app.delete("/livros/{livro_id}", status_code=204, tags=["Livros"])
def remover_livro(livro_id: int):
    if livro_id not in livros_db:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    del livros_db[livro_id]
    return None