from irv.poll import *


class PollExistsError(Exception):
    pass


class PollNotFoundError(Exception):
    pass


class InvalidUserError(Exception):
    pass


_polls = []

_users = {
    "Alice": {
        "points": 1,
        "delegate": ""
    },
    "Bob": {
        "points": 1,
        "delegate": ""
    },
    "Steve": {
        "points": 1,
        "delegate": ""
    },
    "Jim": {
        "points": 1,
        "delegate": ""
    }
}


def register(poll):
    if any([poll.get_name() == p.get_name() for p in _polls]):
        raise PollExistsError()

    _polls.append(poll)


def unregister(name: str):
    global _polls
    _polls = list(filter(lambda p: False if p.get_name() == name else True, _polls))


def get(name: str):
    for poll in _polls:
        if poll.get_name() == name:
            return poll

    raise PollNotFoundError()


# noinspection PyShadowingNames
def _check_circular(user: str, delegate: str):
    """
    Checks whether a delegation would cause a circular dependency.
    This is important because a circular dependency would cause the vote counting
    process to hang.

    :param user: The user delegating their vote
    :param delegate: The user to whom the vote is being delegated
    :return: False if the delegation would cause a circular dependency, or True otherwise
    """

    chain = [user]
    cur = delegate

    # There's probably a faster way to do this, so feel free to change it if you figure it out.
    while len(cur) != 0:
        if cur in chain:
            return False

        chain.append(cur)
        prev = cur

        # IDE complains for some reason, but REPL confirms it's valid... hmmmmm...
        cur = _users[prev]["delegate"]

    return True


def undelegate(user: str):
    """
    Revokes a user's delegation.
    :param user: The user revoking their delegation
    """

    cur = user
    # noinspection PyShadowingNames
    while len(delegate := _users[cur]["delegate"]) != 0:
        cur = delegate

    _users[cur]["points"] -= _users[user]["points"]


# noinspection PyShadowingNames
def delegate(user: str, delegate: str):
    """
    Transfers all "voting points" from user to delegate,
    including any votes that were delegated to Alice by other users.

    :param user: The user delegating their vote
    :param delegate: The user to whom the vote is being delegated
    :return -1 if the delegation would cause a circular dependency, or 0 otherwise
    :except InvalidUserError if either user was invalid
    """

    if not _check_circular(user, delegate):
        return -1

    # If the user already had a delegate, revoke their points
    if len(_users[user]["delegate"]) != 0:
        undelegate(user)
        # _users[_users[user]["delegate"]]["points"] -= _users[user]["points"]

    _users[user]["delegate"] = delegate

    # Recursion isn't safe here; we might blow the stack
    prev = user
    cur = delegate
    while len(cur) != 0:
        _users[cur]["points"] += _users[prev]["points"]

        prev = cur
        cur = _users[prev]["delegate"]
