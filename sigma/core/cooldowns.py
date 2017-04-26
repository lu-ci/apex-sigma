import arrow


class Cooldown(object):
    def __init__(self):
        self.cooldowns = {}

    # cmd_server_usr:
    def on_cooldown(self, cmd, message):
        cd_name = f'{cmd}_{message.author.id}'
        if cd_name in self.cooldowns:
            time_now = arrow.utcnow().timestamp
            cd_expires = self.cooldowns[cd_name]
            if time_now > cd_expires:
                on_cd = False
            else:
                on_cd = True
        else:
            on_cd = False
        return on_cd

    def set_cooldown(self, cmd, message, time):
        cd_name = f'{cmd}_{message.author.id}'
        time_now = arrow.utcnow().timestamp
        self.cooldowns.update({cd_name: time_now + time})

    def get_cooldown(self, cmd, message):
        if not self.on_cooldown(cmd, message):
            cooldown = 0
        else:
            cd_name = f'{cmd}_{message.author.id}'
            time_now = arrow.utcnow().timestamp
            cd_expires = self.cooldowns[cd_name]
            cooldown = cd_expires - time_now
        return cooldown
