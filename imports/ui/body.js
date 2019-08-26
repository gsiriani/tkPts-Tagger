import { Template } from 'meteor/templating';
 
import { Messages } from '../api/messages.js';
 
import './body.html';
 
Template.body.helpers({
  messages() {
    return Messages.find({}, { sort: { createdAt: -1 } });
  },
});


Template.add.events({
  'submit .add-form': function(){
    event.preventDefault();

    // Get input value
    const target = event.target;
    const text = target.text.value;

    // Insert message into collection
    Messages.insert({
      text,
      createdAt: new Date()
    });

    // Clear form
    target.text.value = '';

    // Close modal
    $('#addModal').modal('close');

    return false;
  }
})
