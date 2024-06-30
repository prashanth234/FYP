import graphene

from post.schema.mutation import createPostMutation, updatePostMutation, deletePostMutation, likeMutation
from post.schema.query import allPostsQuery, myPostsQuery, competitionPostsQuery, postDetailsQuery, likeQuery

class PostQuery(
    allPostsQuery.AllPostsQuery,
    myPostsQuery.MyPostsQuery,
    postDetailsQuery.PostDetailsQuery,
    likeQuery.LikeCountQuery,
    competitionPostsQuery.CompetitionPostsQuery,
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