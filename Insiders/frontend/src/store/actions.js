export const ACTION_CREATE_POST = 1; 

export const createPost = (postBody, postTitle, pk) => {
    return {
        type: ACTION_CREATE_POST,
        payload: {pk: pk, body: postBody, title: postTitle}
    };
} 
