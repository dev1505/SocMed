import { useState, type FormEvent, useEffect } from "react";
import { CommonApiCall } from "../CommonFunctions";
import { django_app_backend_url } from "../defaults";

export default function EditProfile() {
    const [image, setImage] = useState(null);
    const [preview, setPreview] = useState(null);
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        async function fetchUserData() {
            const response = await CommonApiCall({ type: "get", url: `${django_app_backend_url}/auth/me` });
            if (response) {
                setUserData(response.data);
                setPreview(response.data.profile_picture);
            }
        }
        fetchUserData();
    }, []);

    function handleImageChange(e) {
        const file = e.target.files[0];
        if (file) {
            setImage(file);
            setPreview(URL.createObjectURL(file));
        }
    }

    async function handleUpdateProfile(e: FormEvent) {
        e.preventDefault();
        const username = (document.getElementById("username") as HTMLInputElement).value;
        const formData = new FormData();
        formData.append("username", username);
        if (image) {
            formData.append("profile_picture", image);
        }
        await CommonApiCall({ type: "post", url: `${django_app_backend_url}/auth/me/`, payload: formData });
    }

    return (
        <div className="mt-4 p-4">
            <div className="bg-white rounded-lg shadow-lg p-8 max-w-lg mx-auto">
                <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">Edit Profile</h1>
                <form onSubmit={handleUpdateProfile} className="space-y-6">
                    <div>
                        <label htmlFor="username" className="block text-sm font-medium text-gray-700">Username</label>
                        <input
                            type="text"
                            id="username"
                            name="username"
                            required
                            autoFocus
                            defaultValue={userData?.username}
                            className=" outline-0 border-2 border-orange-200 mt-1 block p-2 w-full rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        />
                    </div>
                    <div>
                        <label htmlFor="bio" className="block text-sm font-medium text-gray-700">Bio</label>
                        <textarea
                            rows={3}
                            id="bio"
                            name="bio"
                            defaultValue={userData?.username}
                            className="outline-0 border-2 border-orange-200 mt-1 block p-2 w-full rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        />
                    </div>
                    <div>
                        <label htmlFor="image" className="block text-sm font-medium text-gray-700">Profile Picture</label>
                        <div className="mt-1 flex items-center space-x-4">
                            <div className="w-24 h-24 rounded-full overflow-hidden shadow-lg">
                                <img
                                    src={preview || "https://picsum.photos/200"}
                                    alt="Profile Preview"
                                    className="w-full h-full object-cover"
                                />
                            </div>
                            <label htmlFor="image" className="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500">
                                <span>Change</span>
                                <input id="image" name="image" type="file" className="sr-only" onChange={handleImageChange} />
                            </label>
                        </div>
                    </div>
                    <div>
                        <button
                            type="submit"
                            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                            Save Changes
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
