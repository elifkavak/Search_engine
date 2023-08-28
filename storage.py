import sqlite3
import pandas as pd

class DBStorage():
    def __init__(self):
        self.con = sqlite3.connect("links.db")
        self.setup_tables()

    def setup_tables(self):
        cursor = self.con.cursor()
        results_table= r"""
            CREATE TABLE IF NOT EXISTS results(
                id INTEGER PRIMARY KEY,
                query TEXT,
                rank INTEGER,
                link TEXT,
                title TEXT,
                snippet TEXT,
                html TEXT,
                created DATETIME,
                relevance INTEGER,
                UNIQUE(query, link)
            ); 
        """

        cursor.execute(results_table)
        self.con.commit()
        cursor.close()

    def query_results(self, query):
        df = pd.read_sql(f"select * from results where query='{query}' order by rank asc;", self.con)
        return df

    def insert_row(self, values):
        cursor = self.con.cursor()
        try:
            cursor.execute("INSERT INTO results (query, rank, link, title, snippet, html, created) VALUES(?,?,?,?,?,?,?)", values)
            self.con.commit()
        except sqlite3.IntegrityError:
            pass
        cursor.close()

    def update_relevance(self, query, link, relevance):
        cur = self.con.cursor()
        cur.execute('UPDATE results SET relevance=? WHERE query=? AND link=?', [relevance, query, link])
        self.con.commit()
        cur.close()
