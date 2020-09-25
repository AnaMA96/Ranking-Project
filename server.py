from controllers import labcontroller, studentcontroller
from app import app
import os
from dotenv import load_dotenv
load_dotenv()

PORT = os.getenv("PORT")
app.run("0.0.0.0", PORT, debug=True)