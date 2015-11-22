var React    = require('react');
var ReactDOM = require('react-dom');

var USER = 'mariuscoto'


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
    $.get('https://api.github.com/repos/' + this.props.user + '/' + this.props.name, function(res) {
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
    $.get('https://api.github.com/users/' + this.props.user + '/repos', function(res) {
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
          return (<Repo user={this.props.user} key={i} name={repo.name} />)
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


var Profile = React.createClass({
  getInitialState: function() {
      return {
        avatar_url : null,
        name       : null,
        username   : null,
        email      : null
      }
  },

  componentDidMount: function() {
    $.get('https://api.github.com/users/' + this.props.user, function(res) {
      if (this.isMounted()) {
        this.setState({
          avatar_url : res.avatar_url,
          name       : res.name,
          username   : res.login,
          email      : res.email
        });
      }
    }.bind(this));
  },

  render: function() {
    return (
      <div id='profile'>
        <div id='profile-avatar'>
          <img className='avatar' src={this.state.avatar_url}></img>
        </div>
        <div id='profile-info'>
          <div id='profile-name'>{this.state.name}</div>
          <div id='profile-username'>
            <a href={'http://github.com/' + this.state.username}>{this.state.username}</a>
          </div>
          <div id='email'>{this.state.email}</div>
        </div>
      </div>
    )
  }
})


var Nav = React.createClass({
  render: function() {
    return (
      <div id='top-nav'>
        <ul>
          <li><a href='#'>Repos</a></li>
          <li><a href='#'>Badges</a></li>
          <li><a href='#'>Contact</a></li>
        </ul>
      </div>
    )
  }
})


ReactDOM.render(<RepoList user={USER} />, document.getElementById("main"));
ReactDOM.render(<Profile user={USER} />, document.getElementById("top-body"));
ReactDOM.render(<Nav />, document.getElementById("top-tail"));
