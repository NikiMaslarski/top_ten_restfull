import sqlite3
 
 
class DBHolder:
 
    def __init__(self):
        conn = sqlite3.connect('ladder.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS ladder (team TEXT, score INTEGER)')
        c.execute('CREATE TABLE IF NOT EXISTS HOSTINFO (hostname TEXT, ipadr TEXT, port INTEGER)')
        c.close()
 
    def update_score(self, team, new_score):
        conn = sqlite3.connect('ladder.db')
        c = conn.cursor()
        old_score = self.get_score(team)
 
        c.execute("SELECT * FROM ladder WHERE team='{}'".format(team))
 
        if not c.fetchone():
            return False
 
        else:
            # self.c.execute("UPDATE ladder SET score='{}' WHERE team='{}'".format(new_score + old_score, team))
            c.execute("UPDATE ladder SET score='{}' WHERE team='{}'".format(max(new_score, old_score), team))
            conn.commit()            
            c.close()
            return True
 
    def add_score_to_ladder(self, team, score):
        conn = sqlite3.connect('ladder.db')
        c = conn.cursor()
        c.execute("SELECT * FROM ladder WHERE team='{}'".format(team))
 
        if not c.fetchone():
            c.execute("INSERT INTO ladder VALUES('{}', '{}')".format(team, score))
            conn.commit()
            c.close()
            return True
 
        else:
            conn.commit()
            c.close()
            return False
 
    def remove_team_from_ladder(self, team):
        conn = sqlite3.connect('ladder.db')
        c = conn.cursor()
        c.execute("DELETE FROM ladder WHERE team='{}'".format(team))
        conn.commit()
        c.close()
 
    def get_score(self, team):
        conn = sqlite3.connect('ladder.db')
        c = conn.cursor()
        c.execute("SELECT score FROM ladder WHERE team='{}'".format(team))
        return (c.fetchone()[0])
 
    def get_top10(self):
        conn = sqlite3.connect('ladder.db')
        c = conn.cursor()
        c.execute("SELECT * FROM ladder ORDER BY score DESC LIMIT 10")
        return c.fetchall()

#-------------------

    def get_hosts(self):
        conn = sqlite3.connect('ladder.db')
        c = conn.cursor()
        c.execute("SELECT * FROM HOSTINFO")
        return c.fetchall()

    def create_host(self, hostname, ipadr, port):
        conn = sqlite3.connect('ladder.db')
        c = conn.cursor()
        c.execute("SELECT * FROM HOSTINFO WHERE hostname='{}'".format(hostname))
 
        if not c.fetchone():
            c.execute("INSERT INTO HOSTINFO VALUES('{}', '{}', '{}')".format(hostname, ipadr, port))
            conn.commit()
            c.close()
            return True
 
        else:
            conn.commit()
            c.close()
            return False

    def get_host_info(self, hostname):
        conn = sqlite3.connect('ladder.db')
        c = conn.cursor()
        c.execute("SELECT * FROM HOSTINFO WHERE hostname='{}'".format(hostname))
        return c.fetchone()