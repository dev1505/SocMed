import { FaHome, FaUserCircle } from "react-icons/fa";
import { MdAddCircle, MdMessage } from "react-icons/md";
import { useNavigate } from "react-router-dom";
import { CommonApiCall } from "../CommonFunctions";
import { django_app_backend_url } from "../defaults";

import { IoLogOut } from "react-icons/io5";
export default function Sidebar() {

    const navigate = useNavigate();

    const sideBarContents = [
        { name: "Home", icon: FaHome, path: "/" },
        { name: "Messages", icon: MdMessage, path: "/chat" },
        { name: "Create Post", icon: MdAddCircle, path: "/create" },
        { name: "User Profile", icon: FaUserCircle, path: "/profile" },
    ]

    async function handleLogout() {
        const response = await CommonApiCall({ url: django_app_backend_url + "/user/logout", type: "get" })
        if (response) {
            navigate("/login")
        }
    }

    return (
        <div>
            <div className="bg-orange-100 md:border-r-2 border-t-2 md:border-t-0 border-orange-300 flex flex-row md:flex-col justify-evenly items-center w-screen h-1/12 md:w-1/12 md:h-screen fixed bottom-0">
                {
                    sideBarContents?.map((data, index) => {
                        const IconElement = data?.icon;
                        return (
                            <div
                                key={index}
                                title={data.name}
                                className="cursor-pointer"
                                onClick={() => { navigate(data?.path) }}
                            >
                                <IconElement className="text-4xl" />
                            </div>
                        )
                    })
                }
                <div
                    title={"logout"}
                    className="cursor-pointer"
                    onClick={() => handleLogout()}
                >
                    <IoLogOut className="text-4xl" />
                </div>
            </div>
        </div >
    )
}
