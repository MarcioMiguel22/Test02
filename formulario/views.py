from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Resposta
import json
import logging

# Configuração de log
logger = logging.getLogger(__name__)

@csrf_exempt
def salvar_respostas(request):
    """
    Endpoint para salvar ou atualizar respostas enviadas via POST.
    """
    if request.method == 'POST':
        try:
            logger.info("Requisição recebida para salvar respostas.")
            data = json.loads(request.body)

            # Extrair dados da requisição
            numero_instalacao = data.get('numeroInstalacao')
            respostas = data.get('respostas', {})
            comentarios = data.get('comentarios', {})
            tecnico = data.get('tecnico')

            # Validar dados obrigatórios
            if not numero_instalacao or not tecnico or not respostas:
                logger.warning("Dados obrigatórios ausentes.")
                return JsonResponse({'status': 'error', 'message': 'Dados obrigatórios ausentes'}, status=400)

            # Deletar dados existentes antes de salvar novos (Chama a função diretamente)
            deletar_respostas(request, numero_instalacao)

            # Salvar ou atualizar cada resposta no banco de dados
            for pergunta_id, resposta in respostas.items():
                comentario = comentarios.get(pergunta_id, "")
                Resposta.objects.update_or_create(
                    numero_instalacao=numero_instalacao,
                    pergunta_id=pergunta_id,
                    defaults={
                        "resposta": resposta,
                        "comentario": comentario,
                        "tecnico": tecnico
                    }
                )
            logger.info(f"Respostas salvas ou atualizadas para a instalação {numero_instalacao}.")
            return JsonResponse({'status': 'success', 'message': 'Respostas salvas ou atualizadas com sucesso!'})

        except json.JSONDecodeError:
            logger.error("Erro no formato JSON recebido.")
            return JsonResponse({'status': 'error', 'message': 'Formato JSON inválido'}, status=400)
        except Exception as e:
            logger.error(f"Erro interno ao salvar respostas: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Erro interno: {str(e)}'}, status=500)

    logger.warning("Método HTTP não permitido.")
    return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def obter_respostas(request, numero_instalacao):
    """
    Endpoint para obter respostas relacionadas a uma instalação específica.
    """
    if request.method == 'GET':
        try:
            logger.info(f"Requisição para obter respostas da instalação {numero_instalacao}.")
            respostas = Resposta.objects.filter(numero_instalacao=numero_instalacao)

            if not respostas.exists():
                logger.warning(f"Nenhuma resposta encontrada para a instalação {numero_instalacao}.")
                return JsonResponse({'status': 'error', 'message': 'Nenhuma resposta encontrada'}, status=404)

            # Construir resposta JSON
            data = {
                'respostas': {resposta.pergunta_id: resposta.resposta for resposta in respostas},
                'comentarios': {resposta.pergunta_id: resposta.comentario for resposta in respostas},
                'tecnico': respostas.first().tecnico,
                'data_ultima_atualizacao': respostas.latest('data').data
            }
            logger.info(f"Respostas obtidas com sucesso para a instalação {numero_instalacao}.")
            return JsonResponse({'status': 'success', 'data': data})

        except Exception as e:
            logger.error(f"Erro interno ao obter respostas: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Erro interno: {str(e)}'}, status=500)

    logger.warning("Método HTTP não permitido.")
    return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def obter_todas_respostas(request):
    """
    Endpoint para obter todas as respostas.
    """
    if request.method == 'GET':
        try:
            logger.info("Requisição para obter todas as respostas.")
            respostas = Resposta.objects.all()

            if not respostas.exists():
                logger.warning("Nenhuma resposta encontrada.")
                return JsonResponse({'status': 'error', 'message': 'Nenhuma resposta encontrada'}, status=404)

            # Construir resposta JSON
            data = [
                {
                    'numero_instalacao': resposta.numero_instalacao,
                    'pergunta_id': resposta.pergunta_id,
                    'resposta': resposta.resposta,
                    'comentario': resposta.comentario,
                    'tecnico': resposta.tecnico,
                    'data': resposta.data
                }
                for resposta in respostas
            ]
            logger.info("Todas as respostas foram obtidas com sucesso.")
            return JsonResponse({'status': 'success', 'data': data})

        except Exception as e:
            logger.error(f"Erro interno ao obter todas as respostas: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Erro interno: {str(e)}'}, status=500)

    logger.warning("Método HTTP não permitido.")
    return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def criar_instalacao(request):
    """
    Endpoint para criar uma nova instalação.
    """
    if request.method == 'POST':
        try:
            logger.info("Requisição para criar uma nova instalação recebida.")
            data = json.loads(request.body)

            # Obter número da instalação
            numero_instalacao = data.get('numeroInstalacao')

            if not numero_instalacao:
                logger.warning("Número da instalação ausente.")
                return JsonResponse({'status': 'error', 'message': 'Número da instalação é obrigatório.'}, status=400)

            # Verificar se já existe uma instalação com o mesmo número
            if Resposta.objects.filter(numero_instalacao=numero_instalacao).exists():
                logger.warning(f"Instalação {numero_instalacao} já existe.")
                return JsonResponse({'status': 'error', 'message': 'Instalação já existe.'}, status=409)

            # Criar um registro inicial (pode ser vazio) para a instalação
            Resposta.objects.create(
                numero_instalacao=numero_instalacao,
                pergunta_id=0,  # Pode ser ajustado dependendo da lógica
                resposta="",
                comentario="",
                tecnico="Técnico padrão"
            )

            logger.info(f"Nova instalação {numero_instalacao} criada com sucesso.")
            return JsonResponse({'status': 'success', 'message': 'Nova instalação criada com sucesso.'}, status=201)

        except json.JSONDecodeError:
            logger.error("Erro no formato JSON recebido.")
            return JsonResponse({'status': 'error', 'message': 'Formato JSON inválido'}, status=400)
        except Exception as e:
            logger.error(f"Erro interno ao criar instalação: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Erro interno: {str(e)}'}, status=500)

    logger.warning("Método HTTP não permitido.")
    return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def deletar_respostas(request, numero_instalacao):
    """
    Endpoint para deletar respostas relacionadas a uma instalação específica.
    """
    if request.method == 'DELETE':
        try:
            logger.info(f"Requisição para deletar respostas da instalação {numero_instalacao}.")
            
            # Filtrar e deletar as respostas associadas ao número de instalação
            respostas = Resposta.objects.filter(numero_instalacao=numero_instalacao)
            
            if not respostas.exists():
                logger.warning(f"Nenhuma resposta encontrada para a instalação {numero_instalacao}.")
                return JsonResponse({'status': 'error', 'message': 'Nenhuma resposta encontrada'}, status=404)
            
            respostas.delete()  # Deletar todos os registros
            logger.info(f"Respostas da instalação {numero_instalacao} deletadas com sucesso.")
            return JsonResponse({'status': 'success', 'message': 'Respostas deletadas com sucesso!'})
        
        except Exception as e:
            logger.error(f"Erro interno ao deletar respostas: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Erro interno: {str(e)}'}, status=500)
    
    logger.warning("Método HTTP não permitido.")
    return HttpResponseNotAllowed(['DELETE'])
