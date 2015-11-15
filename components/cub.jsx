var React    = require('react');
var ReactDOM = require('react-dom');

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
      <ul>
      { this.state.repos.map(function(repo) {
        return (<li>{repo.name}</li>)
      }, this)}
      </ul>
    );
  }
});

//if( $('#main').length )
ReactDOM.render(<RepoList />, document.body);
