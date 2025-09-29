import { useEffect, useState } from "react";
import { CommonApiCall } from "../CommonFunctions";
import PostCard from "../components/postCard";
import { django_app_backend_url } from "../defaults";

import { useNavigate } from "react-router-dom";

export default function UserProfile() {
    const navigate = useNavigate();
    const [userData, setUserData] = useState(null);

    async function fetchUserData() {
        const response = await CommonApiCall({ type: "get", url: `${django_app_backend_url}/auth` });
        if (response) {
            setUserData(response.data);
        }
    }

    useEffect(() => {
        fetchUserData();
    }, []);

    return (
        <div className="py-4">
            <div className="bg-white rounded-lg shadow-lg p-8 max-w-4xl mx-auto">
                <div className="flex flex-col md:flex-row items-center justify-center">
                    <div className="w-32 h-32 md:w-48 md:h-48 rounded-full overflow-hidden shadow-lg">
                        <img
                            src={userData?.profile_picture || "https://picsum.photos/200"}
                            alt="Profile"
                            className="w-full h-full object-cover"
                        />
                    </div>
                    <div className="md:ml-8 mt-4 md:mt-0 justify-center text-center md:text-left">
                        <h1 className="text-3xl font-bold text-gray-800">{userData?.username}</h1>
                        <div className="flex justify-center md:justify-start mt-4 space-x-6 text-gray-600">
                            <div>
                                <span className="font-bold text-gray-800">{userData?.posts?.length || 0}</span> Posts
                            </div>
                            <div onClick={() => navigate("/profile/followers")} className="cursor-pointer">
                                <span className="font-bold text-gray-800">{userData?.followers || 0}</span> Followers
                            </div>
                            <div onClick={() => navigate("/profile/following")} className="cursor-pointer">
                                <span className="font-bold text-gray-800">{userData?.following || 0}</span> Following
                            </div>
                        </div>
                        <button onClick={() => navigate("/profile/edit")} className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">Edit Profile</button>
                    </div>
                </div>
            </div>
            <div className="mt-8">
                <div className="bg-white rounded-lg shadow-lg p-4">
                    <h2 className="text-xl font-bold text-gray-800 mb-4">Posts</h2>
                    <PostCard />
                </div>
            </div>
        </div>
    );
}
