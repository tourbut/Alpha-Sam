export interface Token {
    access_token: string;
    token_type: string;
}

export interface UserLogin {
    username: string;
    password: string;
}

export interface UserCreate {
    email: string;
    password: string;
    full_name?: string;
}

export interface UserPasswordUpdate {
    current_password: string;
    new_password: string;
}
