import json

import requests
from behave import when, then
from behave.runner import Context


@when('I ask for a presigned upload url with this exchange upload token')
def when_asking_for_pre_signed_upload_url(context: Context):
    r = requests.get(
        url='https://dev.api.bda.ninja/s3_presigned_upload_url',
        headers={
            'Authorization': context.exchange['upload_token']
        })
    context.pre_signed_url_response = r
    assert 200 == r.status_code, f'HTTP code received is {r.status_code} :('


@then("I can upload a file")
def then_a_file_can_be_uploaded(context: Context):
    pre_signed_url = json.loads(context.pre_signed_url_response.text)
    form_data = pre_signed_url['fields'].copy()
    form_data['file'] = b'arandombinarycontent'
    r = requests.post(url=pre_signed_url['url'], files=form_data)
    assert 204 == r.status_code, f'HTTP code received is {r.status_code} :('
