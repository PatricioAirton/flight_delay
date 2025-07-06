flight_delay
Minha API
Este pequeno projeto faz parte do MVP para análise de atraso de voos

Como executar
Será necessário ter todas as libs python listadas no requirements.txt instaladas, é bem simples o processo.

Após clonar o repositório, é necessário ir ao diretório raiz do projeto, pelo terminal, para poder executar os comandos descritos abaixo.

É fortemente indicado o uso de ambientes virtuais do tipo virtualenv.

(env)$ pip install -r requirements.txt
Este comando instala as dependências/bibliotecas, descritas no arquivo requirements.txt.

Para executar a API basta executar:

(env)$ flask run --host 0.0.0.0 --port 5001
Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor automaticamente após uma mudança no código fonte.

(env)$ flask run --host 0.0.0.0 --port 5001 --reload
Abra o http://localhost:5001/#/ no navegador para verificar o status da API em execução.