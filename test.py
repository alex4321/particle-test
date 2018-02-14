import argparse
import requests
import json


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-host')
    parser.add_argument('-port')
    return parser.parse_args()


def _validate_response(name, response, status_code, data, postprocessing=lambda s: s):
    print(name)
    response_status_code = response.status_code
    response_data = json.loads(response.text)
    print("Returned by API:", response.status_code, response_data)
    if response_status_code != status_code:
        print("Wrong status code, must be {0}\n".format(status_code))
        exit(1)
    if postprocessing(response_data) != data:
        print("Wrong data, must be {0}\n".format(data))
        exit(1)
    return response_data


if __name__ == '__main__':
    args = get_arguments()
    BASE_URL = 'http://{0}:{1}'.format(args.host, args.port)

    user1_resp = requests.post(BASE_URL + '/user')
    user1_resp_data = _validate_response("USER1",
                                         user1_resp,
                                         200,
                                         {
                                           'success': True,
                                           'result': {
                                               'uid': "<class 'int'>"
                                           }
                                       },
                                         lambda resp: {
                                           'success': resp['success'],
                                           'result': {
                                               'uid': str(type(resp['result']['uid']))
                                           }
                                       })
    user1_uid = user1_resp_data['result']['uid']

    user2_resp = requests.post(BASE_URL + '/user')
    user2_resp_data = _validate_response("USER2",
                                         user2_resp,
                                         200,
                                         {
                                           'success': True,
                                           'result': {
                                               'uid': "<class 'int'>"
                                           }
                                       },
                                         lambda resp: {
                                           'success': resp['success'],
                                           'result': {
                                               'uid': str(type(resp['result']['uid']))
                                           }
                                       })
    user2_uid = user2_resp_data['result']['uid']

    user3_resp = requests.post(BASE_URL + '/user')
    user3_resp_data = _validate_response("USER3",
                                         user3_resp,
                                         200,
                                         {
                                           'success': True,
                                           'result': {
                                               'uid': "<class 'int'>"
                                           }
                                       },
                                         lambda resp: {
                                           'success': resp['success'],
                                           'result': {
                                               'uid': str(type(resp['result']['uid']))
                                           }
                                       })
    user3_uid = user3_resp_data['result']['uid']

    _validate_response("U1_FOLLOW_U2",
                       requests.post(BASE_URL + '/follow', data={'follower': user1_uid,
                                                               'target': user2_uid}),
                       200,
                       {
                         'success': True,
                         'result': {
                             'follower': {'uid': user1_uid},
                             'target': {'uid': user2_uid}
                         }
                     })

    _validate_response("U2_POST1",
                       requests.post(BASE_URL + '/post', data={'author': user2_uid,
                                                             'body': 'Test1'}),
                       200,
                       {
                         'success': True,
                         'result': {
                             'id': "<class 'int'>",
                             'author': {'uid': user2_uid},
                             'body': 'Test1',
                             'unix_timestamp': "<class 'float'>",
                             'reply_to_message': None
                         }
                     },
                       lambda response: {
                         'success': response['success'],
                         'result': {
                             'id': str(type(response['result']['id'])),
                             'author': {'uid': response['result']['author']['uid']},
                             'body': response['result']['body'],
                             'unix_timestamp': str(type(response['result']['unix_timestamp'])),
                             'reply_to_message': response['result']['reply_to_message']
                         }
                     })

    _validate_response("U1_TIMELINE",
                       requests.get(BASE_URL + '/timeline', params={'user': user1_uid,
                                                                  'max_messages': 100}),
                       200,
                       {
                         'success': True,
                         'result': [
                             {'id': "<class 'int'>",
                              'author': {'uid': "<class 'int'>"},
                              'body': 'Test1',
                              'unix_timestamp': "<class 'float'>",
                              'reply_to_message': None
                            }
                         ]
                     },
                       lambda response: {
                         'success': response['success'],
                         'result': [
                             {'id': str(type(message['id'])),
                              'author': {'uid': str(type(message['author']['uid']))},
                              'body': message['body'],
                              'unix_timestamp': str(type(message['unix_timestamp'])),
                              'reply_to_message': None
                            }
                            for message in response['result']
                         ]
                     }, )

    user3_message = _validate_response("U3_POST1",
                                       requests.post(BASE_URL + '/post', data={'author': user3_uid,
                                                             'body': 'Test2'}),
                                       200,
                                       {
                         'success': True,
                         'result': {
                             'id': "<class 'int'>",
                             'author': {'uid': user3_uid},
                             'body': 'Test2',
                             'unix_timestamp': "<class 'float'>",
                             'reply_to_message': None
                         }
                     },
                                       lambda response: {
                         'success': response['success'],
                         'result': {
                             'id': str(type(response['result']['id'])),
                             'author': {'uid': response['result']['author']['uid']},
                             'body': response['result']['body'],
                             'unix_timestamp': str(type(response['result']['unix_timestamp'])),
                             'reply_to_message': response['result']['reply_to_message']
                         }
                     })
    user3_mid = user3_message['result']['id']

    _validate_response("U1_TIMELINE2",
                       requests.get(BASE_URL + '/timeline', params={'user': user1_uid,
                                                                  'max_messages': 100}),
                       200,
                       {
                         'success': True,
                         'result': [
                             {'id': "<class 'int'>",
                              'author': {'uid': "<class 'int'>"},
                              'body': 'Test1',
                              'unix_timestamp': "<class 'float'>",
                              'reply_to_message': None
                            }
                         ]
                     },
                       lambda response: {
                         'success': response['success'],
                         'result': [
                             {'id': str(type(message['id'])),
                              'author': {'uid': str(type(message['author']['uid']))},
                              'body': message['body'],
                              'unix_timestamp': str(type(message['unix_timestamp'])),
                              'reply_to_message': None
                            }
                            for message in response['result']
                         ]
                     }, )
    _validate_response("U2_POST2",
                       requests.post(BASE_URL + '/post', data={'author': user2_uid,
                                                             'body': 'Test3',
                                                             'reply_to': user3_mid}),
                       200,
                       {
                         'success': True,
                         'result': {
                             'id': "<class 'int'>",
                             'author': {'uid': user2_uid},
                             'body': 'Test3',
                             'unix_timestamp': "<class 'float'>",
                             'reply_to_message': {
                                 'id': user3_mid,
                                 'author': None,
                                 'body': None,
                                 'unix_timestamp': None,
                                 'reply_to_message': None
                             }
                         }
                     },
                       lambda response: {
                         'success': response['success'],
                         'result': {
                             'id': str(type(response['result']['id'])),
                             'author': {'uid': response['result']['author']['uid']},
                             'body': response['result']['body'],
                             'unix_timestamp': str(type(response['result']['unix_timestamp'])),
                             'reply_to_message': response['result']['reply_to_message']
                         }
                     })

    _validate_response("U1_TIMELINE3",
                       requests.get(BASE_URL + '/timeline', params={'user': user1_uid,
                                                                  'max_messages': 100}),
                       200,
                       {
                         'success': True,
                         'result': [
                             {'id': "<class 'int'>",
                              'author': {'uid': "<class 'int'>"},
                              'body': 'Test1',
                              'unix_timestamp': "<class 'float'>",
                              'reply_to_message': None
                            }
                         ]
                     },
                       lambda response: {
                         'success': response['success'],
                         'result': [
                             {'id': str(type(message['id'])),
                              'author': {'uid': str(type(message['author']['uid']))},
                              'body': message['body'],
                              'unix_timestamp': str(type(message['unix_timestamp'])),
                              'reply_to_message': None
                            }
                            for message in response['result']
                         ]
                     }, )

    _validate_response("U1_FOLLOW_U3",
                       requests.post(BASE_URL + '/follow', data={'follower': user1_uid,
                                                               'target': user3_uid}),
                       200,
                       {
                         'success': True,
                         'result': {
                             'follower': {'uid': user1_uid},
                             'target': {'uid': user3_uid}
                         }
                     })

    _validate_response("U1_TIMELINE4",
                       requests.get(BASE_URL + '/timeline', params={'user': user1_uid,
                                                                  'max_messages': 100}),
                       200,
                       {
                         'success': True,
                         'result': [
                             {'id': "<class 'int'>",
                              'author': {'uid': user2_uid},
                              'body': 'Test3',
                              'unix_timestamp': "<class 'float'>",
                              'reply_to_message': None},
                             {'id': "<class 'int'>",
                              'author': {'uid': user3_uid},
                              'body': 'Test2',
                              'unix_timestamp': "<class 'float'>", 'reply_to_message': None},
                             {'id': "<class 'int'>",
                              'author': {'uid': user2_uid},
                              'body': 'Test1',
                              'unix_timestamp': "<class 'float'>",
                              'reply_to_message': None}]}
                       ,
                       lambda response: {
                         'success': response['success'],
                         'result': [
                             {'id': str(type(message['id'])),
                              'author': {'uid': message['author']['uid']},
                              'body': message['body'],
                              'unix_timestamp': str(type(message['unix_timestamp'])),
                              'reply_to_message': None
                            }
                            for message in response['result']
                         ]
                     }, )

    _validate_response("U1_TIMELINE4",
                       requests.get(BASE_URL + '/timeline', params={'user': user1_uid,
                                                                  'max_messages': 1}),
                       200,
                       {
                         'success': True,
                         'result': [
                             {'id': "<class 'int'>",
                              'author': {'uid': user2_uid},
                              'body': 'Test3',
                              'unix_timestamp': "<class 'float'>",
                              'reply_to_message': None}]}
                       ,
                       lambda response: {
                         'success': response['success'],
                         'result': [
                             {'id': str(type(message['id'])),
                              'author': {'uid': message['author']['uid']},
                              'body': message['body'],
                              'unix_timestamp': str(type(message['unix_timestamp'])),
                              'reply_to_message': None
                            }
                            for message in response['result']
                         ]
                     }, )
