from flask import Flask, json
import spotify

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


def retain_attributes(object, attribute_names):
    result={}
    for name in attribute_names:
        if name in object:
            result[name] = object[name]

    return result

def get_current_user():
    return spotify.get_me()


def get_my_albums(all_data=False):
    if all_data:
        return [album_item['album'] for album_item in spotify.get_my_albums()['items']]

    return [retain_attributes(album_item['album'], ['id', 'name', 'uri', 'images']) for album_item in spotify.get_my_albums()['items']]

def get_my_playlists():
    return [playlist_item for playlist_item in spotify.get_my_playlists()['items']]

def get_all():
    return {
        'user': get_current_user(),
        'albums': get_my_albums(),
        'playlists': get_my_playlists()
    }

@app.route('/playlists/<id>')
def get_playlist(id):
    data = get_my_playlist(id)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/albums/<id>')
def get_album(id):
    albums = get_my_albums(all_data=True)
    data = next(iter([album for album in albums if album['id'].encode('utf-8')==id]), None)

    if not data:
        return app.response_class(
            response=json.dumps({'errorMessage': 'Album not found'}),
            status=400,
            mimetype='application/json'
        )

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/albums')
def get_albums():
    data = get_my_albums(all_data=True)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/playlists')
def get_playlists():
    data = get_my_playlists()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/')
def root():
    data = get_all()
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == "__main__":
    app.run(port=8015)
