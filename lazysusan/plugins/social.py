from lazysusan.helpers import (display_exceptions, admin_or_moderator_required,
                               no_arg_command, single_arg_command)
from lazysusan.plugins import CommandPlugin

import pdb


class Social(CommandPlugin):
    COMMANDS = {'/followme': 'follow_user' }

    @display_exceptions
    def follow_user(self, message, data):
        userId = data['senderid']
        if self.idToStalk is None:
            self.idToStalk = userId
            self.bot.reply("I'm sticking with you!",  data)
            self.followUser(userId)
        elif self.idToStalk == userId:
            if message == "no more":
                self.bot.reply("You've changed. I'm not following you any more!", data)
                self.idToStalk = None
            else:
                self.bot.reply("I'm already following you!", data)
                self.followUser(self.idToStalk)

    @display_exceptions
    def __init__(self, *args, **kwargs):
        super(Social, self).__init__(*args, **kwargs)
        self.idToStalk = None
        self.register('deregistered', self.onUserLeft)
        #self.register('registered', self.onUserLeft)


    @display_exceptions
    def followUser(self, userId):
        print "Following user %s" % (userId)
        #Register the switch room to the callback
        self.bot.api.stalk(userId, True, 
                           lambda data: self.switchRoom(data['roomId']))

    @display_exceptions
    def switchRoom(self, roomid):
        print "Registering in %s" % (roomid)
        self.bot.api.roomRegister(roomid)

    @display_exceptions
    def onUserLeft(self, data):
        for userData in data['user']:
            if userData['userid'] == self.idToStalk:
                self.followUser(self.idToStalk)
