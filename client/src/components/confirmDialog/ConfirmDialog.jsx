import "./confirmDialog.scss";

function ConfirmDialog({ message, onConfirm, onCancel }) {
  return (
    <div className="confirmOverlay" onClick={onCancel}>
      <div className="confirmDialog" onClick={(e) => e.stopPropagation()}>
        <h3>Are you sure?</h3>
        <p>{message}</p>
        <div className="actions">
          <button className="cancelBtn" onClick={onCancel}>
            Cancel
          </button>
          <button className="confirmBtn" onClick={onConfirm}>
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
}

export default ConfirmDialog;
