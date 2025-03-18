# Guia de Transporte - Integração Frontend/Backend

Este documento detalha como o frontend se conecta ao backend da aplicação Guia de Transporte, explicando o fluxo de dados, endpoints, e manipulação de imagens.

## Arquitetura de Integração

### Modelos de Dados

**Backend (Django):**
- `GuiaDeTransporte`: Armazena informações das guias de transporte
- `TransportItem`: Armazena os itens transportados incluindo suas imagens em Base64

**Frontend (TypeScript):**
```typescript
// TransportItem em types.ts
interface TransportItem {
  id?: number;
  item: string;
  descricao?: string;
  unidade: string;
  quantidade: number;
  quantidade_total: number;  // Quantidade total
  em_falta: string;
  total: string;
  notas?: string;
  imagem?: string; // Base64 ou URL
  current_user?: string; // Nome do usuário atual manipulando o registro
  created_at?: string;
  updated_at?: string;
}
```

### API Endpoints Disponíveis

| Endpoint | Método | Descrição | Payload/Resposta |
|---------|--------|-----------|-----------------|
| `/guias/` | GET | Lista todas as guias de transporte | Array de GuiaDeTransporte |
| `/guias/` | POST | Cria uma nova guia | GuiaDeTransporte object |
| `/guias/{id}/` | GET | Obtém detalhes de uma guia | GuiaDeTransporte object |
| `/guias/{id}/` | PUT | Atualiza uma guia existente | GuiaDeTransporte object |
| `/guias/{id}/` | DELETE | Remove uma guia existente | - |
| `/transport-items/` ou `/guiaderemeca/` | GET | Lista todos os itens de transporte | Array de TransportItem |
| `/transport-items/` ou `/guiaderemeca/` | POST | Cria um novo item | TransportItem object |
| `/transport-items/{id}/` ou `/guiaderemeca/{id}/` | GET | Obtém detalhes de um item | TransportItem object |
| `/transport-items/{id}/` ou `/guiaderemeca/{id}/` | PUT | Atualiza um item existente | TransportItem object |
| `/transport-items/{id}/` ou `/guiaderemeca/{id}/` | DELETE | Remove um item existente | - |

## Fluxo de Integração

### 1. Serviços de API no Frontend

```typescript
// GuiaService.ts
export class GuiaDeRemecaService {
  private baseUrl = '/api/guiaderemeca';
  
  // Converte dados do backend para o formato do frontend
  transformBackendData(data: any): TransportItem {
    return {
      id: data.id,
      item: data.item,
      descricao: data.descricao,
      unidade: data.unidade,
      quantidade: data.quantidade,
      quantidade_total: data.quantidade_total || 0,  // Nova quantidade total
      em_falta: data.em_falta,
      total: data.total,
      notas: data.notas,
      imagem: data.imagem, // Pode ser Base64 ou URL
      current_user: data.current_user, // Nome do usuário atual
      created_at: data.created_at,
      updated_at: data.updated_at
    };
  }
  
  // Converte dados do frontend para o formato do backend
  transformToBackendFormat(item: TransportItem): any {
    return {
      item: item.item,
      descricao: item.descricao || "",
      unidade: item.unidade,
      quantidade: item.quantidade,
      quantidade_total: item.quantidade_total || 0,  // Nova quantidade total
      em_falta: item.em_falta || "0",
      total: item.total || "0",
      notas: item.notas || "",
      imagem: item.imagem || null,
      current_user: item.current_user || null // Envia o usuário atual
    };
  }
  
  // Converte Base64 para File para envio como FormData
  base64ToFile(base64String: string, filename: string): File {
    const arr = base64String.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, { type: mime });
  }
  
  // Busca todos os itens
  async fetchAll(): Promise<TransportItem[]> {
    const response = await fetch(this.baseUrl);
    const data = await response.json();
    return data.map(this.transformBackendData);
  }
  
  // Cria um novo item (gerencia envio de imagem)
  async create(item: TransportItem): Promise<TransportItem> {
    const backendData = this.transformToBackendFormat(item);
    
    // Decide se envia como JSON ou FormData baseado na imagem
    if (item.imagem && item.imagem.startsWith('data:')) {
      // Envio como FormData se imagem for Base64
      const formData = new FormData();
      Object.keys(backendData).forEach(key => {
        if (key === 'imagem' && backendData[key]) {
          formData.append('imagem', this.base64ToFile(backendData[key], 'image.jpg'));
        } else {
          formData.append(key, backendData[key]);
        }
      });
      
      const response = await fetch(this.baseUrl, {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      return this.transformBackendData(data);
    } else {
      // Envio como JSON se não houver imagem ou se for uma URL
      const response = await fetch(this.baseUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(backendData)
      });
      const data = await response.json();
      return this.transformBackendData(data);
    }
  }
  
  // Similar ao create, mas para atualização
  async update(id: number, item: TransportItem): Promise<TransportItem> {
    // Código similar ao create, mas com método PUT
    // ...
  }
  
  // Exclui um item
  async delete(id: number): Promise<void> {
    await fetch(`${this.baseUrl}/${id}`, {
      method: 'DELETE'
    });
  }
}
```

