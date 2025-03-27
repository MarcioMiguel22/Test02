# Gestão de Códigos de Entrada

Este projeto é uma API RESTful desenvolvida com Django e Django Rest Framework para gerenciar códigos de entrada para diferentes instalações.

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Modelo de Dados](#modelo-de-dados)
- [API Endpoints](#api-endpoints)
- [Exemplos de Uso](#exemplos-de-uso)
- [Testes](#testes)

## 🔍 Visão Geral

Este sistema permite gerenciar códigos de entrada para diferentes localizações e instalações. Cada instalação possui informações como códigos de porta, código de caves, localização de chaves e mais.

## 💻 Tecnologias

- Python 3.x
- Django
- Django Rest Framework
- SQLite (padrão do Django)

## ⚙️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/MarcioMiguel22/Sites/Test02.git
   cd Test02
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

5. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

## 📁 Estrutura do Projeto
