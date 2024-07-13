import "./list.scss";
import Card from "../card/Card";
import EmptyState from "../emptyState/EmptyState";

function List({ posts, emptyMessage, renderActions }) {
  if (!posts || posts.length === 0) {
    return <EmptyState message={emptyMessage || "No listings found."} />;
  }

  return (
    <div className="list">
      {posts.map((item) => (
        <div key={item.id} className="listItem">
          <Card item={item} />
          {renderActions && (
            <div className="listActions">{renderActions(item)}</div>
          )}
        </div>
      ))}
    </div>
  );
}

export default List;
