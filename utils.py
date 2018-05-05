from wit import Wit

server_access_token = "IS2YDEXM3B65KRF6T5TS5JFRKUWGGUP5"
client = Wit(access_token=server_access_token)


def wit_response(message_text):
    resp = client.message(message_text)
    entity = None
    value = None

    try:
        entity = list(resp['entities'])[0]
        value = resp['entities'][entity][0]['value']
    except:
        pass

    return entity, value



