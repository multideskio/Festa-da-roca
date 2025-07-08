from flask import Blueprint, request, jsonify
from src.models.festa_junina import db, VendaFicha, Evento
from sqlalchemy import func
from datetime import datetime

venda_bp = Blueprint('venda', __name__)

@venda_bp.route('/eventos/<int:evento_id>/vendas-fichas', methods=['GET'])
def get_vendas_fichas(evento_id):
    vendas = VendaFicha.query.filter_by(evento_id=evento_id).order_by(VendaFicha.timestamp.desc()).all()
    return jsonify([venda.to_dict() for venda in vendas])

@venda_bp.route('/eventos/<int:evento_id>/vendas-fichas', methods=['POST'])
def registrar_venda_ficha(evento_id):
    data = request.get_json()
    
    try:
        venda = VendaFicha(
            evento_id=evento_id,
            quantidade_fichas=data['quantidade_fichas'],
            valor_unitario=data['valor_unitario'],
            valor_total=data['quantidade_fichas'] * data['valor_unitario'],
            responsavel=data.get('responsavel', '')
        )
        
        db.session.add(venda)
        db.session.commit()
        
        return jsonify(venda.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@venda_bp.route('/eventos/<int:evento_id>/relatorio-caixa', methods=['GET'])
def get_relatorio_caixa(evento_id):
    # Total arrecadado
    total_arrecadado = db.session.query(func.sum(VendaFicha.valor_total)).filter_by(evento_id=evento_id).scalar() or 0
    
    # Total de fichas vendidas
    total_fichas_vendidas = db.session.query(func.sum(VendaFicha.quantidade_fichas)).filter_by(evento_id=evento_id).scalar() or 0
    
    # Vendas por valor de ficha
    vendas_por_valor = db.session.query(
        VendaFicha.valor_unitario,
        func.sum(VendaFicha.quantidade_fichas).label('total_fichas'),
        func.sum(VendaFicha.valor_total).label('total_valor')
    ).filter_by(evento_id=evento_id).group_by(VendaFicha.valor_unitario).all()
    
    relatorio = {
        'evento_id': evento_id,
        'total_arrecadado': float(total_arrecadado),
        'total_fichas_vendidas': total_fichas_vendidas,
        'vendas_por_valor': [
            {
                'valor_unitario': float(venda[0]),
                'total_fichas': venda[1],
                'total_valor': float(venda[2])
            }
            for venda in vendas_por_valor
        ]
    }
    
    return jsonify(relatorio)

@venda_bp.route('/eventos/<int:evento_id>/relatorio-geral', methods=['GET'])
def get_relatorio_geral(evento_id):
    from src.models.festa_junina import VendaBarraca, Barraca
    
    # Relatório do caixa central
    total_arrecadado = db.session.query(func.sum(VendaFicha.valor_total)).filter_by(evento_id=evento_id).scalar() or 0
    total_fichas_vendidas = db.session.query(func.sum(VendaFicha.quantidade_fichas)).filter_by(evento_id=evento_id).scalar() or 0
    
    # Relatório por barraca
    barracas_relatorio = []
    barracas = Barraca.query.filter_by(evento_id=evento_id).all()
    
    for barraca in barracas:
        total_fichas_barraca = db.session.query(func.sum(VendaBarraca.fichas_recebidas)).filter_by(barraca_id=barraca.id).scalar() or 0
        
        barracas_relatorio.append({
            'barraca_id': barraca.id,
            'barraca_nome': barraca.nome,
            'total_fichas_recebidas': total_fichas_barraca,
            'responsavel': barraca.responsavel
        })
    
    # Total de fichas recebidas por todas as barracas
    total_fichas_barracas = sum([b['total_fichas_recebidas'] for b in barracas_relatorio])
    
    relatorio_geral = {
        'evento_id': evento_id,
        'caixa_central': {
            'total_arrecadado': float(total_arrecadado),
            'total_fichas_vendidas': total_fichas_vendidas
        },
        'barracas': barracas_relatorio,
        'resumo': {
            'total_fichas_vendidas': total_fichas_vendidas,
            'total_fichas_recebidas_barracas': total_fichas_barracas,
            'diferenca_fichas': total_fichas_vendidas - total_fichas_barracas
        }
    }
    
    return jsonify(relatorio_geral)

