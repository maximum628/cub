var React    = require('react');
var ReactDOM = require('react-dom');

var USER = 'mariuscoto'


var Repo = React.createClass({
  render: function() {
    var repo_score = this.props.repo.watchers_count * PointsList.watch;
    repo_score += this.props.repo.stargazers_count * PointsList.star;

    return (
      <li>
        <a href={this.props.repo.html_url}>{this.props.repo.name}</a> [{repo_score}]
        <ul>
          <li>Forked: ??</li>
          <li>Forks: {this.props.repo.forks_count}</li>
          <li>Stars: {this.props.repo.stargazers_count}</li>
          <li>Watchers: {this.props.repo.watchers_count}</li>
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
    $.get('/api/v1/repository/?offset=0&limit=100&format=json', function(res) {
      if (this.isMounted()) {
        this.setState({
          repos: res.objects
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
          return (<Repo repo={repo} key={i} />)
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
