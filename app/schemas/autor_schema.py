from marshmallow import Schema, fields, pre_load, validate


class AutorSchema(Schema):
    """Valida a entrada e serializa a saída de Autor.

    Campos desconhecidos são rejeitados (comportamento padrão do Marshmallow),
    então um POST com {"nomee": "..."} volta 422 em vez de gravar lixo no banco.

    Observação sobre os campos opcionais: eles NÃO têm ``load_default``. Assim,
    quando a chave não vem no corpo, ela simplesmente não aparece no resultado
    do ``load`` — o que é o que faz o PATCH (``partial=True``) conseguir
    distinguir "não mandou o campo" de "mandou o campo como null".
    """

    id = fields.Int(dump_only=True)
    nome = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=120, error="nome deve ter entre 2 e 120 caracteres"),
    )
    nacionalidade = fields.Str(
        allow_none=True,
        validate=validate.Length(max=60, error="nacionalidade deve ter no maximo 60 caracteres"),
    )
    data_nascimento = fields.Date(allow_none=True)  # formato ISO: AAAA-MM-DD
    criado_em = fields.DateTime(dump_only=True)

    @pre_load
    def limpa_espacos(self, data, **kwargs):
        """Tira espaços das pontas para " Machado " não virar um nome diferente."""
        if not isinstance(data, dict):
            return data
        return {
            chave: (valor.strip() if isinstance(valor, str) else valor)
            for chave, valor in data.items()
        }


# Instâncias reaproveitadas pelas rotas.
autor_schema = AutorSchema()
autores_schema = AutorSchema(many=True)
