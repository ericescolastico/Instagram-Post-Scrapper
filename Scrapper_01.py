########## Esse scrapping utilizando a API OFICIAL está funcionando para capturar posts de página vinculada no developer

import requests
import csv
import os
from dotenv import load_dotenv

load_dotenv()

# Carregar variáveis de ambiente do arquivo .env
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
USER_ID = os.getenv("USER_ID")

def get_instagram_posts(access_token, user_id, post_count=40):
    url = f'https://graph.instagram.com/{user_id}/media'
    params = {
        'fields': 'id,caption,media_type,media_url,permalink,thumbnail_url,timestamp',
        'access_token': access_token,
        'limit': post_count
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        posts = response.json()
        return posts['data']
    else:
        print(f'Error: {response.status_code}')
        print(response.text)
        return None

def export_posts_to_csv(posts, filename='instagram_posts_aponte.csv'):
    if not posts:
        print("Nenhuma postagem para exportar.")
        return
    
    fieldnames = ['id', 'caption', 'media_type', 'media_url', 'permalink', 'thumbnail_url', 'timestamp']
    
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for post in posts:
            writer.writerow({
                'id': post.get('id', ''),
                'caption': post.get('caption', ''),
                'media_type': post.get('media_type', ''),
                'media_url': post.get('media_url', ''),
                'permalink': post.get('permalink', ''),
                'thumbnail_url': post.get('thumbnail_url', ''),
                'timestamp': post.get('timestamp', '')
            })

if __name__ == "__main__":
    posts = get_instagram_posts(ACCESS_TOKEN, USER_ID, post_count=25)
    
    if posts:
        export_posts_to_csv(posts)
        print("Posts exportados para instagram_posts.csv com sucesso.")
    else:
        print("Nenhuma postagem encontrada.")