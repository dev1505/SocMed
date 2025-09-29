import { useEffect, useState } from "react";
import { CommonApiCall } from "../CommonFunctions";
import { django_app_backend_url } from "../defaults";

export default function UserList({ listType }) {
    const [users, setUsers] = useState([{ id: 1, username: "DEV" }, { id: 1, username: "DEV" }, { id: 1, username: "DEV" }]);

    useEffect(() => {
        async function fetchUsers() {
            const response = await CommonApiCall({ type: "get", url: `${django_app_backend_url}/auth/me/${listType}` });
            if (response) {
                setUsers(response.data);
            }
        }
        fetchUsers();
    }, [listType]);

    return (
        <div className="container mx-auto p-4">
            <div className="bg-white rounded-lg shadow-lg p-8 max-w-lg mx-auto">
                <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">{listType === 'followers' ? 'Followers' : 'Following'}</h1>
                <div className="space-y-4">
                    {users.map((user, index) => (
                        <div key={user.id} className={`flex items-center space-x-4 p-2 hover:bg-gray-100 ${index !== users.length - 1 && "border-b-1 border-gray-200"}`}>
                            <div className="w-16 h-16 rounded-full overflow-hidden shadow-lg">
                                <img
                                    src={user.profile_picture || "https://picsum.photos/200"}
                                    alt="Profile"
                                    className="w-full h-full object-cover"
                                />
                            </div>
                            <div>
                                <p className="font-bold text-gray-800">{user.username}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
