import sqlite3
 
 
class DBHolder:
 
    def __init__(self):
        conn = sqlite3.connect('ladder.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS ladder (team TEXT, score INTEGER)')
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
        c.close()
 
    def get_top10(self):
        conn = sqlite3.connect('ladder.db')
        c = conn.cursor()
        c.execute("SELECT * FROM ladder ORDER BY score DESC LIMIT 10")
        return c.fetchall()
        c.close()