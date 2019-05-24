import {ACTION_CREATE_POST} from './actions'

const initialState = {
    postList: []
};

export const rootReducer = (state = initialState, action) => {
    switch(action.type)
    {
        case ACTION_CREATE_POST:
            return {...state, 
                postList: state.postList.concat({body: action.payload.body, 
                                                 title: action.payload.title,
                                                 pk: action.payload.pk
                                                 })};
    }
    return state;
}; 
