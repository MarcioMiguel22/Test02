from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import Resposta
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def salvar_respostas(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        numero_instalacao = data.get('numeroInstalacao')
        respostas = data.get('respostas')
        comentarios = data.get('comentarios')
        tecnico = data.get('tecnico')

        for pergunta_id, resposta in respostas.items():
            comentario = comentarios.get(pergunta_id, "")
            Resposta.objects.create(
                numero_instalacao=numero_instalacao,
                pergunta_id=pergunta_id,
                resposta=resposta,
                comentario=comentario,
                tecnico=tecnico
            )

        return JsonResponse({'status': 'success'})
    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def obter_respostas(request, numero_instalacao):
    if request.method == 'GET':
        respostas = Resposta.objects.filter(numero_instalacao=numero_instalacao)
        data = {
            'respostas': {resposta.pergunta_id: resposta.resposta for resposta in respostas},
            'comentarios': {resposta.pergunta_id: resposta.comentario for resposta in respostas},
            'tecnico': respostas.first().tecnico if respostas.exists() else ""
        }
        return JsonResponse(data)
