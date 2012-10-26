from functools import wraps
from lazysusan.plugins import CommandPlugin


def get_sender_id(data):
    if data['command'] == 'speak':
        return data['userid']
    elif data['command'] == 'pmmed':
        return data['senderid']
    else:
        raise Exception('Unrecognized command type `{0}`'
                        .format(data['command']))


def moderator_required(function):
    """Indicate a moderator is required to invoke the specified function.

    If the sending user is not a moderator, a private message will be returned
    to them indicating such.
    """
    @wraps(function)
    def wrapper(cls, *args, **kwargs):
        if isinstance(cls, CommandPlugin):
            bot = args[0]
            data = args[2]
        else:  # Support the built-in commands
            bot = cls
            data = args[1]

        user_id = get_sender_id(data)
        # Verify the user is a moderator
        if user_id not in bot.moderator_ids:
            message = 'You must be a moderator to execute that command.'
            return bot.bot.pm(message, user_id)
        return function(cls, *args, **kwargs)
    wrapper.func_dict['moderator_required'] = True
    return wrapper
