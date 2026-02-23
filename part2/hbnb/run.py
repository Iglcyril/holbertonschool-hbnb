#task0
# 6.Create the Entry Point
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)