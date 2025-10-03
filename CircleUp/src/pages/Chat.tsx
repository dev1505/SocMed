import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { CommonApiCall, followUser, unFollowUser } from "../CommonFunctions";
import { django_app_backend_url } from "../defaults";
import { MdCancel } from "react-icons/md";
import { TiTick } from "react-icons/ti";

export default function Chat() {
  const [userData, setUserData] = useState({
    currentUser: {},
    allUsers: [],
    otherUsers: [],
  });
  const navigate = useNavigate();

  async function handleUserChat({ to_user_id }) {
    await navigate(
      `/chat/user?user_id=${to_user_id}&current=${userData.currentUser.id}`
    );
  }

  async function getUsers() {
    const response1 = await CommonApiCall({
      url: `${django_app_backend_url}/auth`,
      type: "get",
    });

    const response2 = await CommonApiCall({
      url: `${django_app_backend_url}/get/users/`,
      type: "get",
    });

    const currentUser = response1?.data;
    const followingList =
      currentUser.following?.map((f) => f.following__id) || [];

    const enhancedUsers = response2.data.map((user) => ({
      ...user,
      following: followingList.includes(user.id),
    }));

    setUserData({
      currentUser,
      allUsers: enhancedUsers,
      otherUsers: enhancedUsers, // initially same
    });
  }

  async function handleFollowing({ followingStatus = "", id }) {
    const rollbackState = userData;

    if (followingStatus === "follow") {
      setUserData((prev) => ({
        ...prev,
        otherUsers: prev.otherUsers.map((user) =>
          user.id === id ? { ...user, following: true } : user
        ),
        allUsers: prev.allUsers.map((user) =>
          user.id === id ? { ...user, following: true } : user
        ),
      }));

      const response = await followUser({ following: id });
      if (!(await response.success)) {
        alert(response.message);
        setUserData(rollbackState);
      }
    } else {
      setUserData((prev) => ({
        ...prev,
        otherUsers: prev.otherUsers.map((user) =>
          user.id === id ? { ...user, following: false } : user
        ),
        allUsers: prev.allUsers.map((user) =>
          user.id === id ? { ...user, following: false } : user
        ),
      }));

      const response = await unFollowUser({ following: id });
      if (!(await response.success)) {
        alert(response.message);
        setUserData(rollbackState);
      }
    }
  }

  useEffect(() => {
    getUsers();
  }, []);

  function handleSearchUser(e) {
    const keyword = e.target.value.toLowerCase();
    if (!keyword) {
      setUserData((prev) => ({ ...prev, otherUsers: prev.allUsers }));
    } else {
      setUserData((prev) => ({
        ...prev,
        otherUsers: prev.allUsers.filter((user) =>
          user.username.toLowerCase().includes(keyword)
        ),
      }));
    }
  }

  return (
    <div>

      <div>
        <input
          type="text"
          name="searchbar"
          id="searchbar"
          onChange={handleSearchUser}
          className="rounded-md bg-white mt-2 p-2 w-full focus:outline-2 outline-orange-400"
          placeholder={`Hello ${userData.currentUser.username ? userData.currentUser.username : ""}, Search Here`}
        />
      </div>

      <div className="flex flex-col w-full p-5 pb-10 gap-2 text-white">
        {userData?.otherUsers?.length ? (
          userData.otherUsers.map((data) => (
            <div
              key={data.id}
              className="flex justify-around items-center gap-3 rounded py-4 bg-stone-500"
            >
              <div className="flex items-center gap-3">
                <img
                  src={data?.profile_pic || "https://picsum.photos/600"}
                  alt="profile"
                  className="w-20 h-20 rounded-full object-cover"
                />
                <div>
                  <div className="text-xl">{data?.username}</div>
                </div>
              </div>
              <div className="flex gap-3 justify-center items-center">
                <div>
                  <button
                    className="rounded cursor-pointer hover:scale-105 bg-slate-700 p-2"
                    onClick={() =>
                      handleFollowing({
                        followingStatus: data?.following
                          ? "unfollow"
                          : "follow",
                        id: data?.id,
                      })
                    }
                  >
                    {data?.following ? (
                      <div className="flex items-center gap-2">
                        Unfollow < MdCancel className="text-lg" />
                      </div>
                    ) : (
                      <div className="flex items-center gap-2">
                        Follow <TiTick className="text-lg" />
                      </div>
                    )}
                  </button>
                </div>
                <div>
                  <button
                    onClick={() => {
                      handleUserChat({ to_user_id: data.id });
                    }}
                    className="rounded cursor-pointer hover:scale-105 bg-slate-700 p-2"
                  >
                    Chat
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div>No users found</div>
        )}
      </div>
    </div>
  );
}