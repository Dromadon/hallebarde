import json
from http import HTTPStatus

import requests
from behave import when, then
from behave.runner import Context


@when('I ask for a presigned upload url with this exchange upload token')
def when_asking_for_pre_signed_upload_url(context: Context):
    r = requests.get(
        url='https://dev.api.bda.ninja/s3_presigned_upload_url',
        headers={
            'Authorization': context.exchange['upload_token']
        },
        params={'filename': 'a_filename'}
    )
    context.pre_signed_upload_url_response = r
    assert HTTPStatus.OK == r.status_code, f'HTTP code received is {r.status_code} :('


@when("I can upload a file")
def then_a_file_can_be_uploaded(context: Context):
    pre_signed_url = json.loads(context.pre_signed_upload_url_response.text)
    context.file_data = b'arandombinarycontent'

    form_data = pre_signed_url['fields'].copy()
    form_data['file'] = context.file_data
    r = requests.post(url=pre_signed_url['url'], files=form_data)
    assert HTTPStatus.NO_CONTENT == r.status_code, f'HTTP code received is {r.status_code} :('


@then('I ask for a presigned download url with this exchange download token')
def when_asking_for_pre_signed_download_url(context: Context):
    r = requests.get(
        url='https://dev.api.bda.ninja/s3_presigned_download_url',
        headers={
            'Authorization': context.exchange['download_token']
        })
    context.pre_signed_download_url_response = r
    assert HTTPStatus.OK == r.status_code, f'HTTP code received is {r.status_code} :('


@then("I can download a file")
def then_a_file_can_be_downloaded(context: Context):
    pre_signed_url = context.pre_signed_download_url_response.text
    r = requests.get(url=pre_signed_url)
    assert HTTPStatus.OK == r.status_code, f'HTTP code received is {r.status_code} :('
    assert r.content == context.file_data
