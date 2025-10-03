import { useEffect, useState } from "react";
import { CommonApiCall, getFollowings } from "../CommonFunctions";
import PostCard from "../components/postCard";
import { django_app_backend_url } from "../defaults";

export default function Home() {

    const [postData, setPostData] = useState({ data: [] });

    async function getPosts() {
        const response = await CommonApiCall({ url: django_app_backend_url + "/get/posts/", type: "get" })
        if (response) {
            setPostData({ ...postData, data: await response.data });
        }
    }

    useEffect(() => {
        getPosts()
    }, [])

    return (
        <>
            <div>
                <form>
                    <input
                        type="text"
                        name="searchbar"
                        id="searchbar"
                        className="rounded-md bg-white mt-2 p-2 w-full focus:outline-2 outline-orange-400"
                        placeholder="Search Here"
                    />
                </form>
            </div>

            <PostCard postData={postData} followButton={true} />
        </>
    )
}
