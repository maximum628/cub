var React    = require('react');
var ReactDOM = require('react-dom');

var History = require('history');
var Router = require('react-router').Router;
var Route = require('react-router').Route;
var Link = require('react-router').Link;
var ReactPaginate = require('react-paginate');

const history = History.createHistory();
const per_page = 10;

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
          <li>Forked: {this.props.repo.fork}</li>
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
        repos: [],
        offset: 0,
        pageNum: 1
      }
  },

  getRepoList: function() {
    var offset = this.state.offset;
    var nextOffset = offset + per_page;
    var url = '/api/v1/repository/?offset=' + offset + '&limit=' + per_page;

    $.get(url, function(res) {
      this.setState({
        repos: res.objects,
        offset: nextOffset,
        pageNum: res.meta.total_count / per_page
      });
    }.bind(this));
  },

  componentDidMount: function() {
    if (this.isMounted()) {
      this.getRepoList();
    }
  },

  handleClick: function(event) {
    this.setState({
      offset: this.state.offset + per_page
    });
    this.getRepoList();
  },

  render: function() {
    return (
      <div>
        <h1>Your score</h1>
        <PointsList />
        <h1>Your contributions</h1>
        { this.state.repos.map(function(repo, i) {
          return (<Repo repo={repo} key={i} />)
        }, this)}

        <ReactPaginate previousLabel={"previous"}
                       nextLabel={"next"}
                       breakLabel={<li className="break"><a href="">...</a></li>}
                       pageNum={this.state.pageNum}
                       marginPagesDisplayed={2}
                       pageRangeDisplayed={5}
                       clickCallback={this.handleClick}
                       containerClassName={"pagination"}
                       subContainerClassName={"pagination-pages"}
                       activeClassName={"active"} />
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
        email      : null,
        progress   : 70,
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

        <div className="profile-progress">
          <span className="progress-level" style={{width: '10%'}}>Noob</span>
          <div id="progress-bar">
            <div className="progress-bar progress-bar-success" role="progressbar" aria-valuenow="70"
            aria-valuemin="0" aria-valuemax="100" style={{width: this.state.progress + '%', float: 'None'}}>
              70%
            </div>
          </div>
          <span className="progress-level" style={{width: '100%'}}>Rockstar</span>
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
            <Link to='/'>CUB</Link>
          </div>
          <nav id="nav">
            <li><Link to='/profile/'>Profile</Link></li>
            <li><Link to='/repos/'>Repos</Link></li>
            <li><Link to='/contact/'>Contact</Link></li>
            { this.render_links() }
          </nav>
        </div>
      </div>
    )
  },

  render_links: function() {
    if (typeof user !== 'undefined') {
      return (<li><a href="/logout/" id="intro-login">Logout</a></li>)
    } else {
      return (<li><a href="/authorize/" id="intro-login">Login</a></li>)
    }
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


var IndexPage = React.createClass({
  render: function() {
    return (
      <div>
        <Nav />
        <div id="intro">
          <div id="intro-top">Open Source Hub</div>
          <div id="intro-body">CUB</div>
          <div id="intro-bottom">
            { this.render_links() }
          </div>
        </div>
      </div>
    )
  },

  render_links: function() {
    if (typeof user !== 'undefined')
      return (<a href="/profile/" id="intro-login">Profile</a>)
    else
      return (<a href="/authorize/" id="intro-login">Login</a>)
  }
})


ReactDOM.render((
  <Router history={history}>
    <Route path="/" component={IndexPage} />
    <Route path="/profile/" component={ProfilePage} />
    <Route path="/repos/" component={RepoPage} />
    <Route path="/contact/" component={ContactPage} />
  </Router>
), document.getElementById("main"))
