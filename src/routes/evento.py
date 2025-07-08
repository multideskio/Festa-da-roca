from flask import Blueprint, request, jsonify
from src.models.festa_junina import db, Evento, Barraca, ItemCardapio
from datetime import datetime

evento_bp = Blueprint('evento', __name__)

@evento_bp.route('/eventos', methods=['GET'])
def get_eventos():
    eventos = Evento.query.all()
    return jsonify([evento.to_dict() for evento in eventos])

@evento_bp.route('/eventos', methods=['POST'])
def create_evento():
    data = request.get_json()
    
    try:
        data_evento = datetime.strptime(data['data_evento'], '%Y-%m-%d').date()
        
        evento = Evento(
            nome=data['nome'],
            data_evento=data_evento,
            local=data['local'],
            objetivo=data.get('objetivo', ''),
            publico_alvo=data.get('publico_alvo', ''),
            status=data.get('status', 'planejamento')
        )
        
        db.session.add(evento)
        db.session.commit()
        
        return jsonify(evento.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@evento_bp.route('/eventos/<int:evento_id>', methods=['GET'])
def get_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)
    return jsonify(evento.to_dict())

@evento_bp.route('/eventos/<int:evento_id>', methods=['PUT'])
def update_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)
    data = request.get_json()
    
    try:
        if 'nome' in data:
            evento.nome = data['nome']
        if 'data_evento' in data:
            evento.data_evento = datetime.strptime(data['data_evento'], '%Y-%m-%d').date()
        if 'local' in data:
            evento.local = data['local']
        if 'objetivo' in data:
            evento.objetivo = data['objetivo']
        if 'publico_alvo' in data:
            evento.publico_alvo = data['publico_alvo']
        if 'status' in data:
            evento.status = data['status']
        
        db.session.commit()
        return jsonify(evento.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@evento_bp.route('/eventos/<int:evento_id>/barracas', methods=['GET'])
def get_barracas_evento(evento_id):
    barracas = Barraca.query.filter_by(evento_id=evento_id).all()
    return jsonify([barraca.to_dict() for barraca in barracas])

@evento_bp.route('/eventos/<int:evento_id>/barracas', methods=['POST'])
def create_barraca(evento_id):
    data = request.get_json()
    
    try:
        barraca = Barraca(
            evento_id=evento_id,
            nome=data['nome'],
            descricao=data.get('descricao', ''),
            responsavel=data.get('responsavel', ''),
            ativa=data.get('ativa', True)
        )
        
        db.session.add(barraca)
        db.session.commit()
        
        return jsonify(barraca.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

