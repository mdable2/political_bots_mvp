// ActionProvider starter code
class ActionProvider {
    constructor(
     createChatBotMessage,
     setStateFunc,
     createClientMessage,
     stateRef,
     createCustomMessage,
     props,
     ...rest
   ) {
     this.createChatBotMessage = createChatBotMessage;
     this.setState = setStateFunc;
     this.createClientMessage = createClientMessage;
     this.stateRef = stateRef;
     this.createCustomMessage = createCustomMessage;
     this.props = props;
   }
   handleBidenClick = () => {
    const message = this.createChatBotMessage(
      "Ok! Start talking to Biden by asking him a question now.",
    );

    this.updateChatbotState(message, "biden");
  };
  handleTrumpClick = () => {
    const message = this.createChatBotMessage(
      "Ok! Start talking to Trump by asking him a question now.",
    );

    this.updateChatbotState(message, "trump");
  };


  updateChatbotState(message, talkingTo) {
    this.setState((prevState) => ({
      ...prevState,
      messages: [...prevState.messages, message],
      talkingTo: talkingTo
    }));
  }
}
 
 export default ActionProvider;
 