### 2. Formulário no Frontend

```typescript
// TransportItemForm.tsx (simplificado)
function TransportItemForm() {
  const [item, setItem] = useState<TransportItem>({
    item: "",
    unidade: "UN",
    quantidade: 0,
    quantidade_total: 0, // Inicializa quantidade total
    em_falta: "0",
    total: "0",
    current_user: getCurrentUser() // Obtém o usuário atual da sessão ou contexto
  });
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const service = new GuiaDeRemecaService();
  
  // Função para obter o usuário atual (implementação depende da sua autenticação)
  function getCurrentUser() {
    // Exemplo: retorna do localStorage ou de um contexto de autenticação
    return localStorage.getItem('currentUser') || 'anonymous';
  }
  
  // Manipula upload de arquivo de imagem
  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64String = reader.result as string;
        setItem({...item, imagem: base64String});
        setImagePreview(base64String);
      };
      reader.readAsDataURL(file);
    }
  };
  
  // Envia dados para o backend
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Atualiza o usuário atual antes de enviar
      const updatedItem = {
        ...item,
        current_user: getCurrentUser()
      };
      
      if (updatedItem.id) {
        await service.update(updatedItem.id, updatedItem);
      } else {
        await service.create(updatedItem);
      }
      // Sucesso - redireciona ou limpa o formulário
    } catch (error) {
      console.error("Erro ao salvar item", error);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {/* Campos do formulário */}
      <input 
        type="text" 
        value={item.item}
        onChange={e => setItem({...item, item: e.target.value})} 
        required
      />
      {/* Outros campos */}
      
      {/* Upload de imagem */}
      <input type="file" onChange={handleImageUpload} />
      {imagePreview && <img src={imagePreview} alt="Preview" />}
      
      <button type="submit">Salvar</button>
    </form>
  );
}
```

### 3. Componente de Listagem

