export type ApiResquestType = {
    type: string;
    url: string;
    payload?: object;
}

export type Comment = {
    id: number;
    user: { username: string, id: number, profile_pic: string };
    content: string;
    created_at?: string;
    updated_at?: string;
};
