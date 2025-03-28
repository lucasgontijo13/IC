# Iniciação Científica - Aprimoramento de Ferramenta para Automação da Auditoria de Conformidade com o CIS em Sistemas e Redes  

Repositório para a documentação do projeto de Iniciação Científica (IC) no IFMG-Campus Formiga, desenvolvido pelos membros da turma de Ciência da Computação.  

## Equipe  

| **Nome**                    | **Matrícula** | **GitHub**         |  
|-----------------------------|:-------------:|--------------------|  
| Kauan Eduardo da Silveira    | 0077593       | [KauanEdS](https://github.com/KauanEdS) |  
| Lucas Gontijo Rodrigues      | 0077151       | [lucasgontijo13](https://github.com/lucasgontijo13) |  

## GitHub Pages - Desenvolvimento Local  

### Configuração do Ambiente de Desenvolvimento  

1. **Criação da Estrutura do Projeto:**  
   - Crie uma pasta para armazenar os repositórios do projeto.  
   - Insira o repositório dentro dessa pasta.  

2. **Configuração do Arquivo `.env`:**  
   - Crie um arquivo `.env` com base no `exemplo.env`.
   - Substitua o arquivo `exemplo.env` pelo `.env` que acabou de criar e editar.

3. **Instalação do Ambiente Virtual:**  

   - Abra o terminal na pasta do projeto que você criou e execute os seguintes comandos,(Lembrando fora do mysite):  

     **Instale o `virtualenv`:**  
     ```console  
     pip install virtualenv  
     ```  

     **Crie o ambiente virtual:**  
     ```console  
     python -m venv venv  
     ```  

     **Ative o ambiente virtual:**  
     - **Linux/macOS:**  
       ```console  
       source venv/bin/activate  
       ```  
     - **Windows:**  
       ```console  
       venv\Scripts\activate  
       ```  

4. **Instalação das Dependências:**  
   - Navegue até a pasta do projeto:  
     ```console  
     cd mysite  
     ```  
   - Instale as dependências:  
     ```console  
     pip install -r requirements.txt  
     ```  

5. **Configuração do Banco de Dados:**  
   - **Geração do banco de dados:**  
     ```console  
     python createDataBase.py  
     ```  
   - **Aplicação de migrações:**  
     ```console  
     python manage.py makemigrations  
     ```  
     ```console  
     python manage.py migrate  
     ```  

6. **Configurando o Login com Google:**  
   - No terminal, execute o comando:  
     ```console  
     python create_social_account.py  
     ```  

7. **Execução do Servidor:**  
   - No terminal, execute o comando:  
     ```console  
     python manage.py runserver  
     ```  

8. **Acesso ao Projeto:**  
   - Abra seu navegador e acesse: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  

   
---

## Screenshots do Projeto

A seguir estão algumas imagens do projeto em funcionamento.

### 1. Tela de Login
![Tela de Login](./img/tela_de_login.png)

### 2. Tela de Registro
![Tela de Registro](./img/tela_de_registro.png)

### 3. Tela de Recuperação de Senha
![Tela de Recuperação de Senha](./img/tela_de_recuperacao_de_senha.png)

### 4. Tela para Digitar a Nova Senha
![Tela para Digitar a Nova Senha](./img/tela_para_nova_senha.png)

### 5. Tela Inicial Após Login
![Tela Inicial Após Login](./img/tela_inicial_apos_login.png)

### 6. Meio da Planilha
![Meio da Planilha](./img/meio_da_planilha.png)

### 7. Final da Planilha
![Final da Planilha](./img/final_da_planilha.png)

### 8. Grafico por Tipo de Ativo
![Grafico por tipo de Ativo](./img/grafico_ativo.png)

### 9. Grafico por Tipo de Controle
![Grafico por tipo de Controle](./img/grafico_controle.png)

### 10. Grafico de Velocimentro
![Grafico de velocímentro mostrando percentual de Sim](./img/grafico_velocimentro.png)













