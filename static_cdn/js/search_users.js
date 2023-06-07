document.addEventListener('DOMContentLoaded', function() {
    var searchInput = document.querySelector('#id_search_query');
    var searchResults = document.querySelector('#search-results');
  
    searchInput.addEventListener('input', function() {
      var searchQuery = searchInput.value.trim();
  
      if (searchQuery.length > 0) {
        fetchUsers(searchQuery);
      } else {
        searchResults.innerHTML = '';
      }
    });
  
    function fetchUsers(query) {
      var url = '/search/?q=' + encodeURIComponent(query);
  
      fetch(url)
        .then(function(response) {
          return response.json();
        })
        .then(function(data) {
          displayResults(data);
        })
        .catch(function(error) {
          console.error('Error:', error);
        });
    }
  
    function displayResults(users) {
      var html = '';
  
      if (users.length > 0) {
        html += '<ul>';
        users.forEach(function(user) {
          html += '<li>' + user.username + '</li>';
        });
        html += '</ul>';
      } else {
        html = '<p>No users found.</p>';
      }
  
      searchResults.innerHTML = html;
    }
  });
  