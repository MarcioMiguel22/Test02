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
    Endpoint para salvar respostas enviadas via POST.
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

            # Salvar cada resposta no banco de dados
            for pergunta_id, resposta in respostas.items():
                comentario = comentarios.get(pergunta_id, "")
                Resposta.objects.create(
                    numero_instalacao=numero_instalacao,
                    pergunta_id=pergunta_id,
                    resposta=resposta,
                    comentario=comentario,
                    tecnico=tecnico
                )
            logger.info(f"Respostas salvas para a instalação {numero_instalacao}.")
            return JsonResponse({'status': 'success', 'message': 'Respostas salvas com sucesso!'})

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
                'tecnico': respostas.first().tecnico
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
