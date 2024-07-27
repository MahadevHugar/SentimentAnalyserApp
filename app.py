from flask import Flask, render_template, request
import openai

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    message=''
    if request.method == 'POST':
        sentence = request.form.get('sentence')
        openai.api_key = ("openai.api_key")
        def analyze_sentiment(prompt):
            chunks = [prompt[i:i+4096] for i in range(0, len(prompt), 4096)]
            completions = []
            
            for chunk in chunks:
             completion = openai.Completion.create(
                engine="text-davinci-002",
                prompt="decide the sentiment whether it is positive or negetive or neutral :"+chunk,
                max_tokens=1024,
                stop=None,
                temperature=0.5   
    
            )
            completions.append(completion)

            message = completions[0].choices[0].text
            return message
        message = analyze_sentiment(sentence)
        return render_template('index.html', message=message)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



import React, { useState } from 'react';
import { LuSend } from 'react-icons/lu';
import './Home.css';

function Paraphrase() {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');

  const handleMessageSubmit = async (e) => {
    e.preventDefault();

    if (userInput) {
      const userMessage = { text: userInput, sender: 'user' };
      const response = await sendRequest(userInput);

      setMessages((prevMessages) => [
        ...prevMessages,
        userMessage,
        { text: response.paraphrased_answer, sender: 'bot' },
      ]);

      setUserInput('');
    }
  };

  const sendRequest = async (query) => {
    const response = await fetch('/paraphrase', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    const data = await response.json();
    return data;
  };

  const renderMessages = () => {
    return messages.map((message, index) => (
      <div
        key={index}
        className={`message ${message.sender === 'user' ? 'user' : 'bot'}`}
      >
        {message.sender === 'user' && (
          <img className="avatar" src="/User.png" alt="User Avatar" />
        )}
        {message.sender === 'bot' && (
          <img className="avatar1" src="/Bot.png" alt="Bot Avatar" />
        )}
        <div className="message-text">{message.text}</div>
      </div>
    ));
  };

  return (
    <div>
      <div className="box">
        <div className="conversation-container">{renderMessages()}</div>
      </div>
      <form className="user-input-form" onSubmit={handleMessageSubmit}>
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="Enter your message here"
          className="user-input"
        />
        <button type="submit" className="send-button">
          <LuSend />
        </button>
      </form>
    </div>
  );
}

export default Paraphrase;
