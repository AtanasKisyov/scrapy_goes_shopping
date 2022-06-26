import scrapy
import json

from scrapy_goes_shoping.utils import utils

class ScrapyGoesShopping(scrapy.Spider):

    name = 'spider'
    start_urls = [
        utils.start_url,
    ]

    def parse(self, response):

        yield scrapy.Request(
            utils.similar_clothing_url,
            callback=self.parse_json,
            headers=utils.similar_clothing_headers,
        )
    
    def parse_json(self, response):

        raw_data = response.body
        serialized_data = json.loads(raw_data)[utils.similars_key]
        result = []

        for product in serialized_data:
            name = product[utils.description_key]
            price = product[utils.color_key][utils.price_key][utils.price_key]
            color = product[utils.color_key][utils.id]
            size = product[utils.color_key][utils.size_key]

            result.append({
                'name': name,
                'color': color,
                'price': price,
                'size': size,
            })
    
        with open(utils.result_file, utils.write_mode) as file:
            json.dump(result, file, indent=utils.json_indent_value)

        yield response
