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
  em_falta: string;
  total: string;
  notas?: string;
  imagem?: string; // Base64 ou URL
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
      em_falta: data.em_falta,
      total: data.total,
      notas: data.notas,
      imagem: data.imagem, // Pode ser Base64 ou URL
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
      em_falta: item.em_falta || "0",
      total: item.total || "0",
      notas: item.notas || "",
      imagem: item.imagem || null
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
    em_falta: "0",
    total: "0"
  });
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const service = new GuiaDeRemecaService();
  
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
      if (item.id) {
        await service.update(item.id, item);
      } else {
        await service.create(item);
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
