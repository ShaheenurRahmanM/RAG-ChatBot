/**
 * MessageBubble Component
 * Displays individual chat messages as bubbles
 */

import PropTypes from 'prop-types';

export function MessageBubble({ message, isUser }) {
  return (
    <div className={`message-bubble ${isUser ? 'user' : 'ai'}`}>
      <div className="bubble-content">
        <p>{message}</p>
      </div>
    </div>
  );
}

MessageBubble.propTypes = {
  message: PropTypes.string.isRequired,
  isUser: PropTypes.bool.isRequired,
};

export default MessageBubble;
