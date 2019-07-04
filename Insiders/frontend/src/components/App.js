import React from "react";
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import CreatePost from './CreatePost'
import PostList from "./PostList";


class App extends React.Component {
    render() {
        return (
        <div className="container">
            <CreatePost/>
            <hr/>
            <PostList/>
        </div>);
    }
}

const mapStateToProps = (state) => {
    return state;
};

const mapActionsToProps = (dispatch) => {
    return {}
}

export default connect(mapStateToProps, mapActionsToProps)(App);