# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# Definindo as colunas
class LivrariaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    livro = scrapy.Field()
    categoria = scrapy.Field()
    estrela = scrapy.Field()
    preco = scrapy.Field()
    estoque = scrapy.Field()
