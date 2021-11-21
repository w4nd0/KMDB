# KMDb 📽️

KMDb é um sistema de avaliação e crítica de filmes, parecida com o IMDb e conta com três tipos de usuários: administradores, criticos e comuns.

Ao utilizar esta API, um administrador pode criar, atualizar e deletar informações sobre um determinado filme; usuários do tipo critico podem criar e atualizar avaliações para os filmes enquanto usuários comuns podem somente ler as informações da API.

## Como instalar e rodar? 🚀

Para instalar o sistema, é necessário seguir alguns passos, como baixar o projeto e fazer instalação das dependências. Para isso, é necessário abrir uma aba do terminal e digitar o seguinte:

```
# Clonando o repositório
git clone git@gitlab.com:trevius/e-4-km-db.git
```

Depois de clonado, é necessário entrar na pasta, criar um ambiente virtual e por fim entrar no ambiente:

```
# Entrar na pasta
cd e-4-km-db

# Criar um ambiente virtual
python3 -m venv venv

# Entrar no ambiente virtual
source venv/bin/activate
```

Então, para instalar as dependências, basta:

`pip install -r requirements.txt`

Depois de ter instalado as dependências, é necessário rodar as migrations para que o banco de dados e as tabelas sejam criadas:

`./manage.py migrate`

Então, para rodar, basta digitar o seguinte, no terminal:

`./manage.py runserver`

E o sistema estará rodando em http://127.0.0.1:8000/

## Utilização 🖥️

