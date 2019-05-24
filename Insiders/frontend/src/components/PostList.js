import React from "react";
import { connect } from 'react-redux';


class PostList extends React.Component {
    render() {
        const {postList} = this.props;
        
        const processedPostList = postList.map((post) => 
        <div className="container">
            <div key={post.pk} className="card">
                <div className="card-header">{post.title}</div>
                <div className="card-body">{post.body}</div>
            </div>
        </div>);

        return (
            <div>
                {processedPostList}
            </div>);
    }
}

const mapStateToProps = (state) => {
    return {
        postList: state.postList,
    }
};

export default connect(mapStateToProps)(PostList);
