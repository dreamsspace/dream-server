from server.schema.user import User, gen_key


def test_user_schema_passwords():
    user1 = User(name='name', password='foobar')

    assert user1.valid_password('foobar')
    assert not user1.valid_password('foobar1')
