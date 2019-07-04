import React from "react";
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { createPost } from '../store/actions';


class CreatePost extends React.Component {
    constructor(props) {
        super(props);
        this.onChangePostBody = this.onChangePostBody.bind(this);
        this.onChangePostTitle = this.onChangePostTitle.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }
    componentWillMount() {
        this.setState((state, props) =>  {return {postBody: "", postTitle: "", 
                                                  bodyNotEmpty: true, titleNotEmpty: true}});
        this.createPost = this.props.createPost;
    }

    shouldComponentUpdate(nextProps, nextState) {
        if(nextState.bodyNotEmpty != this.state.bodyNotEmpty)
            return true;
        if(nextState.titleNotEmpty != this.state.titleNotEmpty)
            return true;
        if(nextState.postBody == this.state.postBody && nextState.postTitle == this.state.postTitle){
            return false;
        }
        return true;
    }

    onChangePostBody(newString) {
        this.setState((state, props) => {return {postBody: newString}});
    }

    onChangePostTitle(newString) {
        
        this.setState((state, props) => {return {postTitle: newString}});
    }

    onSubmit(){
        const body = this.state.postBody;
        const title = this.state.postTitle;
        if(title.length === 0) {
            this.setState((state, props) => {return {titleNotEmpty: false}});
            return;
        }
        if(body.length == 0) {
            this.setState((state, props) => {return {bodyNotEmpty: false}});
            return;
        }
        const {postList} = this.props;
        this.createPost(this.state.postBody, this.state.postTitle, postList.length);
        this.setState((state, props) =>  {return {postBody: "", postTitle: "", 
                                                  bodyNotEmpty: true, titleNotEmpty: true}});
    }

    render() {
        
        return (
        <div className="container mb-auto">
            <div className="form-group">
                <input className="form-control" type="text" placeholder="Post title" value={this.state.postTitle} onChange={(event) => this.onChangePostTitle(event.target.value)}></input>
                <small className="form-text text-danger" hidden={this.state.titleNotEmpty}>Post title cannot be empty.</small>
            </div>
            <div className="form-group">
                <input className="form-control" type="text" placeholder="Post body" value={this.state.postBody} onChange={(event) => this.onChangePostBody(event.target.value)}></input>
                <small className="form-text text-danger" hidden={this.state.bodyNotEmpty}>Post body cannot be empty.</small>
            </div>
            <button className="btn btn-info" onClick={this.onSubmit}>Create post</button>
        </div>);
    }
}

const mapStateToProps = (state) => {
    return {
        postList: state.postList,
    }
};

const mapActionsToProps = (dispatch) => {
    return {
        createPost: bindActionCreators(createPost, dispatch),
    }
}

export default connect(mapStateToProps, mapActionsToProps)(CreatePost); 
