var React    = require('react');
var ReactDOM = require('react-dom');

var History  = require('history');
var Router   = require('react-router').Router;
var Route    = require('react-router').Route;
var Redirect = require('react-router').Redirect;
var Link     = require('react-router').Link;
var ReactPaginate = require('react-paginate');

const history = History.createHistory();
const per_page = 10;


const MAX_PROGRESS = 1000


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
        pageNum: 1,
        nextOffset: per_page,
        previousOffset: 0
      }
  },

  getRepoList: function() {
    var offset = this.state.offset;
    var nextOffset = offset + per_page;
    var previousOffset = (offset - per_page < 1) ? 0 : offset - per_page;
    var url = '/api/v1/repository/?offset=' + offset + '&limit=' + per_page;

    $.get(url, function(res) {
      this.setState({
        repos: res.objects,
        nextOffset: nextOffset,
        previousOffset: previousOffset,
        pageNum: Math.ceil(res.meta.total_count / per_page )})
     }.bind(this));
  },

  componentDidMount: function() {
    if (this.props.username !== 'undefined' && this.isMounted()) {
      this.getRepoList();

    } else {
      // Load demo page
      this.setState({
        repos   : {},
        offset  : null,
        pageNum : null
      });
    }
  },

  handleClick: function(event) {
    var pageSelected = event.selected;

    this.setState({
      offset: pageSelected * per_page
    }, () => {
      this.getRepoList();
    });
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


var ProfileStats = React.createClass({
  getInitialState: function() {
    return {
      repos_count: null,
      repos_score: null,
      repos_top_name: null,
      repos_top_score: null,
      progress: 0
    }
  },

  componentDidMount: function() {
    if (typeof username === 'undefined') {
      if (typeof this.props.username === 'undefined') {
        // User not authenticated, looking at nothing
        // Show demo data
        this.setState({
          repos_count: '###',
          repos_score: '###',
          repos_top_name: '###',
          repos_top_score: '__',
          progress: 15
        });

      } else {
        // User is not authenticated, looking at someone
        // Show some real data
        this.setState({
          repos_count: null,
          repos_score: null,
          repos_top_name: null,
          repos_top_score: null,
          progress: 0
        });
      }

    } else {
      if (typeof this.props.username === 'undefined') {
        // User is authenticated, looking at nothing
        this.setState({
          repos_count: null,
          repos_score: null,
          repos_top_name: null,
          repos_top_score: null,
          progress: 0
        });

      } else if (this.props.username == username) {
        // User is authenticated, looking at own profile
        var offset = 0;
        var per_page = 999;
        var url = '/api/v1/repository/?offset=' + offset + '&limit=' + per_page;

        $.get(url, function(res) {
          if (this.isMounted()) {

            // Compute total repo score and max repo
            var total_score = 0;
            var max_score = 0;
            var max_repo = '';
            for (var i in res.objects) {
              var score = 0;
              score += res.objects[i].watchers_count * PointsList.watch;
              score += res.objects[i].stargazers_count * PointsList.star;

              if (score > max_score) { max_score = score; max_repo = res.objects[i].name }
              total_score += score;
            }

            this.setState({
              repos_count: res.objects.length,
              repos_score: total_score,
              repos_top_name: max_repo,
              repos_top_score: max_score,
              progress: 100 * total_score / MAX_PROGRESS
            });
          }
        }.bind(this));

      } else {
        // User is authenticated, looking at someone
        this.setState({
          repos_count: null,
          repos_score: null,
          repos_top_name: null,
          repos_top_score: null,
          progress: 0
        });
      }
    }
  },

  render: function() {
    return(
      <div>
        <div className="profile-progress">
          <span className="progress-level" style={{width: '10%'}}>Noob</span>
          <span className="progress-level" style={{width: '80%'}}>Master</span>
          <div id="progress-bar">
            <div className="progress-bar progress-bar-success" role="progressbar" aria-valuenow="70"
            aria-valuemin="0" aria-valuemax="100" style={{width: this.state.progress + '%', float: 'None'}}>
              {this.state.progress + '%'}
            </div>
          </div>
          <span className="progress-level" style={{width: '100%'}}>Rockstar</span>
        </div>

        <div className="stats-metric">
          <div className="stats-metric-title">Most important repo</div>
          <div className="stats-metric-no">{this.state.repos_top_name}</div>
          <div className="stats-metric-info">{this.state.repos_top_score + " points"}</div>
        </div>
        <div className="stats-metric">
          <div className="stats-metric-title">Total score</div>
          <div className="stats-metric-no">{this.state.repos_score}</div>
          <div className="stats-metric-info">for all repos</div>
        </div>
        <div className="stats-metric">
          <div className="stats-metric-title">Own contributions count</div>
          <div className="stats-metric-no">{this.state.repos_count}</div>
          <div className="stats-metric-info">repositories</div>
        </div>
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

    // Show demo profile
    if (typeof this.props.username === 'undefined') {
      this.setState({
        avatar_url : 'http://bestmarketinfo.com/images/blank-avatar.png',
        name       : 'Your name',
        username   : 'username',
        email      : 'username@cub.com',
      });
    }

    // User is viewing his own profile
    else if (typeof username !== 'undefined' && this.props.username == username) {
      $.get('/api/v1/account/', function(res) {
        if (this.isMounted()) {
          this.setState({
            avatar_url : res.objects[0].avatar_url,
            name       : res.objects[0].username,
            username   : res.objects[0].login,
            email      : res.objects[0].email
          });
        }
      }.bind(this));

    // User is viewing other user's profile
    } else {
      $.get('/api/v1/account/?username=' + this.props.username, function(res) {
        if (this.isMounted()) {
          this.setState({
            avatar_url : res.objects[0].avatar_url,
            name       : res.objects[0].name,
            username   : res.objects[0].username,
            email      : res.objects[0].email
          });
        }
      }
      .bind(this))
      .fail(function(err) {
        if (err.status == 400 ) {
          // User not found, redirect to 404 page
          window.location.href = "/404/";
        }
      });
    }
  },

  render: function() {
    if (this.state.avatar_url) {
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
      );
    } else {
      return(<div></div>);
    }
  }
})


var Nav = React.createClass({
  render: function() {
    var user = ''
    if (typeof username !== 'undefined')
      user = username

    return (
      <div id="head">
        <div id="head-box">
          <div id="logo">
            <Link to='/'>CUB</Link>
          </div>
          <nav id="nav">
            <li><Link to={'/profile/' + user}>Profile</Link></li>
            <li><Link to={'/repos/' + user}>Repos</Link></li>
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
        <RepoList username={this.props.params.username}  />
      </div>
    )
  }
})


var ContactPage = React.createClass({

  getInitialState: function() {
    return {
    };
  },

  handleNameChange: function(event) {
    this.setState({fullName: event.target.value});
  },

  handleEmailChange: function(event) {
    this.setState({email: event.target.value});
  },

  handleContentChange: function(event) {
    this.setState({content: event.target.value});
  },

  handleSubmit: function(event) {
    var data = JSON.stringify({
      name: this.state.fullName,
      email: this.state.email,
      content: this.state.content
    });

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", Django.csrf_token());
        xhr.setRequestHeader("Content-Type", 'application/json');
      }
    });

    $.ajax({
       type: 'POST',
       url: '/api/public/contact/',
       data: data,
     })
     .done(function(data) {
     })
     .fail(function(jqXhr) {
     });
  },

  render: function() {
    return (
      <div>
        <Nav />
        <form className="col-md-6 col-md-offset-3" id="contact-form">
          <h1>Get in touch with us</h1>
            <div className="form-group">
              <input type="text" value={this.state.fullName} placeholder='Full name' onChange={this.handleNameChange}/>
              <input type="email" value={this.state.email} placeholder='Email' onChange={this.handleEmailChange}/>
            </div>
            <div className="form-group">
              <textarea value={this.state.content} placeholder='Your message' onChange={this.handleContentChange}/>
            </div>
            <div className="form-group">
              <a href='' id="contact-form__submit" onClick={this.handleSubmit}> Send </a>
            </div>
        </form>
      </div>
    )
  }
})


var ProfilePage = React.createClass({
  render: function() {
    return (
      <div>
        <Nav />
        <Profile username={this.props.params.username} />
        <ProfileStats username={this.props.params.username} />
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
          <div id="intro-top">Open Source Connect Hub</div>
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


var NotFoundPage = React.createClass({
  render: function() {
    return (
      <div>
        <Nav />
        <h1>404: Page not found</h1>
      </div>
    )
  }
})


ReactDOM.render((
  <Router history={history}>
    <Route path="/" component={IndexPage} />
    <Route path="/profile/" component={ProfilePage} />
    <Route path="/profile/:username" component={ProfilePage} />
    <Route path="/repos/" component={RepoPage} />
    <Route path="/repos/:username" component={RepoPage} />
    <Route path="/contact/" component={ContactPage} />
    <Route path="/404/" component={NotFoundPage} />
  </Router>
), document.getElementById("main"))
