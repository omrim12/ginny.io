import os
import logging
from prettytable import PrettyTable
from py_edamam import Edamam
from constants import (
    TABLE_COLUMN_WIDTH
)
from urllib3.exceptions import HTTPError

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def edamam_api_recipes_client():
    try:
        return Edamam(
            recipes_appid=os.environ['RECIPES_API_ID'],
            recipes_appkey=os.environ['RECIPES_API_SECRET'],
        )
    except KeyError as key_err:
        LOGGER.error(f"Recipes API credentials are missing: {key_err}")
        raise


def edamam_api_food_client():
    try:
        return Edamam(
            food_appid=os.environ['FOOD_API_ID'],
            food_appkey=os.environ['FOOD_API_CREDENTIALS']
        )
    except KeyError as key_err:
        LOGGER.error(f"Food API credentials are missing: {key_err}")
        raise


def parse_recipes_data(recipes_raw):
    # init recipes table with headers
    recipes_table = PrettyTable()
    recipes_table.field_names = [
        'Recipe name',
        'Cuisine',
        'Recipe source'
    ]

    # parse recipes from raw content
    for recipe in recipes_raw:
        # parse recipe info
        recipe_name = recipe['recipe']['label']
        recipe_cuisine = recipe['recipe']['cuisineType'][0]
        recipe_source = recipe['recipe']['url']

        # add to recipes table
        recipes_table.add_row([
            recipe_name,
            recipe_cuisine,
            recipe_source
        ])

    # adjust table columns width
    recipes_table._max_width = {
        f"Column {i+1}: {TABLE_COLUMN_WIDTH}"
        for i in range(len(recipes_table.field_names))
    }

    return recipes_table


def parse_food_data(food_raw):
    # TODO: optionally parse food data callback
    return PrettyTable()


def get_recipes_info(food_label):
    """
    :param food_label:
    :return:
    """
    # init api client instance
    recipes_api_client = edamam_api_recipes_client()

    try:
        # query edamam api food and recipes according to given label
        recipes_callback = recipes_api_client.search_recipe(food_label)

        # create table
        recipes_table = parse_recipes_data(recipes_callback['hits'])

        return recipes_table

    except HTTPError as http_err:
        LOGGER.error(f"Failed to establish connection with API: {http_err}")


def get_food_info(food_label):
    """
    :param food_label:
    :return:
    """
    # init api client instances
    food_api_client = edamam_api_food_client()

    try:
        # query edamam api food and recipes according to given label
        food_callback = food_api_client.search_food(food_label)

        # create table
        food_table = parse_food_data(food_callback)

        return food_table

    except HTTPError as http_err:
        LOGGER.error(f"Failed to establish connection with API: {http_err}")
