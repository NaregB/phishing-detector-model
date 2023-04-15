import json
import numpy as np
from joblib import load


def lambda_handler(event, context):
    method = event['httpMethod']

    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': json.dumps({
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            })
        }

    if method != 'POST':
        return {
            'statusCode': 400,
            'body': json.dumps({
                "error": "Only POST requests are supported",
            })
        }

    # Get the POST data from the input event
    post_data = json.loads(event['body'])

    required_params = [
        'text_link_disparity',
        're_mail',
        'urls',
        'body_richness',
        'contains_prime_targets',
        'contains_account',
        'domains',
        'HTML',
        'malicious_urls',
        'ip_urls',
        'general_salutation',
        'attachments',
        'dots_count',
        'hex_urls',
        'mailto',
        'contains_update',
        'contains_access',
    ]

    model_data = []
    missing_data = []

    # validate
    for param in required_params:
        data = post_data.get(param, None)
        if data is None:  # data can be 0, so can't be checked with not
            missing_data.append(param)
        else:
            model_data.append(data)

    if len(missing_data):
        return {
            'statusCode': 400,
            'body': json.dumps({
                "error": "missing required params",
                "params": missing_data
            })
        }

    # load model
    model = load('./PhishingModel.joblib')

    # predict
    predict = model.predict(np.array([model_data])).tolist()[0]

    # Return the response in JSON format
    return {
        'statusCode': 200,
        'body': json.dumps({
            "result": predict
        })
    }
