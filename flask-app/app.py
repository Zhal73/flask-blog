from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return """
        "Hello internet!!!!"
        <p>
        <a href="../example">Example</a>
        </p>
        """
@app.route('/')
@app.route('/example')
def example():
    return """
        <!DOCTYPE html>
        <html>
        <body>

        <h1>My First Heading</h1>
        <p>My first paragraph.</p>
        <p>I am very good at this!!! (not)</p>
        <a href="../home">Home </a>
        </body>
        </html>
        """
