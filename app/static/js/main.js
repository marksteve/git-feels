/** @jsx React.DOM */

var React = require('react/addons');

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
  },
  getInitialState: function() {
    return {
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
    };
  },
  componentDidMount: function() {
    this.refs.userRepo.getDOMNode().focus();
    $('> li', this.refs.sentiments.getDOMNode())
      .velocity('transition.expandIn', {
        stagger: 200
      });
  },
  render: function() {
    var sentiments = this.state.sentiments.map(function(data) {
      return <Sentiment data={data} />;
    });
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
        <h2>{this.state.repo_name}</h2>
        <ul
          ref="sentiments"
          className="sentiments"
        >
          {sentiments}
        </ul>
      </form>
    );
  }
});


React.renderComponent(
  <App />,
  document.body
);
