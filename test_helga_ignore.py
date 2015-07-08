# -*- coding: utf8 -*-
from mock import patch

import helga_ignore as ignore


def test_preprocessor_does_nothing():
    with patch.object(ignore, 'ignored', set()):
        chan, nick, msg = ignore.ignore_preprocessor('#bots', 'me', 'foo')
        assert msg == 'foo'


def test_preprocessor_blanks_message_when_ignored():
    with patch.object(ignore, 'ignored', set(['me'])):
        chan, nick, msg = ignore.ignore_preprocessor('#bots', 'me', 'foo')
        assert msg == ''


def test_command_list():
    with patch.object(ignore, 'ignored', set(['me', 'you'])):
        resp = ignore.ignore_command('#bots', 'me', 'foo', 'ignore', ['list'])
        assert resp == 'Currently ignoring the following users: me, you'


def test_command_add_cannot_ignore_self():
    resp = ignore.ignore_command('#bots', 'me', 'foo', 'ignore', ['add', 'me'])
    assert resp == "I'm sorry me, but you can't ignore yourself"


def test_command_add_cannot_ignore_operator():
    with patch.object(ignore.settings, 'OPERATORS', ['you']):
        resp = ignore.ignore_command('#bots', 'me', 'foo', 'ignore', ['add', 'you'])
        assert resp == "I'm sorry me, but I can't ignore an operator"


def test_command_add_cannot_ignore_already_ignored():
    with patch.object(ignore, 'ignored', set(['you'])):
        resp = ignore.ignore_command('#bots', 'me', 'foo', 'ignore', ['add', 'you'])
        assert resp == "I'm already ignoring you"


def test_command_add():
    resp = ignore.ignore_command('#bots', 'me', 'foo', 'ignore', ['add', 'you'])
    assert resp == 'Added you to the ignore list'


def test_command_remove_not_ignoring():
    resp = ignore.ignore_command('#bots', 'me', 'foo', 'ignore', ['remove', 'you'])
    assert resp == 'Removed you from the ignore list'


def test_command_remove():
    with patch.object(ignore, 'ignored', set(['you'])):
        resp = ignore.ignore_command('#bots', 'me', 'foo', 'ignore', ['remove', 'you'])
        assert resp == 'Removed you from the ignore list'
