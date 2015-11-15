var React    = require('react');
var ReactDOM = require('react-dom');


var Repo = React.createClass({
  getInitialState: function() {
    return {
      forks    : "-",
      watchers : "-",
      fork     : "-",
      stars    : "-",
      total    : 0
    }
  },
  componentDidMount: function() {
    $.get('https://api.github.com/repos/mariuscoto/' + this.props.name, function(res) {
      if (this.isMounted()) {
        this.setState({
          forks    : res.forks,
          watchers : res.watchers_count,
          stars    : res.stargazers_count,
          fork     : res.fork ? res.parent.url : null,
          total    : res.watchers_count * PointsList.watch + res.stargazers_count * PointsList.star
        });
      }
    }.bind(this));
  },

  render: function() {
    return (
      <li>{this.props.name} [{this.state.total}]
        <ul>
          <li>Forked: {this.state.fork}</li>
          <li>Forks: {this.state.forks}</li>
          <li>Stars: {this.state.stars}</li>
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

        <PointsList />
      </div>
    );
  }
});


var PointsList = React.createClass({
  statics: {
    watch : 10,
    star  : 20
  },

  render: function() {
    return (
      <div>
        <h2>Points:</h2>
        <ul>
          <li>Watcher: {PointsList.watch}p</li>
          <li>Star: {PointsList.star}p</li>
        </ul>
      </div>
    );
  }
});


ReactDOM.render(<RepoList />, document.getElementById("main"));
