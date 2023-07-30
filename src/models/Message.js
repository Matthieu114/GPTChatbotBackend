'use strict';

function generateUniqueId() {
  // Replace this with your preferred unique ID generation logic
  return `message_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
}

class MessageModel {
  constructor(text, sender) {
    this.id = generateUniqueId();
    this.text = text;
    this.sender = sender;
    this.timestamp = new Date().toLocaleString();
  }
}

module.exports = MessageModel;
