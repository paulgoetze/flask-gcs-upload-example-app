import json
from http import HTTPStatus

from my_app.users.models import User
from tests.support import helpers


def test_avatar_upload(user, client):
    """Test uploading an avatar image for a user"""

    avatar = helpers.load_file_data('test.png')

    response = client.post(
        f'/users/{user.id}/avatar',
        data={'avatar': avatar},
        content_type='multipart/form-data'
    )

    data = response.json
    assert response.status_code == HTTPStatus.CREATED
    assert data['data']['attributes']['avatar'] == user.avatar.url
    assert data['data']['attributes']['avatar_small'] == user.avatar.thumb_32x32_url
    assert data['data']['attributes']['avatar_medium'] == user.avatar.thumb_128x128_url


def test_avatar_upload_with_missing_user(client):
    """Test uploading an avatar image for a not available user"""

    avatar = helpers.load_file_data('test.png')

    response = client.post(
        '/users/-1/avatar',
        data={'avatar': avatar},
        content_type='multipart/form-data'
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_avatar_upload_with_missing_file(user, client):
    """Test uploading an avatar without sending a file"""

    response = client.post(
        f'/users/{user.id}/avatar',
        data={},
        content_type='multipart/form-data'
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_avatar_upload_with_invalid_mime_type(user, client):
    """Test uploading an avatar with invalid MIME type"""

    avatar = helpers.load_file_data('test.gif')

    response = client.post(
        f'/users/{user.id}/avatar',
        data={'avatar': avatar},
        content_type='multipart/form-data'
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_background_upload(user, client):
    """Test uploading an background image for a user"""

    background = helpers.load_file_data('test.png')

    response = client.post(
        f'/users/{user.id}/background',
        data={'profile_background': background},
        content_type='multipart/form-data'
    )

    data = response.json
    assert response.status_code == HTTPStatus.CREATED
    assert data['data']['attributes']['profile_background'] == user.profile_background.url


def test_background_upload_with_missing_user(client):
    """Test uploading an background image for a not available user"""

    background = helpers.load_file_data('test.png')

    response = client.post(
        '/users/-1/background',
        data={'profile_background': background},
        content_type='multipart/form-data'
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_background_upload_with_missing_file(user, client):
    """Test uploading an background without sending a file"""

    response = client.post(
        f'/users/{user.id}/background',
        data={},
        content_type='multipart/form-data'
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_background_upload_with_invalid_mime_type(user, client):
    """Test uploading an background with invalid MIME type"""

    background = helpers.load_file_data('test.gif')

    response = client.post(
        f'/users/{user.id}/background',
        data={'profile_background': background},
        content_type='multipart/form-data'
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_all_users(session, client):
    """Test getting all users"""

    user_a = User(email='user-a@example.com')
    user_b = User(email='user-b@example.com')

    session.add(user_a)
    session.add(user_b)
    session.commit()

    response = client.get('/users', content_type='application/json')
    data = response.json['data']
    assert isinstance(data, list)
    assert len(data) == 2


def test_get_user(user, client):
    """Test getting a user"""

    response = client.get(f'/users/{user.id}', content_type='application/json')
    data = response.json['data']
    assert data['type'] == 'users'
    assert data['id'] == user.id
    assert data['attributes']['email'] == user.email


def test_create_a_user(client):
    """Test creating a user"""

    assert User.query.count() == 0

    email = 'user@example.com'
    response = client.post(
        '/users',
        data=json.dumps({'email': email}),
        content_type='application/json',
    )
    data = response.json

    assert response.status_code == HTTPStatus.CREATED
    assert User.query.filter_by(email=email).count() == 1
    assert data['data']['attributes']['email'] == email


def test_create_a_duplicate_user(user, client):
    """Test creating an already existing user"""

    response = client.post(
        '/users',
        data=json.dumps({'email': user.email}),
        content_type='application/json'
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_updating_a_user(user, client):
    """Test updating a user"""

    email = user.email
    assert User.query.filter_by(email=email).count() == 1

    new_email = f'new-{email}'
    response = client.put(
        f'/users/{user.id}',
        data=json.dumps({'email': new_email}),
        content_type='application/json',
    )
    data = response.json

    assert response.status_code == HTTPStatus.OK
    assert user.email == new_email
    assert User.query.filter_by(email=email).count() == 0
    assert data['data']['id'] == user.id
    assert data['data']['attributes']['email'] == new_email


def test_updating_a_not_existing_user(client):
    """Test updating a not existing user"""

    assert User.query.count() == 0

    response = client.put(
        '/users/-1',
        data=json.dumps({'email': 'email@example.com'}),
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert User.query.count() == 0


def test_deleting_a_user(user, client):
    """Test deleting a user"""

    response = client.delete(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert User.query.get(user.id) is None


def test_deleting_a_not_existing_user(client):
    """Test deleting a not existing user"""

    response = client.delete('/users/0')
    assert response.status_code == HTTPStatus.NOT_FOUND
