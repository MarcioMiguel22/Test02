// ...existing code...

/** Faz POST (bulk) no backend. Retorna o objeto response para tratamento. */
async function saveDataToBackend(data: LocalEntry[]) {
  const transformedData = data.map((item: LocalEntry) => ({
    localizacao: item.Localizacao,
    instalacao: item.Instalacao,
    codigos_da_porta: item.codigosDaPorta.join(','),
    codigo_caves: item.codigoCaves,
    local_da_chave: item.localDaChave,
    administracao: item.administracao,
    estado_do_elevador: item.estadoDoElevador,
    data_da_avaria: item.dataDaAvaria,
    tipo_de_contrato: item.tipoDeContrato,
    pago: item.Pago,
    fim_da_avaria: item.fimDaAvaria,
    notas: item.notas,
    codigo_material: item.codigoMaterial,
    descricao_material: item.descricaoMaterial,
    materiais: item.materiais,
  }));

  try {
    const response = await axios.post(BACKEND_URL, transformedData, {
      headers: { 'Content-Type': 'application/json' },
    });
    return response;
  } catch (error) {
    console.error('Erro ao salvar dados no backend:', error);
    throw error;
  }
}

// ...existing code...
