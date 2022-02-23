import sqlite3
import pickle
import settings
import datetime
import pytz


db_conn = sqlite3.connect("puzzles_db.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)


def initialize_db():
    db_conn.execute("CREATE TABLE IF NOT EXISTS puzzles (_id INTEGER PRIMARY KEY, name TEXT NOT NULL,"
                    " puzzle INTEGER NOT NULL, time TIMESTAMP NOT NULL)")
    preset_puzzles = {"easy": pickle.dumps(settings.puzzle_easy),
                      "normal": pickle.dumps(settings.puzzle_normal),
                      "hard": pickle.dumps(settings.puzzle_hard),
                      "very hard": pickle.dumps(settings.puzzle_very_hard),
                      "empty": pickle.dumps(settings.puzzle_empty),
                      "impossible": pickle.dumps(settings.puzzle_impossible),
                      "anti backtracking": pickle.dumps(settings.puzzle_anti_backtracking),
                      }

    current_time = pytz.utc.localize(datetime.datetime.utcnow())
    insert_stmt = ("INSERT INTO puzzles (name, puzzle, time) SELECT ?, ?, ?"
                   " WHERE NOT EXISTS (SELECT 1 FROM puzzles WHERE name = ?)")

    for key, value in preset_puzzles.items():
        db_conn.execute(insert_stmt, (key, value, current_time, key))
    db_conn.commit()


def load_puzzle():
    puzzle = db_conn.execute("SELECT puzzle FROM puzzles WHERE name = ?", ("easy",))
    return pickle.loads(puzzle.fetchone()[0])


def close_db():
    db_conn.close()