```typescript
// GuiaDeTransporte.tsx (simplificado)
function GuiaDeTransporte() {
  const [items, setItems] = useState<TransportItem[]>([]);
  const service = new GuiaDeRemecaService();
  
  useEffect(() => {
    const fetchItems = async () => {
      try {
        const data = await service.fetchAll();
        setItems(data);
      } catch (error) {
        console.error("Erro ao buscar itens", error);
      }
    };
    fetchItems();
  }, []);
  
  return (
    <div>
      <h1>Itens de Transporte</h1>
      <table>
        <thead>
          <tr>
            <th>Item</th>
            <th>Descrição</th>
            <th>Unidade</th>
            <th>Quantidade</th>
            <th>Em Falta</th>
            <th>Total</th>
            <th>Usuário Atual</th>
            <th>Imagem</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {items.map(item => (
            <tr key={item.id}>
              <td>{item.item}</td>
              <td>{item.descricao}</td>
              <td>{item.unidade}</td>
              <td>{item.quantidade}</td>
              <td>{item.em_falta}</td>
              <td>{item.total}</td>
              <td>{item.current_user || 'N/A'}</td>
              <td>
                {item.imagem && (
                  <img 
                    src={item.imagem} 
                    alt={`Imagem de ${item.item}`}
                    style={{ maxWidth: '100px', maxHeight: '100px' }} 
                  />
                )}
              </td>
              <td>
                {/* Botões de editar e excluir */}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

## Processamento de Imagens

### No Frontend
1. **Upload**:
   - O usuário seleciona um arquivo de imagem
   - O arquivo é convertido para Base64 usando FileReader
   - O Base64 é armazenado no estado do componente e usado para preview

2. **Envio para o Backend**:
   - Se a imagem for Base64, ela é convertida em File e enviada como FormData
   - Se for uma URL ou não existir, os dados são enviados como JSON

3. **Exibição**:
   - Imagens são exibidas diretamente usando a fonte (`src`) como o valor Base64 ou URL

### No Backend
1. **Recebimento**:
   - O campo `imagem` do modelo `TransportItem` é um TextField que armazena a string Base64
   - Os dados são recebidos via JSONParser e salvos diretamente no banco

2. **Processamento**:
   - As imagens são armazenadas como strings Base64 no banco de dados
   - Não há processamento adicional no backend além da validação

3. **Retorno**:
   - O backend retorna a string Base64 como parte do objeto TransportItem

## Considerações Importantes

1. **Tamanho das Imagens**:
   - Considere limitar o tamanho das imagens antes do upload para evitar sobrecarga do banco de dados
   - Implemente compressão de imagem no frontend antes de converter para Base64

2. **Segurança**:
   - Valide os tipos de arquivo permitidos (apenas imagens)
   - Implemente autenticação para proteger os endpoints

3. **Performance**:
   - As imagens Base64 aumentam significativamente o tamanho da payload
   - Considere implementar um sistema de armazenamento dedicado (como Amazon S3) para imagens maiores

4. **Compatibilidade**:
   - Certifique-se que o backend está configurado para aceitar requisições de diferentes tipos (JSON e FormData)
   - Atualize os limites de tamanho de requisição no servidor se necessário

## Próximos Passos para Implementação

1. Ajustar o serializer no backend para processar imagens Base64 corretamente
2. Configurar o parser no backend para aceitar FormData quando necessário
3. Implementar validação de tamanho e tipo de imagem
4. Adicionar autenticação à API
5. Configurar CORS para permitir acesso do frontend ao backend

## Rastreamento do Usuário Atual

### Implementação no Frontend

Para implementar o rastreamento de usuários no frontend:

1. **Armazenar informações do usuário**:
   ```typescript
   // Ao fazer login
   localStorage.setItem('currentUser', username);
   
   // Para obter o usuário atual
   const currentUser = localStorage.getItem('currentUser') || 'anonymous';
   ```

2. **Enviar sempre em requisições**:
   ```typescript
   // Adicionar à todas as requisições que criam ou atualizam dados
   const requestData = {
     ...formData,
     current_user: localStorage.getItem('currentUser')
   };
   ```

3. **Exibir nas interfaces de administração**:
   ```typescript
   // No componente de detalhes
   <div className="item-details">
     <p><strong>Item:</strong> {item.item}</p>
     <p><strong>Descrição:</strong> {item.descricao}</p>
     <p><strong>Última atualização por:</strong> {item.current_user || 'Não informado'}</p>
   </div>
   ```

### Implementação no Backend

O backend já está configurado para:

1. Receber o campo `current_user` através do serializer
2. Armazenar esse valor no banco de dados
3. Retornar o valor em respostas às requisições GET

Isso permite rastrear qual usuário está manipulando cada registro no sistema.

## Sistema de Verificação de Quantidades

### Descrição Técnica

O sistema implementa uma verificação automática que compara duas quantidades:
- `quantidade`: Quantidade registrada na guia de transporte (documento oficial)
- `quantidade_total`: Quantidade efetivamente encontrada no veículo/carrinha

Quando há discrepância (quantidade_total < quantidade), o sistema:
1. Calcula automaticamente o valor de `em_falta`
2. Exige justificativa no campo `notas`
3. Registra qual usuário reportou a discrepância

### Implementação no Backend

```python
# Cálculo automático de itens em falta (views.py)
quantidade = int(data.get('quantidade', 0))
quantidade_total = int(data.get('quantidade_total', 0))

if quantidade_total < quantidade:
    em_falta = str(quantidade - quantidade_total)
    
    # Validação de justificativa
    if not data.get('notas') or not data.get('notas').strip():
        return Response(
            {"notas": "É necessário justificar os itens em falta nas notas."}, 
            status=status.HTTP_400_BAD_REQUEST
        )
