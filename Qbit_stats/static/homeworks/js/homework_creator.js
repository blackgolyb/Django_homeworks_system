/*const user = {
  id: 0,            // user id
  username: "some name",// user name
}
const group = {
  id: 0,            // group id
  name: "some name",// group name
  users_ids = [*user.id],   // list of users
}*/

function buildPatternTable(word) {
  const patternTable = [0];
  let prefixIndex = 0;
  let suffixIndex = 1;

  while (suffixIndex < word.length) {
    if (word[prefixIndex] === word[suffixIndex]) {
      patternTable[suffixIndex] = prefixIndex + 1;
      suffixIndex += 1;
      prefixIndex += 1;
    } else if (prefixIndex === 0) {
      patternTable[suffixIndex] = 0;
      suffixIndex += 1;
    } else {
      prefixIndex = patternTable[prefixIndex - 1];
    }
  }

  return patternTable;
}


function filterObjectsByField(objectsHavingField, word, field) {
  filterReturn = {
    word_length: word.length,
    filteredObjects: [],
  }
  if (word.length != 0) {
    const patternTable = buildPatternTable(word);

    console.log(objectsHavingField);
    for (var i = 0; i < objectsHavingField.length; i++) {
      const checke_word = objectsHavingField[i][field];
      let textIndex = 0;
      let wordIndex = 0;

      while (textIndex < checke_word.length) {
        if (checke_word[textIndex] === word[wordIndex]) {
          // We've found a match.
          if (wordIndex === word.length - 1) {
            filteredObject = {
              starts_id: (textIndex - word.length) + 1,
              obj: objectsHavingField[i],
            }
            filterReturn.filteredObjects.push(filteredObject);
            //return (textIndex - word.length) + 1;

          }
          wordIndex += 1;
          textIndex += 1;
        } else if (wordIndex > 0) {
          wordIndex = patternTable[wordIndex - 1];
        } else {
          wordIndex = 0;
          textIndex += 1;
        }
      }
    }
  }


  return filterReturn;
}

let groups
let users
let getUserById = {}
let filtered_groups
let filtered_users

function returnJson(data) {
  groups = data['groups']
  users = data['users']
  getUserById = {}
  for (var i = 0; i < users.length; i++) {
    getUserById[users[i].id] = users[i];
  }
  console.log(groups);
  console.log(users);
  console.log(getUserById);
}

const searchOutput = document.querySelector('.search-output')

function filterGroupsAndUsers() {
  const search_word = this.value
  console.log(search_word);
  filtered_obj_users = filterObjectsByField(users, search_word, 'username')
  filtered_obj_groups = filterObjectsByField(groups, search_word, 'name')
  console.log(filtered_obj_users, filtered_obj_groups);

  let content = ''
  let group_content = ''

  for (var i = 0; i < filtered_obj_groups.filteredObjects.length; i++) {
    const name = filtered_obj_groups.filteredObjects[i].obj.name
    const starts_selection_id = filtered_obj_groups.filteredObjects[i].starts_id
    const groupSpanPreview = '<span class="search-preview">'+ name.slice(0, starts_selection_id)
      + '<span class="selected-text">' + name.slice(starts_selection_id, starts_selection_id + filtered_obj_groups.word_length) + "</span>"
      + name.slice(starts_selection_id + filtered_obj_groups.word_length) +"</span>";
    const groupSpan = '<span class="search-result invisible">' + name + "</span>"

    let users_list = ''
    for (var j = 0; j < filtered_obj_groups.filteredObjects[i].obj.users.length; j++) {
      const user_id = filtered_obj_groups.filteredObjects[i].obj.users[j];
      try {
        users_list += '<li>' + getUserById[user_id].username + '</li>';
      } catch (e) {
        console.log(e);
      }
    }
    group_content += '<li>'+ groupSpanPreview + groupSpan + '<ul>' + users_list + '</ul>' +'</li>'
  }
  const groupViewer = '<ul class="group-viewer">'+ group_content +'</ul>'
  content += groupViewer;

  for (var i = 0; i < filtered_obj_users.filteredObjects.length; i++) {
    const name = filtered_obj_users.filteredObjects[i].obj.username
    const starts_selection_id = filtered_obj_users.filteredObjects[i].starts_id

    content += '<span class="search-preview">'+ name.slice(0, starts_selection_id)
      + '<span class="selected-text">' + name.slice(starts_selection_id, starts_selection_id + filtered_obj_users.word_length) + "</span>"
      + name.slice(starts_selection_id + filtered_obj_users.word_length) +"</span>"
      + '<span class="search-result invisible">'+ name +"</span>";
  }
  html = "<ul>"+ content +"</ul>"
  searchOutput.innerHTML = html;
  updateGroupEnents();
  console.log(filtered_obj_users, filtered_obj_groups);
}

function normalizeGroupsAndUsersView() {
  searchOutput.querySelectorAll('.search-preview').forEach(function (item) {
    item.classList.add('invisible');
  })
  searchOutput.querySelectorAll('.search-result').forEach(function (item) {
    item.classList.remove('invisible');
  })
}

function updateGroupEnents() {
  $(".group-viewer ul").hide();
  $(".group-viewer li span").click(function() { $(this).next().slideToggle("normal"); });
}

const searchFrom = document.querySelector('form[name=search-form]')
searchFrom.addEventListener('submit', function (e) {
  e.preventDefault()
  ajaxSendForm(this)
})
//searchFrom.submit()

const searchField = document.querySelector('.search-field')
searchField.addEventListener('input', filterGroupsAndUsers)
searchField.addEventListener('blur', normalizeGroupsAndUsersView)
searchField.addEventListener('paste', filterGroupsAndUsers)
//searchField.addEventListener('propertychange', filterGroupsAndUsers)
