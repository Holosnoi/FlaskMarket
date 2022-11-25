from market import app
import os

# print(os.urandom(12).hex())

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)

