import arrow


def is_decayed(db, server_id, user_id):
    day_in_seconds = 86400  # Duh...
    try:
        decay_rate = db.get_settings(server_id, 'WarnDecay')
    except:
        db.set_settings(server_id, 'WarnDecay', 1)
        decay_rate = 1
    decay_addition = decay_rate * day_in_seconds
    warned_users = db.get_settings(server_id, 'WarnedUsers')
    user_warn_data = warned_users[user_id]
    last_warn_timestamp = user_warn_data['Timestamp']
    decay_barrier = decay_addition + last_warn_timestamp
    decayed = False
    if arrow.utcnow().timestamp > decay_barrier:
        decayed = True
    return decayed