else:
    em_falta = "0"
    
data['em_falta'] = em_falta
```

### Implementação no Frontend

```typescript
// Exemplo de cálculo e validação de itens em falta no frontend (TypeScript)
function validateItemQuantities(item: TransportItem): boolean {
  const quantidade = Number(item.quantidade) || 0;
  const quantidadeTotal = Number(item.quantidade_total) || 0;
  
  // Verifica se há itens em falta
  if (quantidadeTotal < quantidade) {
    const emFalta = quantidade - quantidadeTotal;
    
    // Requer justificativa quando há itens em falta
    if (!item.notas || !item.notas.trim()) {
      alert('É necessário justificar os itens em falta nas notas.');
      return false;
    }
    
    // Atualiza o valor em_falta
    item.em_falta = emFalta.toString();
  } else {
    item.em_falta = '0';
  }
  
  return true;
}

// Uso no formulário de envio
handleSubmit = async (e) => {
  e.preventDefault();
  
  if (!validateItemQuantities(this.state.item)) {
    return; // Interrompe o envio se a validação falhar
  }
  
  // Continua com o envio dos dados...
}
```

## Fluxo de Integração

### 2. Formulário no Frontend

```typescript
// TransportItemForm.tsx (simplificado com verificação de quantidades)
function TransportItemForm() {
  const [item, setItem] = useState<TransportItem>({
    item: "",
    unidade: "UN",
    quantidade: 0,
    quantidade_total: 0,
    em_falta: "0",
    total: "0",
    current_user: getCurrentUser()
  });
  
  // ...existing code...
  
  // Calcula automaticamente itens em falta quando os valores mudam
  const handleQuantityChange = (e: React.ChangeEvent<HTMLInputElement>, field: string) => {
    const value = parseInt(e.target.value) || 0;
    const updatedItem = { ...item, [field]: value };
    
    // Quando qualquer um dos campos de quantidade é alterado, recalcula em_falta
    const quantidade = field === 'quantidade' ? value : item.quantidade;
    const quantidadeTotal = field === 'quantidade_total' ? value : item.quantidade_total;
    
    if (quantidadeTotal < quantidade) {
      updatedItem.em_falta = (quantidade - quantidadeTotal).toString();
    } else {
      updatedItem.em_falta = "0";
    }
    
    setItem(updatedItem);
  };
  
  // Adiciona validação ao enviar o formulário
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const updatedItem = {
        ...item,
        current_user: getCurrentUser()
      };
      
      // Validação de itens em falta
      if (Number(updatedItem.em_falta) > 0 && (!updatedItem.notas || !updatedItem.notas.trim())) {
        alert("É necessário justificar os itens em falta nas notas.");
        return;
      }
      
      if (updatedItem.id) {
        await service.update(updatedItem.id, updatedItem);
      } else {
        await service.create(updatedItem);
      }
      // Sucesso - redireciona ou limpa o formulário
    } catch (error) {
      console.error("Erro ao salvar item", error);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      {/* ...campos existentes... */}
      
      <div className="form-group">
        <label>Quantidade na Guia:</label>
        <input 
          type="number" 
          value={item.quantidade}
          onChange={(e) => handleQuantityChange(e, 'quantidade')}
          min="0" 
          required
        />
      </div>
      
      <div className="form-group">
        <label>Quantidade Real na Carrinha:</label>
        <input 
          type="number" 
          value={item.quantidade_total}
          onChange={(e) => handleQuantityChange(e, 'quantidade_total')}
          min="0" 
          required
        />
      </div>
      
      {Number(item.em_falta) > 0 && (
        <div className="alert alert-warning">
          <p><strong>Itens em falta: {item.em_falta}</strong></p>
          <p>É necessário justificar os itens em falta nas notas.</p>
        </div>
      )}
      
      <div className="form-group">
        <label>Notas/Justificativa:</label>
        <textarea 
          value={item.notas || ''}
          onChange={(e) => setItem({...item, notas: e.target.value})}
          required={Number(item.em_falta) > 0}
        />
      </div>
      
      {/* ...outros campos e botões... */}
    </form>
  );
}
```

### 3. Componente de Listagem com Indicação Visual de Faltas

```typescript
// GuiaDeTransporte.tsx (com indicação visual de itens em falta)
function GuiaDeTransporte() {
  // ...existing code...
  
  // Função para determinar a classe CSS baseada no status de falta
  const getRowClass = (item: TransportItem) => {
    if (Number(item.em_falta) > 0) {
      return "row-missing-items"; // Estilo para itens em falta
    } else if (Number(item.quantidade_total) > Number(item.quantidade)) {
      return "row-excess-items"; // Estilo para itens em excesso
    }
    return "row-normal"; // Estilo para itens normais
  };
  
  return (
    <div>
      <h1>Itens de Transporte</h1>
      <table>
        <thead>
          <tr>
            <th>Item</th>
            <th>Descrição</th>
            <th>Unidade</th>
            <th>Qtd. na Guia</th>
            <th>Qtd. na Carrinha</th>
            <th>Em Falta</th>
            <th>Notas/Justificativa</th>
            <th>Usuário</th>
            <th>Imagem</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {items.map(item => (
            <tr key={item.id} className={getRowClass(item)}>
              <td>{item.item}</td>
              <td>{item.descricao}</td>
              <td>{item.unidade}</td>
              <td>{item.quantidade}</td>
              <td>{item.quantidade_total}</td>
              <td className={Number(item.em_falta) > 0 ? "missing-highlight" : ""}>
                {item.em_falta}
              </td>
              <td>{item.notas}</td>
              <td>{item.current_user || 'N/A'}</td>
              <td>
                {item.imagem && (
                  <img 
                    src={item.imagem} 
                    alt={`Imagem de ${item.item}`}
                    style={{ maxWidth: '100px', maxHeight: '100px' }} 
                  />
                )}
              </td>
              <td>
                {/* Botões de editar e excluir */}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      
      <style jsx>{`
        .row-missing-items {
          background-color: #fff3cd;
        }
        .row-excess-items {
          background-color: #f8d7da;
        }
        .row-normal {
          background-color: #d1e7dd;
        }
        .missing-highlight {
          color: #dc3545;
          font-weight: bold;
        }
      `}</style>
    </div>
  );
}
```

## Processamento de Imagens

### No Frontend
1. **Upload**:
   - O usuário seleciona um arquivo de imagem
   - O arquivo é convertido para Base64 usando FileReader
   - O Base64 é armazenado no estado do componente e usado para preview

2. **Envio para o Backend**:
   - Se a imagem for Base64, ela é convertida em File e enviada como FormData
   - Se for uma URL ou não existir, os dados são enviados como JSON

3. **Exibição**:
   - Imagens são exibidas diretamente usando a fonte (`src`) como o valor Base64 ou URL

### No Backend
1. **Recebimento**:
   - O campo `imagem` do modelo `TransportItem` é um TextField que armazena a string Base64
   - Os dados são recebidos via JSONParser e salvos diretamente no banco

2. **Processamento**:
   - As imagens são armazenadas como strings Base64 no banco de dados
   - Não há processamento adicional no backend além da validação

3. **Retorno**:
   - O backend retorna a string Base64 como parte do objeto TransportItem

## Casos de Uso Completos

### 1. Registro de Item com Falta

```typescript
// Exemplo de criação de item com falta
const newItem = {
  item: "Monitor LCD",
  descricao: "Monitor LCD 24 polegadas",
  unidade: "UN",
  quantidade: 10,            // Quantidade na guia
  quantidade_total: 8,       // Quantidade na carrinha
  notas: "2 monitores danificados durante transporte, caixas amassadas",
  total: "1500",
  current_user: "operador_joao"
};

// O backend calculará automaticamente em_falta como "2"
// E validará a presença da justificativa em notas
const savedItem = await guiaDeRemecaService.create(newItem);
```

### 2. Atualização de Quantidades

```typescript
// Exemplo de atualização de item
const itemToUpdate = {
  ...existingItem,
  quantidade: 15,             // Nova quantidade na guia
  quantidade_total: 12,       // Nova quantidade na carrinha
  notas: "3 itens não encontrados, investigação em andamento"
};

// O backend recalculará automaticamente em_falta como "3"
// E validará a presença da justificativa
await guiaDeRemecaService.update(itemToUpdate.id, itemToUpdate);
```
