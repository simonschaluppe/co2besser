
from app import app, db, add_drexel_to_db
from app.models import Test, Action

@app.shell_context_processor
def make_shell_context():
    return {
        "db":db,
        "Test":Test,
        "Action":Action,
        "add_drexel_to_db": add_drexel_to_db}

if __name__ == '__main__':
    print("lol")
    #app.run()
    #a = app.database.data

