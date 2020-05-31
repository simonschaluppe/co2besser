
from app import app

@app.shell_context_processor
def make_shell_context():
    return {
        # "db":db
    }

if __name__ == '__main__':
    print("lol")
    #app.run()
    #a = app.database.data

