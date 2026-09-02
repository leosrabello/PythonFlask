from marshmallow import Schema, fields, pre_load, validate


class LivroSchema(Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200, error="titulo deve ter entre 1 e 200 caracteres"),
    )
    ano = fields.Int(required=True, validate=validate.Range(min=1, max=9999))
    genero = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=80, error="genero deve ter entre 1 e 80 caracteres"),
    )
    autor_id = fields.Int(required=True, validate=validate.Range(min=1))

    @pre_load
    def limpa_espacos(self, data, **kwargs):
        if not isinstance(data, dict):
            return data
        return {
            chave: (valor.strip() if isinstance(valor, str) else valor)
            for chave, valor in data.items()
        }


livro_schema = LivroSchema()
livros_schema = LivroSchema(many=True)
