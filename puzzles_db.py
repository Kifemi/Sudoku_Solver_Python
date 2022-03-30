import sqlite3
import json
import settings
import datetime
import pytz


db_conn = sqlite3.connect("puzzles_db.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)


def initialize_db():
    db_conn.execute("CREATE TABLE IF NOT EXISTS puzzles (_id INTEGER PRIMARY KEY, name TEXT NOT NULL,"
                    " puzzle TEXT NOT NULL, time TIMESTAMP NOT NULL)")
    preset_puzzles = {"easy": json.dumps(settings.puzzle_easy),
                      "normal": json.dumps(settings.puzzle_normal),
                      "hard": json.dumps(settings.puzzle_hard),
                      "very hard": json.dumps(settings.puzzle_very_hard),
                      "empty": json.dumps(settings.puzzle_empty),
                      "impossible": json.dumps(settings.puzzle_impossible),
                      "anti backtracking": json.dumps(settings.puzzle_anti_backtracking),
                      }
    current_time = pytz.utc.localize(datetime.datetime.utcnow())
    insert_stmt = ("INSERT INTO puzzles (name, puzzle, time) SELECT ?, ?, ?"
                   " WHERE NOT EXISTS (SELECT 1 FROM puzzles WHERE name = ?)")

    for key, value in preset_puzzles.items():
        db_conn.execute(insert_stmt, (key, value, current_time, key))
    db_conn.commit()


def load_puzzle(id):
    puzzle = db_conn.execute("SELECT puzzle FROM puzzles WHERE _id = ?", (id,))
    return json.loads(puzzle.fetchone()[0])


def load_puzzles():
    puzzles = db_conn.execute("SELECT name FROM puzzles")
    return puzzles


def check_name(name):
    get_names = ("SELECT name FROM puzzles WHERE name = ?")
    names = db_conn.execute(get_names, (name,)).fetchone()
    return False if names else True


def add_puzzle(name, puzzle):
    insert_stmt = ("INSERT INTO puzzles (name, puzzle, time) SELECT ?, ?, ?"
                   " WHERE NOT EXISTS (SELECT 1 FROM puzzles WHERE name = ?)")

    current_time = pytz.utc.localize(datetime.datetime.utcnow())
    value = json.dumps(puzzle)
    db_conn.execute(insert_stmt, (name, value, current_time, name))
    db_conn.commit()


def close_db():
    db_conn.close()
