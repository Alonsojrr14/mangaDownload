import os
import requests
from bs4 import BeautifulSoup
from ebooklib import epub
from PIL import Image
from io import BytesIO

def extrair_info_url(url):
    parts = url.split("/")
    if len(parts) < 6:
        raise ValueError("URL inválida. Não foi possível extrair o nome do mangá ou o capítulo.")
    manga_nome = parts[4]
    capitulo_num = parts[-2]
    return manga_nome, capitulo_num

def baixar_imagens(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Falha ao acessar a página. Código de status: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img", class_="wp-manga-chapter-img")

    if not img_tags:
        raise Exception("Nenhuma imagem encontrada na página.")

    img_files = []
    for i, img_tag in enumerate(img_tags, start=1):
        img_url = img_tag.get("src", "").strip()
        if not img_url:
            continue

        print(f"Baixando imagem {i}: {img_url}")
        img_response = requests.get(img_url, headers=headers)

        if img_response.status_code == 200:
            try:
                with Image.open(BytesIO(img_response.content)) as img:
                    img = img.convert("RGB")
                    img_byte_arr = BytesIO()
                    img.save(img_byte_arr, format="JPEG")
                    img_byte_arr = img_byte_arr.getvalue()

                img_filename = f"img_{i}.jpeg"  # Nome único para cada imagem
                img_files.append((img_filename, img_byte_arr))
            except Exception as e:
                print(f"Erro ao processar imagem {i}: {e}")
                continue

    return img_files

def criar_epub(manga_nome, capitulo_num, img_files, diretorio_manga):
    livro = epub.EpubBook()
    livro.set_identifier(f"{manga_nome}-{capitulo_num}")
    livro.set_title(f"{manga_nome.capitalize()} - Capítulo {capitulo_num}")
    livro.set_language("pt")
    livro.add_author("Desconhecido")

    if img_files:
        capa_filename, capa_content = img_files[0]
        livro.set_cover(f"OEBPS/images/{capa_filename}", capa_content)

    css_content = "img { max-width: 100%; height: auto; display: block; margin: 0 auto; }"
    css_item = epub.EpubItem(
        uid="style",
        file_name="OEBPS/styles/style.css",
        media_type="text/css",
        content=css_content
    )
    livro.add_item(css_item)

    paginas = []
    for i, (img_filename, img_content) in enumerate(img_files, start=1):
        img_item = epub.EpubItem(
            uid=f"img_{i}",
            file_name=f"OEBPS/images/{img_filename}",
            media_type="image/jpeg",
            content=img_content
        )
        livro.add_item(img_item)

        img_html = f'<html xmlns="http://www.w3.org/1999/xhtml"><head><link rel="stylesheet" type="text/css" href="../styles/style.css" /></head><body><img src="../images/{img_filename}" style="width:100%;"/></body></html>'
        page_item = epub.EpubHtml(
            uid=f"page_{i}",
            file_name=f"OEBPS/pages/page_{i}.xhtml",
            content=img_html
        )
        livro.add_item(page_item)
        paginas.append(page_item)

    livro.add_item(epub.EpubNcx())
    livro.add_item(epub.EpubNav())

    livro.spine = ["nav"] + paginas

    epub_path = os.path.join(diretorio_manga, f"{manga_nome.capitalize()}_Cap_{capitulo_num}.epub")
    epub.write_epub(epub_path, livro, {})
    print(f"EPUB criado com sucesso: {epub_path}")

def processar_capitulo(url, headers, diretorio_base):
    try:
        manga_nome, capitulo_num = extrair_info_url(url)
        print(f"{manga_nome} - Capítulo {capitulo_num} encontrado, iniciando download.")

        diretorio_manga = os.path.join(diretorio_base, manga_nome)
        os.makedirs(diretorio_manga, exist_ok=True)

        img_files = baixar_imagens(url, headers)
        if img_files:
            criar_epub(manga_nome, capitulo_num, img_files, diretorio_manga)
        else:
            print("Nenhuma imagem foi baixada.")
    except Exception as e:
        print(f"Erro ao processar {url}: {e}")

def main():
    lista_urls = [
        "https://mangalivre.ru/manga/one-piece/capitulo-502/",
        "https://mangalivre.ru/manga/one-piece/capitulo-503/",
        ###Adicionar mais links conforme o desejado.....
        ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    diretorio_base = r"C:\Users\SeuNome\Mangas"

    for url in lista_urls:
        processar_capitulo(url, headers, diretorio_base)

if __name__ == "__main__":
    main()