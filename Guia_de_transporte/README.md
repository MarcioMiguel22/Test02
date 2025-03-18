# Guia de Transporte

## Descrição
Um sistema de gerenciamento de guias de transporte desenvolvido com Django e Django REST Framework. Esta aplicação permite criar, visualizar, atualizar e excluir registros de itens transportados, mantendo um controle detalhado sobre a movimentação de mercadorias.

## Características Principais
- API RESTful completa
- Gerenciamento de guias de transporte
- Controle de itens transportados
- Tracking de itens em falta
- Suporte para imagens (Base64)
- Interface administrativa personalizada
- Logging detalhado para debugging

## Tecnologias Utilizadas
- Django
- Django REST Framework
- PostgreSQL (em produção)
- JWT para autenticação

## Instalação

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passos para Instalação
1. Clone o repositório
```
git clone <url-do-repositorio>
cd Test02
```

2. Crie um ambiente virtual e ative-o
```
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências
```
pip install -r requirements.txt
```

4. Execute as migrações
```
python manage.py migrate
```

5. Crie um superusuário (admin)
```
python manage.py createsuperuser
```

6. Inicie o servidor
```
python manage.py runserver
```

## Estrutura do Projeto
- `models.py`: Define os modelos de dados para GuiaDeTransporte e TransportItem
- `views.py`: Contém as classes de visualização da API
- `serializers.py`: Responsável pela serialização/deserialização dos dados
- `urls.py`: Define os endpoints da API
- `admin.py`: Configuração da interface administrativa

## API Endpoints

### Guia de Transporte
- `GET /guias/` - Lista todas as guias de transporte
- `POST /guias/` - Cria uma nova guia de transporte
- `GET /guias/{id}/` - Obtém detalhes de uma guia específica
- `PUT /guias/{id}/` - Atualiza uma guia existente
- `DELETE /guias/{id}/` - Remove uma guia existente

### Itens de Transporte
- `GET /transport-items/` ou `/guiaderemeca/` - Lista todos os itens de transporte
- `POST /transport-items/` ou `/guiaderemeca/` - Cria um novo item de transporte
- `GET /transport-items/{id}/` ou `/guiaderemeca/{id}/` - Obtém detalhes de um item específico
- `PUT /transport-items/{id}/` ou `/guiaderemeca/{id}/` - Atualiza um item existente
- `DELETE /transport-items/{id}/` ou `/guiaderemeca/{id}/` - Remove um item existente

## Sistema de Verificação de Quantidades

O sistema possui um mecanismo avançado para verificação e controle de quantidades:

### Campos de Quantidade
- `quantidade`: Quantidade conforme a guia de transporte
- `quantidade_total`: Quantidade real encontrada na carrinha/veículo

### Cálculo Automático de Faltas
- O campo `em_falta` é calculado automaticamente como a diferença entre `quantidade` e `quantidade_total` quando a quantidade real é menor que a da guia.
- Quando há itens em falta (quantidade_total < quantidade), é obrigatório fornecer uma justificativa no campo `notas`.

### Validação de Dados
- O sistema bloqueia a criação/atualização de registros com itens em falta sem a devida justificativa.
- Uma mensagem de erro específica é retornada quando faltar justificativa: "É necessário justificar os itens em falta nas notas."

### Rastreabilidade
- O campo `username` e `current_user` registram quem criou/atualizou cada item, permitindo auditoria completa do processo.

## Implementação Backend

### Detalhes de API e Exemplos

#### GuiaDeTransporte API

**Lista de Guias (GET /guias/)**
- Retorna: Lista paginada de guias
- Exemplo de resposta:
```json
[
  {
    "id": 1,
    "item": "Caixa 01",
    "descricao": "Caixa com produtos eletrônicos",
    "em_falta": "2",
    "quantidade": 10,
    "notas": "Frágil, manusear com cuidado",
    "total": "500",
    "created_at": "2023-06-15T14:30:00Z",
    "updated_at": "2023-06-15T14:30:00Z"
  },
  {
    "id": 2,
    "item": "Pacote 02",
    "descricao": "Documentos",
    "em_falta": null,
    "quantidade": 1,
    "notas": "Entregar em mãos",
    "total": "50",
    "created_at": "2023-06-16T09:15:00Z",
    "updated_at": "2023-06-16T09:15:00Z"
  }
]
```

**Criar Nova Guia (POST /guias/)**
- Payload necessário:
```json
{
  "item": "Nome do Item",
  "descricao": "Descrição detalhada",
  "quantidade": 10,              // Quantidade conforme a guia
  "quantidade_total": 8,         // Quantidade real encontrada
  "notas": "Justificativa para os 2 itens em falta: danificados durante transporte",
  "unidade": "UN",
  "total": "100"
}
```
- Campos obrigatórios: `item`, `descricao`, `quantidade`, `quantidade_total`
- Campo `em_falta` é calculado automaticamente
- Se houver itens em falta (quantidade_total < quantidade), o campo `notas` torna-se obrigatório

#### TransportItem API

**Lista de Itens (GET /transport-items/ ou /guiaderemeca/)**
- Retorna: Lista completa de itens de transporte
- Exemplo de resposta:
```json
[
  {
    "id": 1,
    "item": "Monitor",
    "descricao": "Monitor LCD 24 polegadas",
    "unidade": "UN",
    "quantidade": 5,
    "em_falta": "0",
    "total": "2500",
    "notas": "Verificar integridade na entrega",
    "imagem": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAA...",
    "created_at": "2023-07-10T11:22:33Z",
    "updated_at": "2023-07-10T11:22:33Z"
  }
]
```

**Criar Novo Item (POST /transport-items/ ou /guiaderemeca/)**
- Payload necessário:
```json
{
  "item": "Teclado",
  "descricao": "Teclado mecânico",
  "unidade": "UN",
  "quantidade": 10,
  "em_falta": "0",
  "total": "1500",
  "notas": "Modelo XYZ",
  "imagem": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAA..."
}
```
- Campos obrigatórios: `item`, `unidade`, `quantidade`
- Campos opcionais: `descricao`, `em_falta`, `total`, `notas`, `imagem`
- Para o campo `imagem`, envie uma string Base64 com o formato: `data:image/jpeg;base64,{dadosBase64}`

**Atualizar Item (PUT /transport-items/{id}/ ou /guiaderemeca/{id}/)**
- Payload similar ao de criação, mas apenas com os campos que deseja atualizar
- Exemplo para atualização parcial:
```json
{
  "quantidade": 15,
  "notas": "Atualizado: Modelo XYZ Premium"
}
```

### Manipulação de Imagens

O sistema aceita imagens no formato Base64. Para o frontend:

1. Converter imagem para Base64:
```javascript
function toBase64(file) {
   return new Promise((resolve, reject) => {
     const reader = new FileReader();
     reader.readAsDataURL(file);
     reader.onload = () => resolve(reader.result);
     reader.onerror = error => reject(error);
   });
}

