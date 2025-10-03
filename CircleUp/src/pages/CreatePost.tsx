import { useState, type FormEvent } from "react";
import { IoIosCreate } from "react-icons/io";
import { MdCancel } from "react-icons/md";
import { CommonApiCall } from "../CommonFunctions";
import { django_app_backend_url } from "../defaults";
export default function CreatePost() {
    const [image, setImage] = useState(null);
    const [preview, setPreview] = useState(null);

    function handleImageChange(e) {
        const file = e.target.files[0];
        if (file) {
            setImage(file);
            setPreview(URL.createObjectURL(file));
        }
    }

    async function handleCreatePost(e: FormEvent) {
        e.preventDefault();
        const content = (document.getElementById("content") as HTMLTextAreaElement).value;
        const formData = new FormData();
        formData.append("content", content);
        if (image) {
            formData.append("image", image);
        }
        await CommonApiCall({ type: "post", url: `${django_app_backend_url}/user/post/upload/`, payload: formData });
    }

    function handleClearPost() {
        setImage("");
        document.getElementById("content").value = '';
        setPreview(null);
    }

    return (
        <div className="flex w-full h-full justify-center items-center">
            <div className="bg-white rounded-lg flex flex-col shadow-lg p-8">
                <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">Create a New Post</h1>
                <form onSubmit={handleCreatePost} className="space-y-6">
                    <div>
                        <label htmlFor="content" className="block text-sm font-medium text-gray-700">Content</label>
                        <textarea
                            id="content"
                            name="content"
                            rows={4}
                            className="mt-1 w-full p-2 border-2 outline-0 border-orange-200 rounded-md focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        ></textarea>
                    </div>
                    <div>
                        <label htmlFor="image" className="block text-sm font-medium text-gray-700">Image</label>
                        <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                            <div className="space-y-1 text-center">
                                {
                                    preview ?
                                        (
                                            <img src={preview} alt="Preview" className="mx-auto h-48 w-auto rounded-md" />
                                        )
                                        :
                                        (
                                            <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48" aria-hidden="true">
                                                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                                            </svg>
                                        )
                                }
                                <div className="flex text-sm text-gray-600">
                                    <label htmlFor="image" className="relative cursor-pointer bg-white rounded-md font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500">
                                        <span>Upload a file</span>
                                        <input id="image" name="image" type="file" className="sr-only" required onChange={handleImageChange} />
                                    </label>
                                    <p className="pl-1">or drag and drop</p>
                                </div>
                                <p className="text-xs text-gray-500">PNG, JPG, GIF up to 10MB</p>
                            </div>
                        </div>
                    </div>
                    <div>
                        <button
                            type="button"
                            className="w-full flex items-center gap-2 justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                            onClick={handleClearPost}
                        >
                            Clear Post <MdCancel className="text-lg" />
                        </button>
                    </div>
                    <div>
                        <button
                            type="submit"
                            className="w-full flex justify-center items-center gap-2 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                            Create Post <IoIosCreate className="text-lg" />
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}