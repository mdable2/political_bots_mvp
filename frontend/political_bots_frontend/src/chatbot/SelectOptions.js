import React from "react";

import "./SelectOptions.css";

const SelectOptions = (props) => {
  const options = [
    { text: "Joe Biden", handler: props.actionProvider.handleBidenClick, id: 1 },
    { text: "Donald Trump", handler: props.actionProvider.handleTrumpClick, id: 2 },
  ];

  const optionsMarkup = options.map((option) => (
    <button
      className="learning-option-button"
      key={option.id}
      onClick={option.handler}
    >
      {option.text}
    </button>
  ));

  return <div className="learning-options-container">{optionsMarkup}</div>;
};

export default SelectOptions;