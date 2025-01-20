export class ServicosDados {
  private dados: Map<string, any> = new Map();

  async buscarTodos(): Promise<any[]> {
    return Array.from(this.dados.values());
  }

  async atualizar(id: string, dadosAtualizados: any): Promise<any | null> {
    const existente = this.dados.get(id);
    if (!existente) return null;
    
    const atualizado = { ...existente, ...dadosAtualizados };
    this.dados.set(id, atualizado);
    return atualizado;
  }

  async apagar(id: string): Promise<void> {
    this.dados.delete(id);
  }

  async apagarTodos(): Promise<void> {
    this.dados.clear();
  }
}
