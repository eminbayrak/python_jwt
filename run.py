from app import create_app
from app.auth import auth_blueprint

app = create_app()
app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
