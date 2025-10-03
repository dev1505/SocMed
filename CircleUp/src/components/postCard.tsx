import { useEffect, useState, type FormEvent } from "react";
import { FaHeart } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { checkfollowing, CommonApiCall, followUser, likePost, unFollowUser } from "../CommonFunctions";
import { django_app_backend_url } from "../defaults";
import type { Comment } from "../typedef";
import './postCard.css';

export default function PostCardModal({ postData, followButton }) {

    const intitialState: { selectedPost: Comment; openPost: boolean; follow: boolean, is_liked: boolean } = { selectedPost: {}, openPost: false, follow: false, is_liked: false }
    const [postOpen, setPostOpen] = useState(intitialState);
    const navigate = useNavigate();

    const formatTime = (timeStr) => {
        try {
            return new Date(timeStr.split("")[0]).toLocaleString();
        } catch {
            return timeStr;
        }
    };

    const [commentData, setCommentData] = useState<{ comments: Comment[]; content: string; }>({ comments: [], content: "" });

    async function getUserComments() {
        const response = await CommonApiCall({
            url: django_app_backend_url + "/user/comments/get/",
            type: "post",
            payload: { post: postOpen.selectedPost.id }
        })
        setCommentData({ ...commentData, comments: await response.data })
    }

    async function postComments(e: FormEvent) {
        e.preventDefault();
        if (e.target.value !== "") {
            const response = await CommonApiCall(
                {
                    url: django_app_backend_url + "/user/comment/post/",
                    type: "post",
                    payload: {
                        post: postOpen.selectedPost.id,
                        content: commentData.content,
                    }
                }
            )
            setCommentData({
                ...commentData,
                comments: [
                    ...commentData.comments,
                    {
                        id: response.data.id,
                        user: response.data.user,
                        content: response.data.content,
                        created_at: response.data.created_at,
                        updated_at: response.data.updated_at,
                    },
                ],
                content: "",
            });
        }
    }

    async function handleFollowing() {
        if (postOpen.follow === false) {
            const response = await followUser({ following: postOpen.selectedPost.user.id })
            setPostOpen({ ...postOpen, follow: await response.success })
        }
        else {
            const response = await unFollowUser({ following: postOpen.selectedPost.user.id })
            setPostOpen({ ...postOpen, follow: !(await response.success) })
        }
    }

    async function checkPostLike() {
        const response = await CommonApiCall({ url: `${django_app_backend_url}/user/post/check/like/${postOpen.selectedPost.id}/`, type: "get" })
        setPostOpen({ ...postOpen, selectedPost: { ...postOpen.selectedPost, is_liked: await response.is_liked ? true : false } })
        console.log("object", { ...postOpen, selectedPost: { ...postOpen.selectedPost, is_liked: await response.is_liked ? true : false } })
    }

    useEffect(() => {
        if (postOpen.openPost) {
            checkPostLike()
            getUserComments();
            (async () => {
                setPostOpen({ ...postOpen, follow: await checkfollowing({ user_id: postOpen.selectedPost.user.id }) });
            })()
        }
    }, [postOpen.openPost])

    async function handleLikePost() {
        const response = await likePost({ post_id: postOpen.selectedPost.id })
        console.log(await response)
        if (await response.success) {
            setPostOpen({ ...postOpen, selectedPost: { ...postOpen.selectedPost, is_liked: await response.message === "liked" ? true : false } })
        }
    }

    return (
        <div>
            <div className="columns-2 sm:columns-3 lg:columns-4 pt-5 gap-2">
                {
                    postData.data.map((post, index) => (
                        <div
                            key={index}
                            className="mb-2 rounded break-inside-avoid shadow cursor-pointer transform hover:scale-105 transition-transform duration-300"
                            onClick={() => setPostOpen({ ...postOpen, selectedPost: post, openPost: true })}
                        >
                            <img
                                src={post.image ? post.image : "https://picsum.photos/600/800"} // fallback URL
                                alt={`Post ${post.id}`}
                                className="w-full object-cover rounded"
                                onError={(e) => {
                                    console.log(post.id, "image failed to load");
                                    (e.target as HTMLImageElement).src = "https://picsum.photos/600/800"; // fallback
                                }}
                            />
                        </div>
                    ))
                }
            </div>
            {
                postOpen.openPost && (
                    <div
                        className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 fade-in"
                        onClick={() => {
                            setPostOpen(intitialState)
                            setCommentData({ ...commentData, comments: [], content: "" })
                        }}
                    >
                        <div
                            className="bg-white/10 w-11/12 md:w-4/5 lg:w-3/4 xl:w-2/3 h-auto md:h-4/5 rounded-2xl overflow-hidden flex flex-col md:flex-row shadow-2xl border border-white/20 slide-in"
                            onClick={(e) => e.stopPropagation()}
                        >
                            <div className="relative md:w-1/2 h-64 md:h-full">
                                <img
                                    src={postOpen.selectedPost.image}
                                    alt={`Post ${postOpen.selectedPost.id}`}
                                    className="w-full h-full object-cover"
                                />
                                <button
                                    onClick={handleLikePost}
                                    className="absolute top-4 right-4 bg-white/20 p-3 cursor-pointer rounded-full backdrop-blur-sm hover:bg-white/30 transition-colors duration-300"
                                >
                                    <FaHeart className={`${postOpen.selectedPost.is_liked ? "text-red-500" : "text-white "} text-2xl`} />
                                </button>
                            </div>

                            <div className="md:w-1/2 p-6 flex flex-col bg-gradient-to-br from-gray-900 to-gray-800 text-white">
                                <div className="flex items-center justify-between mb-4">
                                    <div
                                        className="flex items-center gap-3 cursor-pointer"
                                        onClick={() => { navigate(`/profile?user_id=${postOpen.selectedPost.user.id}`) }}
                                    >
                                        <img
                                            src={postOpen.selectedPost.user.profile_pic}
                                            alt="Profile"
                                            className="w-14 h-14 rounded-full object-cover border-2 border-white/50"
                                        />
                                        <div className="font-bold text-lg bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">{postOpen.selectedPost.user.username}</div>
                                    </div>
                                    {followButton && <button
                                        className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-5 py-2 rounded hover:from-purple-600 hover:to-pink-600 transition-all duration-300 transform hover:scale-105"
                                        onClick={handleFollowing}
                                    >{postOpen.follow === false ? "Follow" : "Unfollow"}</button>}
                                </div>

                                <p className="text-gray-300 mb-1">{postOpen.selectedPost.content}</p>
                                <div className="text-gray-400 text-sm mb-2">
                                    {formatTime(postOpen.selectedPost.created_at)}
                                </div>
                                <div className="flex-grow overflow-auto h-48 md:h-auto no-scrollbar pt-4 space-y-4">
                                    {
                                        commentData.comments.map((comment, index) => (
                                            <div key={index} className="flex items-start gap-3 slide-in" style={{ animationDelay: `${index * 100}ms` }}>
                                                <img
                                                    src={comment.user.profile_pic}
                                                    alt={comment.user.username}
                                                    className="w-10 h-10 rounded-full object-cover border-2 border-white/30"
                                                />
                                                <div className="bg-white/10 p-2 rounded-xl w-full">
                                                    <span className="font-bold bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-blue-500">{comment.user.username}</span>
                                                    <p className="text-gray-300">{comment.content}</p>
                                                    <p className="text-gray-400 text-xs">{formatTime(comment.created_at)}</p>
                                                </div>
                                            </div>
                                        ))
                                    }
                                </div>

                                <div className="pt-4">
                                    <div>
                                        <form
                                            className="flex items-center justify-center gap-3"
                                            onSubmit={postComments}
                                        >
                                            <input
                                                type="text"
                                                id="comment"
                                                placeholder="Add a comment..."
                                                onChange={(e) => { setCommentData({ ...commentData, content: e.target.value }) }}
                                                value={commentData.content}
                                                className="w-full border-none rounded-lg p-2 bg-white/10 text-white placeholder-gray-400 focus:ring-2 focus:ring-purple-500 outline-none"
                                            />
                                            <button
                                                type="submit"
                                                className="bg-gradient-to-r from-green-400 to-blue-500 text-white px-5 py-2 rounded hover:from-green-500 hover:to-blue-600 transition-all duration-300 transform hover:scale-105"
                                            >
                                                Post
                                            </button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )
            }
        </div >
    );
}
