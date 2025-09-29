import { useEffect, useState } from "react";
import { CommonApiCall } from "../CommonFunctions";
import PostCard from "../components/postCard";
import { django_app_backend_url } from "../defaults";

export default function Home() {

    const [postData, setPostData] = useState({ data: [], selectedPost: false });

    async function getPosts() {
        const response = await CommonApiCall({ url: django_app_backend_url + "/get/posts", type: "get" })
        if (response) {
            setPostData({ ...postData, data: await response.data });
        }
    }

    useEffect(() => {
        getPosts()
    }, [])

    return (
        <>
            <PostCard postData={postData} setPostData={setPostData} />
        </>
    )
}
