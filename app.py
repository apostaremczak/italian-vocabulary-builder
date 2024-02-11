import aiohttp
import asyncio
import logging
from dataclasses import dataclass
from flask import Flask, render_template, redirect, url_for, request

from vocab_builder.api_client import ApiClient
from vocab_builder.app_config import parse_config_from_credentials
from vocab_builder.coniugazione.coniugazione_client import ConiugazioneClient
from vocab_builder.pons.pons_api_client import PonsApiClient
from vocab_builder.translation_config import get_translation_config
from vocab_builder.treccani.treccani_client import TreccaniClient

app = Flask(__name__)

# Read credentials for APIs
credentials = parse_config_from_credentials()
# Translation config - determines which language to translate to
translation_config = get_translation_config()

# Configure logging
logging.basicConfig(level=logging.DEBUG)


@dataclass
class SearchResults:
    translation: str
    definition: str
    conjugation: str


# Basic in-memory cache
word_cache: dict[str, SearchResults] = {}


async def get_results(word):
    if word in word_cache:
        logging.info(f"Serving results for '{word}' from cache")
        return word_cache[word]

    pons_client = PonsApiClient(credentials.pons_api_secret, translation_config)
    translation = await pons_client.fetch_data(word)

    coniugazione_client = ConiugazioneClient()
    conjugation = await coniugazione_client.fetch_data(word)

    treccani_client = TreccaniClient()
    definition = await treccani_client.fetch_data(word)

    result = SearchResults(
        translation=translation.to_html(),
        definition=definition.to_html(),
        conjugation=conjugation.to_html()
    )
    word_cache[word] = result
    return result


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_word = request.form['search_word']
        return redirect(url_for('search', word=search_word))
    return render_template('index.html')


@app.route('/search/<word>')
async def search(word: str):
    # Perform asynchronous API calls to fetch results
    results = await get_results(word)

    # Render the template with the extracted results
    return render_template(
        'search_results.html',
        word=word,
        pons_result=results.translation,
        treccani_result=results.definition,
        conjugation=results.conjugation
    )
