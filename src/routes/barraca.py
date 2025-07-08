from flask import Blueprint, request, jsonify
from src.models.festa_junina import db, Barraca, ItemCardapio, VendaBarraca
from sqlalchemy import func

barraca_bp = Blueprint('barraca', __name__)

@barraca_bp.route('/barracas/<int:barraca_id>', methods=['GET'])
def get_barraca(barraca_id):
    barraca = Barraca.query.get_or_404(barraca_id)
    return jsonify(barraca.to_dict())

@barraca_bp.route('/barracas/<int:barraca_id>', methods=['PUT'])
def update_barraca(barraca_id):
    barraca = Barraca.query.get_or_404(barraca_id)
    data = request.get_json()
    
    try:
        if 'nome' in data:
            barraca.nome = data['nome']
        if 'descricao' in data:
            barraca.descricao = data['descricao']
        if 'responsavel' in data:
            barraca.responsavel = data['responsavel']
        if 'ativa' in data:
            barraca.ativa = data['ativa']
        
        db.session.commit()
        return jsonify(barraca.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@barraca_bp.route('/barracas/<int:barraca_id>/cardapio', methods=['GET'])
def get_cardapio_barraca(barraca_id):
    itens = ItemCardapio.query.filter_by(barraca_id=barraca_id).all()
    return jsonify([item.to_dict() for item in itens])

@barraca_bp.route('/barracas/<int:barraca_id>/cardapio', methods=['POST'])
def add_item_cardapio(barraca_id):
    data = request.get_json()
    
    try:
        item = ItemCardapio(
            barraca_id=barraca_id,
            nome=data['nome'],
            preco_fichas=data['preco_fichas'],
            disponivel=data.get('disponivel', True)
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify(item.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@barraca_bp.route('/cardapio/<int:item_id>', methods=['PUT'])
def update_item_cardapio(item_id):
    item = ItemCardapio.query.get_or_404(item_id)
    data = request.get_json()
    
    try:
        if 'nome' in data:
            item.nome = data['nome']
        if 'preco_fichas' in data:
            item.preco_fichas = data['preco_fichas']
        if 'disponivel' in data:
            item.disponivel = data['disponivel']
        
        db.session.commit()
        return jsonify(item.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@barraca_bp.route('/barracas/<int:barraca_id>/vendas', methods=['GET'])
def get_vendas_barraca(barraca_id):
    vendas = VendaBarraca.query.filter_by(barraca_id=barraca_id).all()
    return jsonify([venda.to_dict() for venda in vendas])

@barraca_bp.route('/barracas/<int:barraca_id>/vendas', methods=['POST'])
def registrar_venda_barraca(barraca_id):
    data = request.get_json()
    
    try:
        venda = VendaBarraca(
            barraca_id=barraca_id,
            item_id=data['item_id'],
            quantidade=data['quantidade'],
            fichas_recebidas=data['fichas_recebidas'],
            responsavel=data.get('responsavel', '')
        )
        
        db.session.add(venda)
        db.session.commit()
        
        return jsonify(venda.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@barraca_bp.route('/barracas/<int:barraca_id>/relatorio', methods=['GET'])
def get_relatorio_barraca(barraca_id):
    # Total de fichas recebidas
    total_fichas = db.session.query(func.sum(VendaBarraca.fichas_recebidas)).filter_by(barraca_id=barraca_id).scalar() or 0
    
    # Vendas por item
    vendas_por_item = db.session.query(
        ItemCardapio.nome,
        func.sum(VendaBarraca.quantidade).label('total_quantidade'),
        func.sum(VendaBarraca.fichas_recebidas).label('total_fichas')
    ).join(VendaBarraca).filter(VendaBarraca.barraca_id == barraca_id).group_by(ItemCardapio.id).all()
    
    relatorio = {
        'barraca_id': barraca_id,
        'total_fichas_recebidas': total_fichas,
        'vendas_por_item': [
            {
                'item_nome': item[0],
                'total_quantidade': item[1],
                'total_fichas': item[2]
            }
            for item in vendas_por_item
        ]
    }
    
    return jsonify(relatorio)

