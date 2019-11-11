import json

import requests
from behave import given, when, then
from behave.runner import Context


@given('I create a couple of exchange tokens to use the Hallebarde file transfer services')
def given_create_an_exchange(context: Context):
    r = requests.post('https://dev.api.bda.ninja/exchanges',
                      headers={
                          'Authorization': context.authorization_token
                      })
    context.exchange = json.loads(r.text)


@when('I ask for all my exchanges')
def when_getting_all_exchanges(context: Context):
    r = requests.get('https://dev.api.bda.ninja/exchanges',
                     headers={
                         'Authorization': context.authorization_token
                     })
    context.all_exchanges = json.loads(r.text)


@when('I revoke this exchange')
def when_revoking_an_exchange(context: Context):
    requests.delete(
        url='https://dev.api.bda.ninja/exchanges',
        headers={
            'Authorization': context.authorization_token,
            'exchange_identifier': context.exchange['identifier']
        })


@then('the exchange I created is included in the list')
def then_checking_created_exchange_exists(context: Context):
    assert context.exchange['identifier'] in [exchange['identifier'] for exchange in context.all_exchanges]


@then('the exchange I created is not included in the list')
def then_checking_created_exchange_does_not_exists(context: Context):
    assert context.exchange['identifier'] not in [exchange['identifier'] for exchange in context.all_exchanges]
