// Global vars


// Firebase setup
var firebase = new Firebase("https://tweetengine.firebaseio.com/");
var messages = firebase.child("messages");

// Register html fields
var messageField = $('#messageInput');
var messageList = $('#messages');

// Record session commands
var recents = []
var recentIndex = -1
var recentSize = 0

// Listen for message submit
messageField.keypress(function (e) {
  // Enter
  if (e.keyCode == 13) {

    // Grab fields
    var username = "andrewsosa001";
    var message = messageField.val();

    // Save message to chat, reset field
    messages.push({name:username, text:message});
    messageField.val('');

    // Store command in session record
    recentSize = recents.unshift(message)

  }
  // Up
  if (e.keyCode == 38) {
    ++recentIndex;
    if (recentIndex >= recentSize) {
      recentIndex = -1;
      messageField.val('');
    } else {
      messageField.val(recents[recentIndex]);
    }
    e.preventDefault();
  }
  // Down
  if (e.keyCode == 40) {
    if (recentIndex <= -1) {
      messageField.val('')
    } else {
      --recentIndex;
      messageField.val(recents[recentIndex]);
    }
    e.preventDefault();
  }
});

// Add a callback that is triggered for each chat message.
messages.limitToLast(10).on('child_added', function (snapshot) {

  // Retrieve message values
  var data = snapshot.val();
  var username = data.name || "UNKNOWN";
  var message = data.text;

  // Create html elements, sanatize text
  var messageElement = $("<li>");
  var nameElement = $("<strong class='chat-username'></strong>")
  nameElement.text(username + "\t\t");
  messageElement.text(message).prepend(nameElement);

  // Add message
  messageList.append(messageElement)

  // Scroll to bottom
  messageList[0].scrollTop = messageList[0].scrollHeight;
});

console.log("Controller online!")
