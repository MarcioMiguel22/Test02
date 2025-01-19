import { Request, Response } from 'express';
import { ServicosDados } from '../services/ServicosDados';

export class ControladorDados {
  private servicosDados = new ServicosDados();

  async buscarTodos(req: Request, res: Response) {
    try {
      const dados = await this.servicosDados.buscarTodos();
      res.json(dados);
    } catch (erro) {
      res.status(500).json({ erro: 'Falha ao buscar dados' });
    }
  }

  async apagar(req: Request, res: Response) {
    try {
      const { id } = req.params;
      await this.servicosDados.apagar(id);
      res.status(204).send();
    } catch (erro) {
      res.status(500).json({ erro: 'Falha ao apagar dados' });
    }
  }

  async apagarTodos(req: Request, res: Response) {
    try {
      await this.servicosDados.apagarTodos();
      res.status(204).send();
    } catch (erro) {
      res.status(500).json({ erro: 'Falha ao apagar todos os dados da tabela' });
    }
  }
}
