import { useEffect, useState } from "react";
import { CommonApiCall } from "../CommonFunctions";
import PostCard from "../components/postCard";
import { django_app_backend_url } from "../defaults";

import { useNavigate, useSearchParams } from "react-router-dom";

export default function UserProfile() {

    const navigate = useNavigate();
    const [params] = useSearchParams()
    const user_id = params.get("user_id") ?? null
    const [userData, setUserData] = useState(null);
    const [postData, setPostData] = useState({ data: [] });

    async function fetchUserData() {
        let response;
        if (user_id) {
            response = await CommonApiCall({ type: "get", url: `${django_app_backend_url}/auth?user_id=${user_id}` });
        } else {
            response = await CommonApiCall({ type: "get", url: `${django_app_backend_url}/auth` });
        }
        if (response) {
            setUserData(await response.data);
        }
    }

    async function getPostData() {
        let posts;
        if (user_id) {
            posts = await CommonApiCall({ type: "post", url: `${django_app_backend_url}/get/other/user/posts/`, payload: { user_id } });
        } else {
            posts = await CommonApiCall({ type: "get", url: `${django_app_backend_url}/get/user/posts/` });
        }
        if (posts) {
            setPostData({ ...postData, data: await posts.data });
        }
    }

    useEffect(() => {
        fetchUserData();
        getPostData();
    }, [user_id]);


    return (
        <div className="min-h-screen p-4 sm:p-6 md:p-8">
            <div className="max-w-4xl mx-auto">
                <div className="bg-white rounded-2xl shadow-xl p-6 md:p-8">
                    <div className="flex flex-col md:flex-row items-center">
                        <div className="w-32 h-32 md:w-40 md:h-40 rounded-full overflow-hidden shadow-lg mx-auto md:mx-0">
                            <img
                                src={userData?.profile_pic || "https://picsum.photos/200"}
                                alt="Profile"
                                className="w-full h-full object-cover"
                            />
                        </div>
                        <div className="md:ml-8 mt-6 md:mt-0 text-center md:text-left flex-grow">
                            <h1 className="text-3xl md:text-4xl font-bold text-gray-800">{userData?.username}</h1>
                            <div className="text-md font-bold text-gray-400">{userData?.bio}</div>
                            <div className="flex justify-center md:justify-start mt-2 space-x-6 text-gray-600">
                                <div className="text-center">
                                    <span className="font-bold text-lg text-gray-800">{userData?.posts?.length || 0}</span>
                                    <p>Posts</p>
                                </div>
                                <div onClick={() => navigate("/profile/followers")} className="cursor-pointer text-center">
                                    <span className="font-bold text-lg text-gray-800">{userData?.followers?.length || 0}</span>
                                    <p>Followers</p>
                                </div>
                                <div onClick={() => navigate("/profile/following")} className="cursor-pointer text-center">
                                    <span className="font-bold text-lg text-gray-800">{userData?.following?.length || 0}</span>
                                    <p>Following</p>
                                </div>
                            </div>
                            <div className="mt-6 flex justify-center md:justify-start space-x-4">
                                {user_id ? (
                                    <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-300">
                                        Follow
                                    </button>
                                ) : (
                                    <button onClick={() => navigate("/profile/edit")} className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors duration-300">
                                        Edit Profile
                                    </button>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
                <div className="mt-8">
                    <div className="bg-white rounded-2xl shadow-xl p-4">
                        <h2 className="text-2xl font-bold text-gray-800 mb-4 text-center md:text-left">Posts</h2>
                        <PostCard postData={postData} followButton={false} />
                    </div>
                </div>
            </div>
        </div>
    );
}