// Uso
const file = document.querySelector('input[type="file"]').files[0];
const base64 = await toBase64(file);
// Enviar 'base64' para a API no campo 'imagem'
```

2. Exibir imagem Base64 recebida da API:
```html
<img :src="item.imagem" alt="Imagem do item">
```

### Considerações para o Frontend

1. **Formatação de Datas**: As datas são recebidas no formato ISO 8601 (UTC)
   - Exemplo para formatar data recebida: 
   ```javascript
   const date = new Date(item.created_at);
   const formattedDate = date.toLocaleDateString('pt-BR');
   ```

2. **Tratamento de Campos Vazios**: Campos como `em_falta`, `notas` podem ser null
   - Verifique valores nulos antes de processá-los

3. **Paginação**: A listagem de guias suporta paginação
   - Parâmetros: `?page=1&page_size=10`
   - A resposta inclui: `count`, `next`, `previous` e `results`

## Modelos de Dados

### GuiaDeTransporte
- `item`: Nome do item (CharField)
- `descricao`: Descrição detalhada (TextField)
- `unidade`: Unidade de medida (CharField)
- `quantidade`: Quantidade do item (IntegerField)
- `quantidade_total`: Quantidade total do item (IntegerField)
- `peso`: Peso do item (DecimalField, opcional)
- `volume`: Volume do item (DecimalField, opcional)
- `em_falta`: Informação sobre falta (CharField, opcional)
- `notas`: Observações (TextField, opcional)
- `total`: Valor total (CharField)
- `imagem`: Imagem em Base64 (TextField, opcional)
- `username`: Nome do usuário que registrou (CharField, opcional)
- `current_user`: Nome do usuário atual manipulando o registro (CharField, opcional)
- `created_at`: Data de criação (DateTimeField)
- `updated_at`: Data de atualização (DateTimeField)

### TransportItem
- `item`: Nome do item (CharField)
- `descricao`: Descrição detalhada (TextField, opcional)
- `unidade`: Unidade de medida (CharField)
- `quantidade`: Quantidade do item (IntegerField)
- `quantidade_total`: Quantidade total do item (IntegerField)
- `em_falta`: Informação sobre falta (CharField)
- `total`: Valor total (CharField)
- `notas`: Observações (TextField, opcional)
- `imagem`: Imagem em Base64 (TextField, opcional)
- `current_user`: Nome do usuário atual manipulando o registro (CharField, opcional)
- `created_at`: Data de criação (DateTimeField)
- `updated_at`: Data de atualização (DateTimeField)

## Casos de Uso

### Verificação de Quantidades
1. **Itens sem falta**: Quando `quantidade` = `quantidade_total`, o campo `em_falta` é definido como "0"
2. **Itens com falta**: Quando `quantidade` > `quantidade_total`:
   - O campo `em_falta` recebe o valor da diferença
   - Uma justificativa no campo `notas` é obrigatória
   - O sistema registra o usuário que realizou a operação

### Exemplo de Fluxo de Verificação
1. Recebimento de mercadorias:
   - Registre no campo `quantidade` o valor conforme documentação de transporte
   - Registre no campo `quantidade_total` a quantidade efetivamente recebida
2. O sistema calcula automaticamente se há faltas
3. Em caso de faltas, forneça uma justificativa no campo `notas`
4. Os dados ficam disponíveis para auditoria posterior com informações sobre quem realizou a verificação

## Interface Administrativa
A aplicação inclui uma interface administrativa personalizada acessível em `/admin/` após iniciar o servidor. Use as credenciais do superusuário criado anteriormente para acessar.

## Licença
[Especificar a licença do projeto]