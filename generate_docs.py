"""
GERAR DOCUMENTAÇÃO DA API
=========================
Este script baixa o arquivo openapi.json de um serviço que já está rodando
e salva localmente. Esse arquivo é a "planta" completa da API em formato
padrão (OpenAPI/Swagger): todas as rotas, os campos de cada modelo, os
tipos de dados, os exemplos, os códigos de status possíveis.

Uso:
    python generate_docs.py http://localhost:8001 book-service-openapi.json
    python generate_docs.py http://localhost:8003 loan-service-openapi.json
"""

import json
import sys
import urllib.request


def gerar_documentacao(url_base: str, arquivo_saida: str):
    url = url_base.rstrip("/") + "/openapi.json"
    print(f"Buscando especificação da API em: {url}")
    with urllib.request.urlopen(url) as resposta:
        spec = json.loads(resposta.read())

    with open(arquivo_saida, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)

    print(f"Documentação salva em: {arquivo_saida}")
    print(f"Título da API: {spec.get('info', {}).get('title')}")
    print(f"Rotas encontradas: {list(spec.get('paths', {}).keys())}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python generate_docs.py <url_do_servico> <arquivo_saida.json>")
        print("Exemplo: python generate_docs.py http://localhost:8001 book-service-openapi.json")
        sys.exit(1)

    gerar_documentacao(sys.argv[1], sys.argv[2])