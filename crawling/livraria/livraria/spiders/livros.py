import scrapy
from scrapy import selector
from scrapy.http import request
from ..items import LivrariaItem

# Definindo domínio e URL inicial
class LivrosSpider(scrapy.Spider):
    name = 'livros'
    allowed_domains = ['books.toscrape.com/']
    start_urls = ['https://books.toscrape.com/']

    # Efetuando looping de URLs das categorias para acessá-los
    def parse(self, response):
        urls = response.xpath("//div[@class='side_categories']/ul/li/ul/li/a/@href")
        for url in urls:
            yield response.follow(url.get(), callback=self.parse_livros, dont_filter=True)
        
    # Efetuando o looping para preencher as colunas
    def parse_livros(self, response):
        item = LivrariaItem()
        quadros_livro = response.xpath("//li[@class='col-xs-6 col-sm-4 col-md-3 col-lg-3']")
        categorias = response.xpath("//div[@class='side_categories']")
        for quadro in quadros_livro:
            item['livro'] = quadro.xpath(".//article[@class='product_pod']/h3/a/@title").get()
            item['categoria'] = categorias.xpath(".//ul[@class='nav nav-list']/li/ul/li/a/strong/text()").get()
            item['estrela'] = quadro.xpath(".//article[@class='product_pod']/p/@class").get()[12:]
            item['preco'] = quadro.xpath("//div[@class='product_price']/p/text()").get()
            item['estoque'] = quadro.xpath(".//div[@class='product_price'] /p[2]/@class").get()
            yield item
        # Caso houver um botão 'nexet', ir para a próxima página
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse_livros, dont_filter=True)