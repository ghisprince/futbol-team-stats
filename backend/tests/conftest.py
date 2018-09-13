import pytest

from app import create_app
from app.models import db, User, Role, Team, get_or_create


@pytest.fixture()
def testapp(request):
    app = create_app('app.settings.TestConfig')
    client = app.test_client()

    db.app = app
    db.create_all()

    if getattr(request.module, "create_user", True):
        admin = get_or_create(db.session, User,  username='admin', password='supersafepassword')
        admin.teams.append(get_or_create(db.session, Team, name='a team'))
        admin.teams.append(get_or_create(db.session, Team, name='b team'))
        admin.roles.append(get_or_create(db.session, Role, name="editor"))
        db.session.add(admin)
        db.session.commit()

    if getattr(request.module, "login_user", True):
        client.post('/login',
                     data=dict(username='admin',
                               password="supersafepassword"),
                     follow_redirects=True)


    def teardown():
        db.drop_all()
        db.session.remove()

    request.addfinalizer(teardown)

    return client
