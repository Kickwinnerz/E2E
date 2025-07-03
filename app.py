from flask import Flask, request, jsonify
import time
import requests
import threading

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
    # Implement your messaging logic here
    # For example, using Facebook's API or another platform's API
    print(f"Sending message: {message}")

# Route for sending messages
@app.route('/send_messages', methods=['POST'])
def send_messages():
    global cookie, haters_name, speed, thread_id, messages, stop_thread
    cookie = request.form.get('cookie')
    haters_name = request.form.get('haters_name')
    speed = int(request.form.get('speed'))
    thread_id = request.form.get('thread_id')
    messages = request.form.get('messages').splitlines()
    stop_thread = False
    
    # Start sending messages in a separate thread
    threading.Thread(target=send_messages_thread).start()
    
    return jsonify({'status': 'success'})

def send_messages_thread():
    global stop_thread
    for message in messages:
        if stop_thread:
            break
        send_message(message)
        time.sleep(speed)

# Route for stopping messages
@app.route('/stop_messages', methods=['POST'])
def stop_messages():
    global stop_thread
    stop_thread = True
    print("Stopping messages...")
    return jsonify({'status': 'stopped'})

@app.route('/')
def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>D3VI KING</title>
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
    /* Your CSS styles here */
  body {
    font-family: 'Roboto', sans-serif;
    margin: 0;
    padding: 20px;
    width: 350px;
    background-color: #212121; /* Dark gray */
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.container {
    flex: 1;
    padding: 20px;
    background-color: #333; /* Dark gray */
    border-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.form-control {
    outline: none;
    border: 1px solid #555; /* Dark gray */
    background-color: #444; /* Dark gray */
    width: 100%;
    height: 40px;
    padding: 7px;
    margin-bottom: 20px;
    border-radius: 10px;
    color: #fff;
}

.form-control:focus {
    border-color: #666; /* Dark gray */
    box-shadow: 0px 0px 10px rgba(102, 102, 102, 0.2);
}

#sendBtn {
    background-color: #03A9F4; /* Blue */
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

#sendBtn:hover {
    background-color: #039BE5;
}

#stopBtn {
    background-color: #E91E63; /* Pink */
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

#stopBtn:hover {
    background-color: #C2185B;
}

footer {
    text-align: center;
    padding: 10px;
    background-color: #333;
    color: #fff;
    border-top: 1px solid #ddd;
}
  </style>
</head>
<body>
    <header class="header mt-4">
        <h3>
            <span class="material-icons">auto_awesome</span> D3VI KING
        </h3>
    </header>
    <div class="container text-center">
        <form action="/send_messages" method="post">
            <div class="mb-3">
                <label for="cookie">Enter Your id Cookies:</label>
                <input type="text" id="cookie" name="cookie" class="form-control" placeholder="Enter Cookies Name">
            </div>
            <div class="mb-3">
                <label for="HatersName">Enter Your HaterSName(SiiNgle):</label>
                <input type="text" id="HatersName" name="haters_name" class="form-control" placeholder="Enter Haters Name">
            </div>
            <div class="mb-3">
                <label for="messageText">Enter Messages To Send (One Per line):</label>
                <textarea class="form-control" id="messageText" name="messages" rows="5" placeholder="Enter your messages here..."></textarea>
            </div>
            <div class="mb-3">
                <label for="speed">Enter Speed (seconds between messages):</label>
                <input type="number" id="speed" name="speed" class="form-control" placeholder="Delay in seconds" min="1" value="1">
            </div>
            <div class="mb-3">
                <label for="threadId">Enter Thread ID:</label>
                <input type="text" id="threadId" name="thread_id" class="form-control" placeholder="Enter Thread ID">
            </div>
            <input type="submit" id="sendBtn" value="Submit">
        </form>
        <button id="stopBtn" onclick="stopMessages()">Stop Sending Messages</button>
        <script>
            function stopMessages() {
                fetch('/stop_messages', { method: 'POST' });
            }
        </script>
    </div>
    <footer>
        <span class="material-icons">code</span> Developed by <span class="author">Devi King</span> <span class="material-icons">favorite</span>
    </footer>
</body>
</html>

              """
 if __name__ == '__main__':
    app.run(debug=True)            