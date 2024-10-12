import "./emptyState.scss";

function EmptyState({ message = "Nothing here yet." }) {
  return (
    <div className="emptyState">
      <div className="emptyIcon">&#x1F4ED;</div>
      <p>{message}</p>
    </div>
  );
}

export default EmptyState;
