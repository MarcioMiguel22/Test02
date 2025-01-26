from urllib import request
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Resposta
from django.views.decorators.csrf import csrf_exempt
import json


print(f"Dados recebidos no endpoint: {request.body}")


@csrf_exempt
def salvar_respostas(request):
    """
    Endpoint para salvar respostas enviadas via POST.
    """
    if request.method == 'POST':
        try:
            # Carregar e validar os dados do corpo da requisição
            data = json.loads(request.body)
            numero_instalacao = data.get('numeroInstalacao')
            respostas = data.get('respostas', {})
            comentarios = data.get('comentarios', {})
            tecnico = data.get('tecnico')

            # Verificar se os campos obrigatórios foram fornecidos
            if not numero_instalacao or not tecnico or not respostas:
                return JsonResponse({'status': 'error', 'message': 'Dados obrigatórios ausentes'}, status=400)

            # Salvar as respostas no banco de dados
            for pergunta_id, resposta in respostas.items():
                comentario = comentarios.get(pergunta_id, "")
                Resposta.objects.create(
                    numero_instalacao=numero_instalacao,
                    pergunta_id=pergunta_id,
                    resposta=resposta,
                    comentario=comentario,
                    tecnico=tecnico
                )

            return JsonResponse({'status': 'success', 'message': 'Respostas salvas com sucesso!'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Formato JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Erro interno: {str(e)}'}, status=500)

    # Retornar erro se o método não for POST
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def obter_respostas(request, numero_instalacao):
    """
    Endpoint para obter respostas relacionadas a uma instalação específica.
    """
    if request.method == 'GET':
        try:
            # Buscar respostas no banco de dados
            respostas = Resposta.objects.filter(numero_instalacao=numero_instalacao)

            # Verificar se existem respostas
            if not respostas.exists():
                return JsonResponse({'status': 'error', 'message': 'Nenhuma resposta encontrada'}, status=404)

            # Construir a resposta JSON com os dados
            data = {
                'respostas': {resposta.pergunta_id: resposta.resposta for resposta in respostas},
                'comentarios': {resposta.pergunta_id: resposta.comentario for resposta in respostas},
                'tecnico': respostas.first().tecnico if respostas.exists() else ""
            }

            return JsonResponse({'status': 'success', 'data': data})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Erro interno: {str(e)}'}, status=500)

    # Retornar erro se o método não for GET
    return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def obter_todas_respostas(request):
    """
    Endpoint para obter todas as respostas.
    """
    if request.method == 'GET':
        try:
            # Buscar todas as respostas no banco de dados
            respostas = Resposta.objects.all()

            # Verificar se existem respostas
            if not respostas.exists():
                return JsonResponse({'status': 'error', 'message': 'Nenhuma resposta encontrada'}, status=404)

            # Construir a resposta JSON com os dados
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

            return JsonResponse({'status': 'success', 'data': data})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Erro interno: {str(e)}'}, status=500)

    # Retornar erro se o método não for GET
    return HttpResponseNotAllowed(['GET'])
