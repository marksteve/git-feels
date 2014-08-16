/** @jsx React.DOM */

var React = require('react/addons');


var Report = React.createClass({
  componentDidUpdate: function() {
    if (this.props.data) {
      $('> li', this.refs.sentiments.getDOMNode())
        .velocity('transition.expandIn', {
          stagger: 200
        });
    }
  },
  render: function() {
    var data = this.props.data;
    if (!data) {
      return null;
    }
    var sentiments = data.sentiments.map(function(data, i) {
      return <Sentiment key={i} data={data} />;
    });
    return (
      <div className="report">
        <h2>{data.repo_name}</h2>
        <ul
          ref="sentiments"
          className="sentiments"
        >
          {sentiments}
        </ul>
      </div>
    );
  }
});


var Sentiment = React.createClass({
  render: function() {
    var data = this.props.data;
    return (
      <li className="sentiment">
        <img src={data.avatar} />
        <h3>
          {data.name}
        </h3>
        <ul>
          <li>{data.username}</li>
        </ul>
        <div className="happy score">
          +20
        </div>
      </li>
    );
  }
});


var App = React.createClass({
  submit: function(e) {
    e.preventDefault();
    this.setState({
      report: {
        repo_name: 'marksteve/drake',
        sentiments: [
          {
            name: 'Mark Steve Samson',
            username: 'marksteve',
            avatar: '//lorempixel.com/64/64/people'
          },
          {
            name: 'Mark Steve Samson',
            username: 'marksteve',
            avatar: '//lorempixel.com/64/64/people'
          }
        ]
      }
    });
  },
  getInitialState: function() {
    return {
      report: null
    };
  },
  componentDidMount: function() {
    this.refs.userRepo.getDOMNode().focus();
  },
  render: function() {
    return (
      <form onSubmit={this.submit}>
        <h1>git feels</h1>
        <p>
          <input
            ref="userRepo"
            type="text"
            placeholder="marksteve/drake"
          />
        </p>
        <Report data={this.state.report} />
      </form>
    );
  }
});


React.renderComponent(
  <App />,
  document.body
);