Para utilizar este sistema, é necessário utilizar um API Client, como o [Insomnia](https://insomnia.rest/download)

## Rotas 🔄

### **ACCOUNTS**
<br>

**POST /api/accounts/**

Rota para criar uma conta, de acordo com a requisição:

- Usuário Comum (is_superuser `false` e is_staff `false`)
- Crítico (is_superuser `false` e is_staff `true`)
- Administrador (is_superuser `true` e is_staff `true`)

Request:

```
{
    "username": "user",
    "password": "1234",
    "first_name": "John",
    "last_name": "Wick",
    "is_superuser": false,
    "is_staff": false
}
```

`RESPONSE STATUS -> HTTP 201 (create)`

Response:

```
{
    "id": 1,
    "username": "user",
    "first_name": "John",
    "last_name": "Wick",
    "is_superuser": false,
    "is_staff": false,
}
```

**POST /api/login/**

Rota para logar na aplicação, retorna o token para acessar as rotas autentificadas.

Request:

```
{
    "username": "user",
    "password": "1234"
}
```

`RESPONSE STATUS -> HTTP 200 (ok)`

Response:

```
{
    "token": "dfd384673e9127213de6116ca33257ce4aa203cf"
}
```
<hr>

### **MOVIES**
<br>

**POST /api/movies/**\
🔑(somente admin)

Rota para criar um filme.

Request:

```
{
    "title": "O Poderoso Chefão 2",
    "duration": "175m",
    "genres": [
        {"name": "Crime"},
        {"name": "Drama"}
    ],
    "premiere": "1972-09-10",
    "classification": 14,
    "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' ..."
}
```

`RESPONSE STATUS -> HTTP 201 (create)`

Response:

```
{
 "id": 1,
    "title": "O Poderoso Chefão 2",
    "duration": "175m",
    "genres": [
        {
            "id": 1,
            "name": "Crime"
        },
        {
            "id": 2,
            "name": "Drama"
        }
    ],
    "premiere": "1972-09-10",
    "classification": 14,
    "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma ..."
}
```

**GET /api/movies/**

Rota que lista todos os filmes cadastrados.

`RESPONSE STATUS -> HTTP 200 (ok)`

Response:

```
[
    {
        "id": 1,
        "title": "O Poderoso Chefão 2",
        "duration": "175m",
        "genres": [
            {
                "id": 1,
                "name": "Crime"
            },
            {
                "id": 2,
                "name": "Drama"
            }
        ],
        "premiere": "1972-09-10",
        "classification": 14,
        "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' ..."
    },
    {
        "id": 2,
        "title": "Um Sonho de Liberdade",
        "duration": "142m",
        "genres": [
            {
                "id": 2,
                "name": "Drama"
            },
            {
                "id": 4,
                "name": "Ficção científica"
            }
        ],
        "premiere": "1994-10-14",
        "classification": 16,
        "synopsis": "Andy Dufresne é condenado a duas prisões perpétuas..."
    }
]
```

**GET /api/movies?title=\<nome>**

Rota que lista todos os filmes cadastrados que contenham um determinado valor (passado via request) em seu título.

`RESPONSE STATUS -> HTTP 200 (ok)`

Response:

```
# Busca feita com a palavra 'liberdade'
[
  {
    "id": 2,
    "title": "Um Sonho de Liberdade",
    "duration": "142m",
    "genres": [
        {
            "id": 2,
            "name": "Drama"
        },
      {
        "id": 3,
        "name": "Ficção científica"
      }
    ],
    "premiere": "1994-10-14",
    "classification": 16,
    "synopsis": "Andy Dufresne é condenado a duas prisões perpétuas..."
  },
  {
    "id": 3,
    "title": "Em busca da liberdade",
    "duration": "175m",
    "genres": [
        {
            "id": 2,
            "name": "Drama"
        },
        {
            "id": 4,
            "name": "Obra de época"
        }
    ],
    "premiere": "2018-02-22",
    "classification": 14,
    "synopsis": "Representando a Grã-Bretanha,  corredor Eric Liddell",
  }
]  
```

**GET /api/movies/\<int:movie_id>/**

Rota que busca o filme especificado pelo id.\

🗝️ Caso o usuário esteja autenticado, as reviews serão mostradas juntamente com o retorno.

`RESPONSE STATUS -> HTTP 200 (ok)`

Response:

```
# Header -> Authorization: Token <token-do-critic ou token-do-admin>         
{
    "id": 9,
    "title": "Nomadland",
    "duration": "110m",
    "genres": [
        {
            "id": 2,
            "name": "Drama"
        },
        {
            "id": 4,
            "name": "Obra de Época"
        }
    ],
    "premiere": "2021-04-15",
    "classification": 14,
    "synopsis": "Uma mulher na casa dos 60 anos que, depois de perder...",
    "reviews": [
        {
        "id": 5,
        "critic": {
            "id": 1,
            "first_name": "Jacques",
            "last_name": "Aumont"
        },
        "stars": 8,
        "review": "Nomadland apresenta fortes credenciais para ser favorito ...",
        "spoilers": false
        }
    ]
}
```

No caso de um acesso anônimo o retorno será:

```
{
  "id": 9,
  "title": "Nomadland",
  "duration": "110m",
  "genres": [
    {
      "id": 2,
      "name": "Drama"
    },
    {
      "id": 4,
      "name": "Obra de Época"
    }
  ],
  "premiere": "2021-04-15",
  "classification": 14,
  "synopsis": "Uma mulher na casa dos 60 anos que, depois de perder..."
}
```

**PUT /api/movies/\<int:movie_id>/**\
🔑(somente admin)

Rota para atualizar um filme, a partir do seu id

Request:

```
{
    "title": "O Poderoso Chefão",
    "duration": "175m",
    "genres": [
        {"name": "Crime"},
        {"name": "Drama"},
        {"name": "Mafia"}
    ],
    "premiere": "1972-09-10",
    "classification": 14,
    "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma 'família' ..."
}
```

`RESPONSE STATUS -> HTTP 200 (ok)`

Response:

```
{
    "id": 1,
    "title": "O Poderoso Chefão",
    "duration": "175m",
    "genres": [
        {
            "id": 1,
            "name": "Crime"
        },
        {
            "id": 2,
            "name": "Drama"
        },
        {
            "id": 3,
            "name": "Mafia"
        }
    ],
    "premiere": "1972-09-10",
    "classification": 14,
    "synopsis": "Don Vito Corleone (Marlon Brando) é o chefe de uma ..."
}
```

**DELETE /api/movies/\<int:movie_id>/**\
🔑(somente admin)

Rota para deletar um filme.\
*Ao excluir um filme da plataforma, também serão removidos todos os reviews correspondentes.

`RESPONSE STATUS -> HTTP 204 (no content)`
<hr>

### **REVIEWS**

<br>

**POST /api/movies/\<int:movie_id>/review/**\
🔑(somente crítico)

Rota para a criação de uma avaliação de um filme.

Request:

```
{
    "stars": 7,
    "review": "O Poderoso Chefão 2 podia ter dado muito errado...",
    "spoilers": false,
}
```

`RESPONSE STATUS -> HTTP 201 (create)`

Response:

```
{
    "id": 1,
    "critic": {
        "id": 1,
        "first_name": "Jacques",
        "last_name": "Aumont"
    },
    "stars": 7,
    "review": "O Poderoso Chefão 2 podia ter dado muito errado...",
    "spoilers": false
}
```


**PUT /api/movies/\<int:movie_id>/review/**\
🔑(somente crítico)

Rota para a atualização de uma avaliação de um filme. 


Request:

```
# Todos os campos são obrigatórios
{
    "stars": 2,
    "review": "O Poderoso Chefão 2 podia ter dado muito certo..",
    "spoilers": true
}
```

`RESPONSE STATUS -> HTTP 200 (ok)`

Response:

```
{
    "id": 1,
    "critic": {
        "id": 1,
        "first_name": "Jacques",
        "last_name": "Aumont"
    },
    "stars": 2,
    "review": "O Poderoso Chefão 2 podia ter dado muito certo..",
    "spoilers": true
}
```

**GET /api/reviews/**\
🔑(somente admin ou crítico)

Lista as reviews, todas se o usuário for admin ou apenas do próprio usuário se for crítico

`RESPONSE STATUS -> HTTP 200 (ok)`

Response:

```
[
   {
      "id":1,
      "critic":{
         "id":1,
         "first_name":"Jacques",
         "last_name":"Aumont"
      },
      "stars":2,
      "review":"O Poderoso Chefão 2 podia ter dado muito certo..",
      "spoilers":true,
      "movie": 1
   },
   {
      "id":2,
      "critic":{
         "id":2,
         "first_name":"Bruce",
         "last_name":"Wayne"
      },
      "stars": 8,
      "review":"Não consegui ver até o final, fiquei com medo",
      "spoilers":false,
      "movie": 2
   },
   {
      "id":3,
      "critic":{
         "id":2,
         "first_name":"Bruce",
         "last_name":"Wayne"
      },
      "stars":10,
      "review":"Melhor filme que já assisti",
      "spoilers":true
      "movie": 1
   }
]
```

Aqui a rota sendo acessada com um usuário do tipo crítico, e no retorno somente suas avaliações são exibidas:

```
# Header -> Authorization: Token <token-do-critic>
[
  {
      "id":2,
      "critic":{
         "id":2,
         "first_name":"Bruce",
         "last_name":"Wayne"
      },
      "stars": 8,
      "review":"Não consegui ver até o final, fiquei com medo",
      "spoilers":false,
      "movie": 2
   },
   {
      "id":3,
      "critic":{
         "id":2,
         "first_name":"Bruce",
         "last_name":"Wayne"
      },
      "stars":10,
      "review":"Melhor filme que já assisti",
      "spoilers":true
      "movie": 1
   }
]
```

## Tecnologias utilizadas 📱

- Django
- Django Rest Framework
- SQLite

<hr>

**Licence**\
MIT