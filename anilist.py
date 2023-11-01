import requests
import json

class Anilist:
  def __init__(self):
    pass
  def busca(self,nome:str, page = 1)->list:
    query = '''
    query ($id: Int, $page: Int, $perPage: Int, $search: String,$type:MediaType) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (id: $id, search: $search,type:$type) {
                id
                type
                title {
                    romaji
                }
            }
        }
    }
    '''
    variables = {
        'search': nome,
        'type': "ANIME",
        'page': page,
        'perPage': 5
    }
    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()
    result = data["data"]["Page"]["media"]
    return result

if __name__ == "__main__":
    anilistapi = Anilist()
    animes = input("Insira o nome que deseja buscar: ")
    print(anilistapi.busca(animes,2))