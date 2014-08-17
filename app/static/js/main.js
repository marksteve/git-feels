/** @jsx React.DOM */

var React = require('react/addons');
var superagent = require('superagent');


var Report = React.createClass({
  componentDidUpdate: function() {
    if (this.props.data) {
      $('> li', this.refs.authors.getDOMNode())
        .hide()
        .velocity('transition.bounceIn', {
          duration: 500,
          stagger: 100
        });
    }
  },
  render: function() {
    var data = this.props.data;
    if (!data) {
      return null;
    }
    var authors = data.authors.map(function(data) {
      return <Author key={data.id} data={data} />;
    });
    return (
      <div className="report">
        <h2>{data.repo_name}</h2>
        <ul
          ref="authors"
          className="authors"
        >
          {authors}
        </ul>
      </div>
    );
  }
});


var Author = React.createClass({
  componentDidMount: function() {
    $('.sentiment .pie', this.getDOMNode())
      .peity('pie', {
        diameter: 64,
        fill: ["#ccffaa", "#ffcccc"]
      });
  },
  render: function() {
    var data = this.props.data;
    var pie;
    if (!data.pos && !data.neg) {
      pie = '1/2';
    } else if (!data.pos) {
      pie = '0/1';
    } else if (!data.neg) {
      pie = '1/1';
    } else {
      pie = data.pos + '/' + (data.pos + data.neg);
    }
    return (
      <li className="author">
        <img src={data.avatar_url} />
        <h3>
          {data.name || data.login}
        </h3>
        <ul>
          <li>Profanities: {data.profanities}</li>
        </ul>
        <div
          className="sentiment"
          title={
            "Positive: " + data.pos.toFixed(2) + "\n" +
            "Negative: " + data.neg.toFixed(2)
          }
        >
          <span className="pie">
            {pie}
          </span>
        </div>
      </li>
    );
  }
});


var App = React.createClass({
  submit: function(e) {
    e.preventDefault();
    superagent
      .post('/analyze')
      .send({
        user_repo: this.refs.userRepo.getDOMNode().value
      })
      .end(this.setReport);
    this.setState({
      title: 'gitting feels...',
      report: null
    });
  },
  setReport: function(res) {
    if (res.error) {
      this.setState({
        title: ':('
      });
    }
    this.setState({
      title: 'git feels',
      report: res.body.report
    });
  },
  getInitialState: function() {
    return {
      title: 'git feels',
      report: null
    };
  },
  componentDidMount: function() {
    this.refs.userRepo.getDOMNode().focus();
  },
  render: function() {
    return (
      <form onSubmit={this.submit}>
        <h1>{this.state.title}</h1>
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
