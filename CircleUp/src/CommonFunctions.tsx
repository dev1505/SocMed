import axios from "axios";
import { type FormEvent } from "react";
import { Navigate } from "react-router-dom";
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
            return <Navigate to="/login" replace={true} />
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