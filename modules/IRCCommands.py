def send_pong(con, msg):
    con.send('PONG %s\r\n' % msg)


def send_message(con, chan, msg):
    con.send('PRIVMSG %s :%s\r\n' % (chan, msg))
    print("BOT: " + msg)


def send_nick(con, nick):
    con.send('NICK %s\r\n' % nick)


def send_pass(con, password):
    con.send('PASS %s\r\n' % password)


def join_channel(con, chan):
    con.send('JOIN %s\r\n' % chan)


def part_channel(con, chan):
    con.send('PART %s\r\n' % chan)

