from flask import Flask

from routes.main_routes import main_bp
from routes.chatbot_routes import chatbot_bp

app = Flask(
    __name__,
    template_folder="../client/templates",
    static_folder="../client/static"
)

app.register_blueprint(main_bp)
app.register_blueprint(chatbot_bp)

if __name__ == "__main__":
    app.run(debug=True)