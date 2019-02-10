//publish


var messageText = 'Sample Message';
var message = solace.SolclientFactory.createMessage();
message.setDestination(solace.SolclientFactory.createTopicDestination(publisher.topicName));
message.setBinaryAttachment(messageText);
message.setDeliveryMode(solace.MessageDeliveryModeType.DIRECT);
if (publisher.session !== null) {
    try {
        publisher.session.send(message);
        publisher.log('Message published.');
    } catch (error) {
        publisher.log(error.toString());
    }
} else {
    publisher.log('Cannot publish because not connected to Solace message router.');
}