import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import Chatbot from 'react-chatbot-kit';
import 'react-chatbot-kit/build/main.css';

import ActionProvider from './chatbot/ActionProvider';
import MessageParser from './chatbot/MessageParser';
import config from './chatbot/config';

import { connect } from 'react-redux';
import { changeQueryText } from './actions/query';
import { bindActionCreators } from 'redux';
import { useSelector } from 'react-redux';

const App = (props) => {
  let listExplain = <p>{props.query.query}</p>;
  if (props.query.query !== "") {
    const data_json = JSON.parse(props.query.query);
    console.log(data_json.explain);
    listExplain = data_json.explain.map((d) => <li key={d.location}>{"Location: " + d.location + " ======= Message: " + d.text}</li>);
  }

  return (
    <div className="App">
      <header className="App-header">
        <div className="main-container">
          <p className='divider'>Hello and welcome to political bots! She aint pretty, but she works. You are able to chat with the AI form of Joe Biden and Donald Trump. The bots were only trained this weekend so their responses are sometimes not the best, but next to it you'll see an attempt at explaining why that response was given. Explainability is complete with where the remark was given and said remark. Hope you enjoy!</p>
          <Chatbot className="divider" config={config} actionProvider={ActionProvider} messageParser={MessageParser} props={props} />
          <div className="list-items">
            {listExplain}
          </div>
        </div>
      </header>
    </div>
  );
}

const mapStateToProps = state => ({
  query: state.query
});

const ActionCreators = Object.assign(
  {},
  changeQueryText,
);

// const mapDispatchToProps = dispatch => ({
//   actions: bindActionCreators(ActionCreators, dispatch)
// });

// export default connect(mapStateToProps, mapDispatchToProps)(App);
const mapDispatchToProps = dispatch => {
  return {
    changeQueryText: query => dispatch(changeQueryText(query))
  }
};

export default connect(mapStateToProps, mapDispatchToProps)(App);
