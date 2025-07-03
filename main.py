from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Store messages and other data
messages = []
cookie = ""
haters_name = ""
speed = 1
thread_id = ""
stop_thread = False

# Function to send messages
def send_message(message):
    try:
        # Implement your messaging logic here
        # For example, using Facebook's API or another platform's API
        print(f"Sending message: {message}")
    except Exception as e:
        print(f"Error sending message: {e}")

# Route for sending messages
@app.route('/send_messages', methods=['POST'])
def send_messages():
    global cookie, haters_name, speed, thread_id, messages, stop_thread
    try:
        cookie = request.form.get('cookie')
        haters_name = request.form.get('haters_name')
        speed = int(request.form.get('speed'))
        thread_id = request.form.get('thread_id')
        messages = request.form.get('messages').splitlines()
        stop_thread = False
        for message in messages:
            if stop_thread:
                break
            send_message(message)
            time.sleep(speed)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Route for stopping messages
@app.route('/stop_messages', methods=['POST'])
def stop_messages():
    global stop_thread
    try:
        stop_thread = True
        print("Stopping messages...")
        return jsonify({'status': 'stopped'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Send Messages</title>
<style>
    /* Your CSS styles here */
body {
    font-family: Arial, sans-serif;
    background-color: #f2f2f2;
}

.container {
    width: 50%;
    margin: 40px auto;
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

label {
    display: block;
    margin-bottom: 10px;
}

input[type="text"], input[type="number"], textarea {
    width: 100%;
    height: 40px;
    margin-bottom: 20px;
    padding: 10px;
    border: 1px solid #ccc;
}

textarea {
    height: 100px;
}

input[type="submit"] {
    background-color: #3498db;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

input[type="submit"]:hover {
    background-color: #2980b9;
}

#stop-button {
    background-color: #e74c3c;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

#stop-button:hover {
    background-color: #c0392b;
}

</style>

    </head>
    <body>
        <h1>D3VI E2E Messages</h1>
        <form id="send-messages-form">
            <label for="cookie">Cookie:</label>
            <input type="text" id="cookie" name="cookie"><br><br>
            <label for="haters_name">Haters Name:</label>
            <input type="text" id="haters_name" name="haters_name"><br><br>
            <label for="speed">Speed:</label>
            <input type="number" id="speed" name="speed" value="1"><br><br>
            <label for="thread_id">Thread ID:</label>
            <input type="text" id="thread_id" name="thread_id"><br><br>
            <label for="messages">Messages:</label>
            <textarea id="messages" name="messages" rows="5" cols="30"></textarea><br><br>
            <input type="submit" value="Send Messages">
        </form>
        <button id="stop-button" onclick="stopMessages()">Stop Messages</button>
        <script>
            const form = document.getElementById('send-messages-form');
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const formData = new FormData(form);
                fetch('/send_messages', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error(error));
            });

            function stopMessages() {
                fetch('/stop_messages', {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error(error));
            }
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(port=5000)
