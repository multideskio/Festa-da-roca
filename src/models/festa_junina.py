from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    data_evento = db.Column(db.Date, nullable=False)
    local = db.Column(db.String(200), nullable=False)
    objetivo = db.Column(db.Text)
    publico_alvo = db.Column(db.Text)
    status = db.Column(db.String(50), default='planejamento')  # planejamento, ativo, finalizado
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'data_evento': self.data_evento.isoformat() if self.data_evento else None,
            'local': self.local,
            'objetivo': self.objetivo,
            'publico_alvo': self.publico_alvo,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Barraca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    responsavel = db.Column(db.String(100))
    ativa = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    evento = db.relationship('Evento', backref=db.backref('barracas', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'evento_id': self.evento_id,
            'nome': self.nome,
            'descricao': self.descricao,
            'responsavel': self.responsavel,
            'ativa': self.ativa,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ItemCardapio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barraca_id = db.Column(db.Integer, db.ForeignKey('barraca.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    preco_fichas = db.Column(db.Integer, nullable=False)  # quantidade de fichas necessárias
    disponivel = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    barraca = db.relationship('Barraca', backref=db.backref('itens_cardapio', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'barraca_id': self.barraca_id,
            'nome': self.nome,
            'preco_fichas': self.preco_fichas,
            'disponivel': self.disponivel,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class VendaFicha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id'), nullable=False)
    quantidade_fichas = db.Column(db.Integer, nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)  # valor em reais de cada ficha
    valor_total = db.Column(db.Float, nullable=False)
    responsavel = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    evento = db.relationship('Evento', backref=db.backref('vendas_fichas', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'evento_id': self.evento_id,
            'quantidade_fichas': self.quantidade_fichas,
            'valor_unitario': self.valor_unitario,
            'valor_total': self.valor_total,
            'responsavel': self.responsavel,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

class VendaBarraca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barraca_id = db.Column(db.Integer, db.ForeignKey('barraca.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item_cardapio.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    fichas_recebidas = db.Column(db.Integer, nullable=False)
    responsavel = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    barraca = db.relationship('Barraca', backref=db.backref('vendas', lazy=True))
    item = db.relationship('ItemCardapio', backref=db.backref('vendas', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'barraca_id': self.barraca_id,
            'item_id': self.item_id,
            'quantidade': self.quantidade,
            'fichas_recebidas': self.fichas_recebidas,
            'responsavel': self.responsavel,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'item_nome': self.item.nome if self.item else None,
            'barraca_nome': self.barraca.nome if self.barraca else None
        }

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # admin, operador_caixa, responsavel_barraca
    barraca_id = db.Column(db.Integer, db.ForeignKey('barraca.id'), nullable=True)  # apenas para responsáveis de barraca
    ativo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    barraca = db.relationship('Barraca', backref=db.backref('responsaveis', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'tipo': self.tipo,
            'barraca_id': self.barraca_id,
            'barraca_nome': self.barraca.nome if self.barraca else None,
            'ativo': self.ativo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

