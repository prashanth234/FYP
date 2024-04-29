import graphene

from post.schema.mutation import createPostMutation, updatePostMutation, deletePostMutation
from post.schema.query import allPostsQuery, myPostsQuery, postDetailsQuery, trendingPostsQuery 

class PostQuery(
    allPostsQuery.AllPostsQuery,
    myPostsQuery.MyPostsQuery,
    postDetailsQuery.PostDetailsQuery,
    trendingPostsQuery.TrendingPostsQuery,
    graphene.ObjectType,
):
    pass

class PostMutation(
    createPostMutation.CreatePostMutation,
    updatePostMutation.UpdatePostMutation,
    deletePostMutation.DeletePostMutation,
    graphene.ObjectType
):
    pass