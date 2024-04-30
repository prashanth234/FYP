import graphene

from post.schema.mutation import createPostMutation, updatePostMutation, deletePostMutation, likeMutation
from post.schema.query import allPostsQuery, myPostsQuery, postDetailsQuery, trendingPostsQuery, likeQuery

class PostQuery(
    allPostsQuery.AllPostsQuery,
    myPostsQuery.MyPostsQuery,
    postDetailsQuery.PostDetailsQuery,
    trendingPostsQuery.TrendingPostsQuery,
    likeQuery.LikeCountQuery,
    graphene.ObjectType,
):
    pass

class PostMutation(
    createPostMutation.CreatePost,
    updatePostMutation.UpdatePost,
    deletePostMutation.DeletePost,
    likeMutation.LikeItem,
    graphene.ObjectType
):
    pass