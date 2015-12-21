var React    = require('react');
var ReactDOM = require('react-dom');

var History = require('history');
var Router = require('react-router').Router;
var Route = require('react-router').Route;
var Link = require('react-router').Link;

const history = History.createHistory();

var Repo = React.createClass({
  render: function() {
    var repo_score = this.props.repo.watchers_count * PointsList.watch;
    repo_score += this.props.repo.stargazers_count * PointsList.star;

    return (
      <div className="repo-item">
        <div className="repo-score">
          <div className="repo-score-points">{repo_score}</div>
          <div className="repo-score-text">Points</div>
        </div>
        <div className="repo-name">
          <a href={this.props.repo.html_url}>{this.props.repo.name}</a>
        </div>
        <div className="repo-description">{this.props.repo.description}</div>
        <ul>
          <li>Forked: ??</li>
          <li>Forks: {this.props.repo.forks_count}</li>
          <li>Stars: {this.props.repo.stargazers_count}</li>
          <li>Watchers: {this.props.repo.watchers_count}</li>
        </ul>
      </div>
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
        <h1>Your contributions</h1>
        { this.state.repos.map(function(repo, i) {
          return (<Repo repo={repo} key={i} />)
        }, this)}

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
    $.get('/api/v1/account/?format=json', function(res) {
      if (this.isMounted()) {
        this.setState({
          avatar_url : res.objects[0].avatar_url,
          name       : res.objects[0].name,
          username   : res.objects[0].login,
          email      : res.objects[0].email
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
      <div id="head">
        <div id="head-box">
          <div id="logo">
            <a href="/"> CUB </a>
          </div>
          <nav id="nav">
            <li><Link to='/profile'>Profile</Link></li>
            <li><Link to='/'>Repos</Link></li>
            <li><Link to='/contact'>Contact</Link></li>
          </nav>
        </div>
      </div>
    )
  }
})


var RepoPage = React.createClass({
  render: function() {
    return (
      <div>
        <Nav />
        <RepoList />
      </div>
    )
  }
})


var ContactPage = React.createClass({
  render: function() {
    return (
      <div>
        <Nav />
        <h1>Get in touch</h1>
      </div>
    )
  }
})


var ProfilePage = React.createClass({
  render: function() {
    return (
      <div>
        <Nav />
        <Profile />
      </div>
    )
  }
})


ReactDOM.render((
  <Router history={history}>
    <Route path="/profile" component={ProfilePage} />
    <Route path="/" component={RepoPage} />
    <Route path="/contact" component={ContactPage} />
  </Router>
), document.getElementById("main"))
