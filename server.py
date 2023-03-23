from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher


@dispatcher.add_method
def foobar(**kwargs):
    return kwargs["foo"] + kwargs["bar"]


@dispatcher.add_method(name='getQty')
def getQty():
    f = open('products.txt', 'r')
    content = f.readlines()
    buffer = '{ "product": [ '
    for line in content:
        # print(line)

        contentElement = line.split(",")[2]
        print(contentElement)
        buffer += contentElement + ','
    buffer = buffer[:-1]
    buffer += ']}'
    print(buffer)

    import json
    return json.loads(buffer)


@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher["echo"] = lambda s: s
    dispatcher["add"] = lambda a, b: a + b

    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, application)
