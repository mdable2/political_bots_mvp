// Config starter code
import { createChatBotMessage } from "react-chatbot-kit";
import SelectOptions from "./SelectOptions";

const config = { 
  botName: "Political Bot",
  initialMessages: [createChatBotMessage("Hi, who would you like to talk with?", {
    widget: "selectOptions"
  })],
  widgets: [
    {
      widgetName: "selectOptions",
      widgetFunc: (props) => <SelectOptions {...props} />,
    },
  ],
  customStyles: {
    botMessageBox: {
      backgroundColor: "#376B7E",
    },
    chatButton: {
      backgroundColor: "#376B7E",
    },
  },
}

export default config
