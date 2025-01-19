const URL_BASE_API = 'https://api.example.com/dados/nome_do_app_codigoentrada';

export async function buscarDados(): Promise<any> {
  const resposta = await fetch(URL_BASE_API);
  if (!resposta.ok) throw new Error('Falha ao buscar dados');
  return resposta.json();
}

export async function enviarDados(dados: any): Promise<any> {
  const resposta = await fetch(URL_BASE_API, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(dados),
  });
  if (!resposta.ok) throw new Error('Falha ao enviar dados');
  return resposta.json();
}

export async function apagarDados(id: string): Promise<void> {
  const resposta = await fetch(`${URL_BASE_API}/${id}`, {
    method: 'DELETE',
  });
  if (!resposta.ok) throw new Error('Falha ao apagar dados');
}

export async function apagarTodosOsDados(): Promise<void> {
  const resposta = await fetch(`${URL_BASE_API}/limpar-tabela`, {
    method: 'DELETE',
  });
  if (!resposta.ok) throw new Error('Falha ao apagar todos os dados da tabela');
}