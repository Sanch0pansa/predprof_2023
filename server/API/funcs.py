import json
def getData(request):
    if 'multipart/form-data' in request.content_type:
        return request.POST
    elif 'application/json' in request.content_type:
        return json.loads(request.body)