import { useState } from "react";

export default function PostCardModal({ postData, setPostData }) {
    // Optional helper to format created_at 
    const formatTime = (timeStr) => {
        try {
            return new Date(timeStr).toLocaleString();
        } catch {
            return timeStr;
        }
    };

    return (
        <div>
            <div className="columns-2 sm:columns-3 lg:columns-4 pt-5 gap-2">
                {postData.data.map((post, index) => (
                    <div
                        key={index}
                        className="mb-2 rounded break-inside-avoid shadow cursor-pointer"
                        onClick={() => setPostData({ ...postData, selectedPost: post })}
                    >
                        <img
                            className="w-full object-cover rounded"
                            src={post.image}
                            alt={`Post ${post.id}`}
                        />
                    </div>
                ))}
            </div>
            {postData.selectedPost && (
                <div
                    className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
                    onClick={() => setPostData({ ...postData, selectedPost: false })}
                >
                    <div
                        className="bg-white w-11/12 md:w-3/4 h-3/4 rounded-lg overflow-hidden flex flex-col md:flex-row"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div className="md:w-1/2 h-full">
                            <img
                                src={postData.selectedPost.image}
                                alt={`Post ${postData.selectedPost.id}`}
                                className="w-full h-full object-cover"
                            />
                        </div>

                        <div className="md:w-1/2 p-6 flex flex-col justify-between">
                            <div>
                                <h2 className="text-xl font-semibold mb-2">
                                    Post #{postData.selectedPost.id}
                                </h2>
                                <p className="text-gray-700 mb-4">{postData.selectedPost.content}</p>
                            </div>

                            <div className="flex items-center justify-between space-x-3 font-bold">
                                <div className="flex items-center gap-2">
                                    <img
                                        src={`https://picsum.photos/seed/user${postData.selectedPost.user}/100`}
                                        alt="Profile"
                                        className="w-16 h-16 rounded-full object-cover"
                                    />
                                    <div className="text-gray-500">User {postData.selectedPost.user}</div>
                                </div>
                                <div className="text-gray-500">
                                    {formatTime(postData.selectedPost.created_at)}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
