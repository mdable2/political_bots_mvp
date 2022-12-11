// MessageParser starter code
class MessageParser {
    constructor(actionProvider, state) {
      this.actionProvider = actionProvider;
      this.state = state;
    }
  
    async parse(message) {
      if (this.state.talkingTo === "biden") {
        console.log("talking to biden");
        const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({"person": "Biden", "query": message})
        };

        const response = await fetch("http://localhost:8000/chat", requestOptions);
        const data = await response.json()
        const msg = this.actionProvider.createChatBotMessage(data.response);
        this.actionProvider.updateChatbotState(msg, "biden");
        const m = {
          "to": "biden",
          "msg": message,
          "explain": data.explainability
        }
        this.actionProvider.props.props.changeQueryText(JSON.stringify(m));

      }
      else { // talking to trump in this block
        console.log("talking to trump");
        const m = {
          "to": "trump",
          "msg": message
        }
        this.actionProvider.props.props.changeQueryText(JSON.stringify(m));
        const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({"person": "Trump", "query": message})
        };

        const response = await fetch("http://localhost:8000/chat", requestOptions);
        const data = await response.json()
        const msg = this.actionProvider.createChatBotMessage(data.response);
        this.actionProvider.updateChatbotState(msg, "trump");
      }
    }
  }
  
  export default MessageParser;