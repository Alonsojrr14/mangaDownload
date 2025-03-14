# Manga EPUB Downloader

Um script em Python que baixa capítulos de mangás de um site específico e os converte em arquivos EPUB, organizando as imagens dentro de um livro digital.

## 📌 Funcionalidades
- Extração automática do nome do mangá e do número do capítulo a partir da URL.
- Download das imagens do capítulo.
- Conversão das imagens em um arquivo EPUB formatado corretamente.
- Organização dos arquivos EPUB em diretórios específicos para cada mangá.

## 🔧 Pré-requisitos
Antes de executar o script, certifique-se de ter as seguintes bibliotecas Python instaladas:

```bash
pip install requests beautifulsoup4 ebooklib pillow
```

## 🚀 Como Usar
1. **Configurar a lista de URLs**
   - No arquivo `main()`, adicione as URLs dos capítulos que deseja baixar na variável `lista_urls`.

2. **Executar o script**
   - Execute o script Python:
   
   ```bash
   python script.py
   ```

3. **Acessar os arquivos EPUB**
   - Os arquivos EPUB gerados estarão no diretório especificado na variável `diretorio_base`.

## 📁 Estrutura do Projeto
```
/
│── MangaReader.py            # Código principal
│── README.md            # Este arquivo
```

## ⚙️ Configuração
### Diretório de Download
Altere a variável `diretorio_base` para definir onde os arquivos EPUB serão salvos. Exemplo:
```python
diretorio_base = r"C:\Users\SeuNome\Mangas"
```

### Cabeçalhos HTTP
Caso o site bloqueie requisições, pode ser necessário atualizar os cabeçalhos `headers` para simular um navegador:
```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
```

## ⚠️ Possíveis Erros e Soluções
- **Nenhuma imagem encontrada**: O site pode ter alterado sua estrutura, tente verificar se as classes HTML ainda correspondem.
- **Erro de conexão**: Certifique-se de que a URL está correta e que você tem acesso ao site.
- **EPUB não abre corretamente**: Verifique se todas as imagens foram baixadas corretamente.

## 📜 Licença
Este projeto é de uso livre para fins educacionais e pessoais. Não deve ser utilizado para distribuição ilegal de conteúdo protegido por direitos autorais.

---
✉️ Para dúvidas ou sugestões, entre em contato!

