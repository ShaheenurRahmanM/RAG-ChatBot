/**
 * SourceList Component
 * Displays the source documents used to answer the question
 */

import PropTypes from 'prop-types';

export function SourceList({ sources }) {
  if (!sources || sources.length === 0) {
    return null;
  }

  return (
    <div className="source-list">
      <p className="source-label">📄 Sources:</p>
      <div className="source-items">
        {sources.map((source, index) => (
          <div key={index} className="source-item">
            {source}
          </div>
        ))}
      </div>
    </div>
  );
}

SourceList.propTypes = {
  sources: PropTypes.arrayOf(PropTypes.string),
};

export default SourceList;
