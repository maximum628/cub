var React    = require('react');
var ReactDOM = require('react-dom');


var Repo = React.createClass({
  getInitialState: function() {
    return {
      forks    : "-",
      watchers : "-",
      fork     : "-"
    }
  },
  componentDidMount: function() {
    $.get('https://api.github.com/repos/mariuscoto/' + this.props.name, function(res) {
      if (this.isMounted()) {
        this.setState({
          forks    : res.forks,
          watchers : res.watchers,
          fork     : res.fork ? res.parent.url : null
        });
      }
    }.bind(this));
  },

  render: function() {
    return (
      <li>{this.props.name}
        <ul>
          <li>Forked: {this.state.fork}</li>
          <li>Forks: {this.state.forks}</li>
          <li>Watchers: {this.state.watchers}</li>
        </ul>
      </li>
    )
  }
})


var RepoList = React.createClass({
  getInitialState: function() {
      return {
        repos: []
      }
  },

  componentDidMount: function() {
    $.get('https://api.github.com/users/mariuscoto/repos', function(res) {
      if (this.isMounted()) {
        this.setState({
          repos: res
        });
      }
    }.bind(this));
  },

  render: function() {
    return (
      <div>
        <h2>Repos:</h2>
        <ul>
        { this.state.repos.map(function(repo, i) {
          return (<Repo key={i} name={repo.name} />)
        }, this)}
        </ul>
      </div>
    );
  }
});


ReactDOM.render(<RepoList />, document.getElementById("main"));
