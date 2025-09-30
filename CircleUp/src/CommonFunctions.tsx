import axios from "axios";
import { type FormEvent } from "react";
import { django_app_backend_url } from "./defaults";
import type { ApiResquestType } from "./typedef";

export async function CommonApiCall({ type = "get", payload = {}, url }: ApiResquestType) {
    try {
        let response;
        if (type === "get") {
            response = await axios.get(
                url,
                { withCredentials: true }
            );
        }
        else {
            response = await axios.post(
                url,
                payload,
                { withCredentials: true }
            );
        }
        const response_data = await response.data;
        return response_data
    } catch (response_error) {
        if (response_error?.status === 401) {
            const response = await axios.get(
                django_app_backend_url + "/api/token/refresh",
                { withCredentials: true }
            );
            if (response.status === 401) {
                window.location.href = "/login";
            }
            const response_data = response.data;
        }
        alert(JSON.stringify(response_error?.response?.data?.message) ?? "error")
        return false;
    }
}

// eslint-disable-next-line react-refresh/only-export-components
export async function handleGoogleLogin(e: FormEvent) {
    e.preventDefault();
    const getGoogleUrl = await CommonApiCall({ type: "get", url: django_app_backend_url + "/auth/google/login/" })
    window.location.href = await getGoogleUrl.data
}

// eslint-disable-next-line react-refresh/only-export-components
export async function handleGithubLogin(e: FormEvent) {
    e.preventDefault();
    const getGithubUrl = await CommonApiCall({ type: "get", url: django_app_backend_url + "/auth/github/login/" })
    window.location.href = await getGithubUrl.data
}

// eslint-disable-next-line react-refresh/only-export-components
export async function handleCallbackRedirect() {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");
    const state = urlParams.get("state");
    if (code) {
        const callbackResponse = await CommonApiCall({
            type: "get",
            url: `${django_app_backend_url}/auth/${state}/callback/?code=${encodeURIComponent(code)}`,
        });
        return callbackResponse;
    }
    else {
        return false;
    }
}

// eslint-disable-next-line react-refresh/only-export-components
export async function followUser({ following }) {
    const response = await CommonApiCall({ url: django_app_backend_url + "/user/follow/", type: "post", payload: { following } })
    return await response
}

// eslint-disable-next-line react-refresh/only-export-components
export async function unFollowUser({ following }) {
    const response = await CommonApiCall({ url: django_app_backend_url + "/user/unfollow/", type: "post", payload: { following } })
    return await response
}

// eslint-disable-next-line react-refresh/only-export-components
export async function getFollowers() {
    const response = await CommonApiCall({ url: django_app_backend_url + "/user/getfollowers/", type: "get" })
    return await response
}

// eslint-disable-next-line react-refresh/only-export-components
export async function getFollowings() {
    const response = await CommonApiCall({ url: django_app_backend_url + "/user/getfollowings/", type: "get" })
    return await response
}

// eslint-disable-next-line react-refresh/only-export-components
export async function checkfollowing({ user_id }) {
    const response = await CommonApiCall({ url: django_app_backend_url + "/user/checkfollowing/", type: "post", payload: { user_id } })
    return await response.success
}

// eslint-disable-next-line react-refresh/only-export-components
export async function likePost({ post_id }) {
    const response = await CommonApiCall({ url: django_app_backend_url + "/user/post/like/", type: "post", payload: { post_id } })
    return await response
}