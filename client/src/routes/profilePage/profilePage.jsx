import Chat from "../../components/chat/Chat";
import List from "../../components/list/List";
import Loader from "../../components/loader/Loader";
import ConfirmDialog from "../../components/confirmDialog/ConfirmDialog";
import "./profilePage.scss";
import apiRequest from "../../lib/apiRequest";
import { Await, Link, useLoaderData, useNavigate } from "react-router-dom";
import { Suspense, useContext, useState } from "react";
import { AuthContext } from "../../context/AuthContext";

function ProfilePage() {
  const data = useLoaderData();
  const { updateUser, currentUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const [confirmAction, setConfirmAction] = useState(null);
  const [confirmMessage, setConfirmMessage] = useState("");
  const [deletedPosts, setDeletedPosts] = useState([]);

  const handleLogout = async () => {
    try {
      await apiRequest.post("/auth/logout");
      updateUser(null);
      navigate("/");
    } catch (err) {
      console.log(err);
    }
  };

  const handleDeletePost = (postId) => {
    setConfirmMessage("This will permanently delete this listing.");
    setConfirmAction(() => async () => {
      try {
        await apiRequest.delete("/posts/" + postId);
        setDeletedPosts((prev) => [...prev, postId]);
      } catch (err) {
        console.log(err);
      }
      setConfirmAction(null);
    });
  };

  const handleDeleteAccount = () => {
    setConfirmMessage(
      "This will permanently delete your account and all your data. This cannot be undone."
    );
    setConfirmAction(() => async () => {
      try {
        await apiRequest.delete("/users/" + currentUser.id);
        updateUser(null);
        navigate("/");
      } catch (err) {
        console.log(err);
      }
      setConfirmAction(null);
    });
  };

  const filterDeleted = (posts) =>
    posts.filter((p) => !deletedPosts.includes(p.id));

  return (
    <div className="profilePage">
      <div className="details">
        <div className="wrapper">
          <div className="title">
            <h1>User Information</h1>
            <Link to="/profile/update">
              <button>Update Profile</button>
            </Link>
          </div>
          <div className="info">
            <span>
              Avatar:
              <img src={currentUser.avatar || "/noavatar.jpg"} alt="" />
            </span>
            <span>
              Username: <b>{currentUser.username}</b>
            </span>
            <span>
              E-mail: <b>{currentUser.email}</b>
            </span>
            <div className="infoActions">
              <button className="logoutBtn" onClick={handleLogout}>
                Logout
              </button>
              <button className="deleteAccountBtn" onClick={handleDeleteAccount}>
                Delete Account
              </button>
            </div>
          </div>
          <div className="title">
            <h1>My List</h1>
            <Link to="/add">
              <button>Create New Post</button>
            </Link>
          </div>
          <Suspense fallback={<Loader />}>
            <Await
              resolve={data.postResponse}
              errorElement={<p>Error loading posts!</p>}
            >
              {(postResponse) => (
                <List
                  posts={filterDeleted(postResponse.data.userPosts)}
                  emptyMessage="You haven't created any listings yet."
                  renderActions={(item) => (
                    <>
                      <Link to={`/edit/${item.id}`}>
                        <button className="editBtn">Edit</button>
                      </Link>
                      <button
                        className="deleteBtn"
                        onClick={() => handleDeletePost(item.id)}
                      >
                        Delete
                      </button>
                    </>
                  )}
                />
              )}
            </Await>
          </Suspense>
          <div className="title">
            <h1>Saved List</h1>
          </div>
          <Suspense fallback={<Loader />}>
            <Await
              resolve={data.postResponse}
              errorElement={<p>Error loading posts!</p>}
            >
              {(postResponse) => (
                <List
                  posts={postResponse.data.savedPosts}
                  emptyMessage="You haven't saved any listings yet."
                />
              )}
            </Await>
          </Suspense>
        </div>
      </div>
      <div className="chatContainer">
        <div className="wrapper">
          <Suspense fallback={<Loader />}>
            <Await
              resolve={data.chatResponse}
              errorElement={<p>Error loading chats!</p>}
            >
              {(chatResponse) => <Chat chats={chatResponse.data} />}
            </Await>
          </Suspense>
        </div>
      </div>

      {confirmAction && (
        <ConfirmDialog
          message={confirmMessage}
          onConfirm={confirmAction}
          onCancel={() => setConfirmAction(null)}
        />
      )}
    </div>
  );
}

export default ProfilePage;
