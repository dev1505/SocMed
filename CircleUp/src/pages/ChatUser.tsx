import { useEffect, useRef, useState } from "react";
import { Navigate, useNavigate, useSearchParams } from "react-router-dom";
import { CommonApiCall } from "../CommonFunctions";
import { django_app_backend_url, django_chat_app_backend_url } from "../defaults";

export default function ChatUser() {
    const [searchParams] = useSearchParams();
    const to_user_id = searchParams.get("user_id");
    const current_id = searchParams.get("current");
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const messagesEndRef = useRef(null);
    const socketRef = useRef(null);
    const [userData, setUserData] = useState({ currentUser: "", otherUser: "" })
    async function getUserInfo() {
        const response1 = await CommonApiCall({ url: django_app_backend_url + "/auth", type: "get" })
        const response2 = await CommonApiCall({ url: django_app_backend_url + "/auth?user_id=" + to_user_id, type: "get" })
        setUserData({ currentUser: await response1?.data, otherUser: await response2?.data })
    }

    async function loadUserMessages() {
        const response = await CommonApiCall({
            url: `${django_app_backend_url}/user/messages/${to_user_id}/`,
            type: "get",
        });

        if (response?.data) {
            const mappedMessages = response.data.map((msg) => ({
                text: msg.message,
                sender: msg.from_user === parseInt(to_user_id) ? "other" : "me",
            }));
            setMessages(mappedMessages);
        }
    }

    const navigate = useNavigate();

    useEffect(() => {

        loadUserMessages();
        getUserInfo();

        let roomName = "";
        if (current_id && to_user_id) {
            if (current_id > to_user_id) {
                roomName = to_user_id + "" + current_id;
            }
            else {
                roomName = current_id + "" + to_user_id;

            }
        }
        else {
            roomName = "room1";
        }

        socketRef.current = new WebSocket(`${django_chat_app_backend_url}/ws/chat/${roomName}/`);

        socketRef.current.onopen = () => console.log("connected");

        socketRef.current.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                setMessages((prev) => [
                    ...prev,
                    { text: data.message, sender: "other" },
                ]);
            } catch {
                console.error("Invalid WS message:", event.data);
            }
        };

        socketRef.current.onclose = () => console.log("disconnected");

        return () => socketRef.current.close();
    }, [to_user_id]);

    // Auto-scroll to bottom on new messages
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const sendMessage = () => {
        if (!input.trim()) return;

        if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
            socketRef.current.send(
                JSON.stringify({ message: input, to_user_id: to_user_id })
            );
        }

        setMessages((prev) => [
            ...prev,
            { text: input, sender: "me" },
        ]);
        setInput("");
    };
    function parseMessageTime(date, time) {
        if (!date || !time) return "";
        const cleanedTime = time.split(".")[0]; // "13:25:05"
        const dateTimeStr = `${date}T${cleanedTime}`;
        const d = new Date(dateTimeStr);
        if (isNaN(d)) return "";
        return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    }

    return (
        <div className="flex flex-col pt-3 h-full">
            <header className="border border-stone-600 rounded z-10">
                <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        <div className="flex items-center" onClick={() => { navigate("/profile?user_id=" + userData.otherUser.id) }}>
                            <img
                                className="h-10 w-10 rounded-full object-cover"
                                src={userData?.otherUser?.profile_pic || "https://picsum.photos/100"}
                                alt="User avatar"
                            />
                            <div className="ml-3">
                                <h1 className="text-lg font-semibold text-gray-900">
                                    {userData?.otherUser?.username}
                                </h1>
                                <p className="text-sm text-gray-500">Online</p>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            <main className="flex-1 overflow-y-auto p-4 flex flex-col">
                <div className="max-w-4xl flex-1 flex flex-col gap-4">
                    {messages.map((msg, index) => (
                        <div
                            key={index}
                            className={`flex items-end gap-2 flex-col ${msg?.sender === "me" ? "items-end" : "items-start"}`}
                        >
                            <div className={`flex items-end gap-2 ${msg?.sender === "me" ? "justify-end" : "justify-start"}`}>
                                {msg?.sender === "other" && (
                                    <img
                                        onClick={() => { navigate("/profile?user_id=" + userData.otherUser.id) }}
                                        className="h-8 w-8 rounded-full object-cover"
                                        src={userData?.otherUser?.profile_pic || "https://picsum.photos/100"}
                                        alt="User avatar"
                                    />
                                )}
                                <div
                                    className={`px-4 py-2 rounded-2xl max-w-md md:max-w-lg break-words ${msg?.sender === "me"
                                        ? "bg-blue-600 text-white rounded-br-none"
                                        : "bg-white text-gray-800 shadow-sm rounded-bl-none"
                                        }`}
                                >
                                    {msg?.text}
                                </div>
                                {msg?.sender === "me" && (
                                    <img
                                        className="h-8 w-8 rounded-full object-cover"
                                        src={userData?.currentUser?.profile_pic || "https://picsum.photos/100"}
                                        alt="User avatar"
                                    />
                                )}
                            </div>

                            <span className="text-xs text-gray-400 mt-1">
                                {parseMessageTime(msg?.date, msg?.message_time)}
                            </span>
                        </div>
                    ))}

                    <div ref={messagesEndRef} />
                </div>
            </main>

            <footer className="border-t p-4">
                <div className="max-w-4xl mx-auto">
                    <div className="flex items-center gap-2">
                        <input
                            type="text"
                            placeholder="Type a message..."
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                            className="flex-1 p-3 border-gray-300 rounded-full focus:ring-blue-500 focus:border-blue-500 outline-none transition"
                        />
                        <button
                            onClick={sendMessage}
                            className="inline-flex items-center justify-center h-12 w-12 rounded-full bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                className="h-6 w-6"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M5 12h14M12 5l7 7-7 7"
                                />
                            </svg>
                        </button>
                    </div>
                </div>
            </footer>
        </div>
    );
}
